"""Deterministic stdlib model of the Hercules capability-routing contract.

The owning Skill consumes this normalized decision contract. Maintainer tests
feed it mocked local evidence for the architecture's capability matrix. The
file is non-executable and has no discovery or mutation side effects.
"""

from __future__ import annotations


SANITIZED_FAILURES = {
    "missing executable",
    "unsupported command",
    "provider/access rejection",
    "unavailable capability",
    "runtime failure",
}

VALID_AUTHORITIES = {"read-only", "write-capable"}
CONCRETE_SURFACE_EVIDENCE_TOKENS = {
    "definition",
    "docs",
    "documentation",
    "help",
    "instructions",
    "manifest",
    "metadata",
    "schema",
}


def _authority_fits(required, offered):
    if required == "write-capable":
        return offered == "write-capable"
    return offered in VALID_AUTHORITIES


def _unique_strings(values):
    if isinstance(values, str):
        values = [values]
    return list(dict.fromkeys(value for value in values or [] if isinstance(value, str)))


def _is_concrete_surface_evidence(evidence):
    if not isinstance(evidence, str) or not evidence.strip():
        return False
    normalized = evidence.lower()
    for separator in ("_", "/", " ", "."):
        normalized = normalized.replace(separator, "-")
    tokens = {token for token in normalized.split("-") if token}
    return bool(tokens & CONCRETE_SURFACE_EVIDENCE_TOKENS)


def _normalize_surface(surface):
    if not isinstance(surface, dict):
        return None
    name = surface.get("name")
    family = surface.get("family")
    evidence = surface.get("evidence")
    authority = surface.get("authority")
    if (
        not name
        or not family
        or authority not in VALID_AUTHORITIES
        or not _is_concrete_surface_evidence(evidence)
    ):
        return None
    return {
        "family": family,
        "name": name,
        "capabilities": _unique_strings(surface.get("capabilities")),
        "authority": authority,
        "evidence": evidence,
    }


def _surface_coverage(surfaces, *, required_authority):
    covered = set()
    for surface in surfaces:
        if _authority_fits(required_authority, surface["authority"]):
            covered.update(surface["capabilities"])
    return covered


def _focus_surfaces(surfaces, *, required_capabilities, required_authority):
    focused = []
    for surface in surfaces:
        if not _authority_fits(required_authority, surface["authority"]):
            continue
        capabilities = [
            capability
            for capability in surface["capabilities"]
            if capability in required_capabilities
        ]
        if capabilities:
            focused.append({**surface, "capabilities": capabilities})
    return focused


def _normalize_cached_route(
    cached,
    *,
    role,
    required_authority,
    required_capabilities,
    fingerprint,
):
    if not isinstance(cached, dict):
        return None
    record = {
        "role": cached.get("role"),
        "facility": cached.get("facility"),
        "kind": cached.get("kind", "cached"),
        "confirmed_surface": list(cached.get("confirmed_surface", [])),
        "authority": cached.get("authority"),
        "evidence": cached.get("evidence"),
        "fingerprint": cached.get("fingerprint"),
    }
    if (
        record["role"] != role
        or not record["facility"]
        or role not in record["confirmed_surface"]
        or record["authority"] not in VALID_AUTHORITIES
        or not _authority_fits(required_authority, record["authority"])
        or not isinstance(record["evidence"], str)
        or not record["evidence"].strip()
        or record["fingerprint"] != fingerprint
    ):
        return None

    required = set(required_capabilities)
    proved = set(_unique_strings(cached.get("required_capabilities")))
    if proved != required:
        return None

    if required_capabilities:
        surfaces = []
        for surface in cached.get("confirmed_surfaces", []):
            normalized = _normalize_surface(surface)
            if normalized is not None:
                surfaces.append(normalized)
        surfaces = _focus_surfaces(
            surfaces,
            required_capabilities=required,
            required_authority=required_authority,
        )
        covered = _surface_coverage(
            surfaces,
            required_authority=required_authority,
        )
        if not required <= covered:
            return None
        record["required_capabilities"] = list(required_capabilities)
        record["confirmed_surfaces"] = surfaces
    return record


def decide_route(*, demand, facilities, cache=None, invocation=None, evidence=None):
    """Return observable route/map/fallback/failure state from local evidence."""
    role = demand["role"]
    required_authority = demand.get("authority", "read-only")
    required_capabilities = _unique_strings(demand.get("required_capabilities"))
    required_set = set(required_capabilities)
    fingerprint = (evidence or {}).get("fingerprint")
    cache_invalidated = False
    invalidation_reason = None
    cached_route = None
    cached_record = None

    if cache:
        if cache.get("fingerprint") != fingerprint:
            cache_invalidated = True
            invalidation_reason = "stale-cache"
        else:
            routes = cache.get("routes") or {}
            if role not in routes:
                cache_invalidated = True
                invalidation_reason = "cache-missing-role"
            else:
                cached_record = _normalize_cached_route(
                    routes[role],
                    role=role,
                    required_authority=required_authority,
                    required_capabilities=required_capabilities,
                    fingerprint=fingerprint,
                )
                if cached_record is None:
                    cache_invalidated = True
                    invalidation_reason = "invalid-cache-record"
                else:
                    cached_route = cached_record["facility"]

    scanned = []
    deep_inspection = []
    candidates = []
    capability_records = []
    missing_requirements = {}
    invocation_failed = invocation and not invocation.get("ok", False)
    if cached_route is not None and not invocation_failed:
        capability_records.append(cached_record)
    else:
        for facility in facilities:
            declared = _unique_strings(facility.get("capabilities"))
            deep = _unique_strings(facility.get("deep_capabilities"))
            relevant = role in declared or (
                facility.get("kind") == "plugin"
                and facility.get("relevant") is True
                and role in deep
            )
            if not relevant:
                continue
            scanned.append(facility["name"])
            confirmed = declared
            if role not in confirmed:
                deep_inspection.append(facility["name"])
                confirmed = deep

            facility_authority = facility.get("authority")
            facility_evidence = facility.get("evidence")
            if (
                role not in confirmed
                or facility_authority not in VALID_AUTHORITIES
                or not isinstance(facility_evidence, str)
                or not facility_evidence.strip()
                or not _authority_fits(required_authority, facility_authority)
            ):
                continue

            surfaces = []
            for surface in facility.get("surfaces", []):
                normalized = _normalize_surface(surface)
                if normalized is not None:
                    surfaces.append(normalized)
            surfaces = _focus_surfaces(
                surfaces,
                required_capabilities=required_set,
                required_authority=required_authority,
            )
            covered = _surface_coverage(
                surfaces,
                required_authority=required_authority,
            )
            missing = required_set - covered

            if missing:
                deep_surfaces = []
                for surface in facility.get("deep_surfaces", []):
                    normalized = _normalize_surface(surface)
                    if normalized is not None and missing.intersection(
                        normalized["capabilities"]
                    ):
                        deep_surfaces.append(normalized)
                if deep_surfaces:
                    if facility["name"] not in deep_inspection:
                        deep_inspection.append(facility["name"])
                    surfaces.extend(_focus_surfaces(
                        deep_surfaces,
                        required_capabilities=required_set,
                        required_authority=required_authority,
                    ))
                    covered = _surface_coverage(
                        surfaces,
                        required_authority=required_authority,
                    )
                    missing = required_set - covered

            if missing:
                missing_requirements[facility["name"]] = sorted(missing)
                continue

            candidates.append(facility)
            record = {
                "role": role,
                "facility": facility["name"],
                "kind": facility.get("kind", "unknown"),
                "confirmed_surface": list(confirmed),
                "authority": facility_authority,
                "evidence": facility_evidence,
                "fingerprint": fingerprint,
            }
            if required_capabilities:
                record["required_capabilities"] = list(required_capabilities)
                record["confirmed_surfaces"] = list(surfaces)
            capability_records.append(record)

    preferred = demand.get("user_preference") or demand.get("project_preference")
    if preferred:
        candidates.sort(key=lambda item: item["name"] != preferred)

    route = cached_route if cached_route is not None and not invocation_failed else None
    if route is None:
        route = candidates[0]["name"] if candidates else None
    fallback = None
    failure = None
    if invocation_failed:
        attempted = invocation.get("facility")
        raw_category = invocation.get("category", "runtime failure")
        category = raw_category if raw_category in SANITIZED_FAILURES else "runtime failure"
        failure = {"facility": attempted, "category": category}
        cache_invalidated = True
        invalidation_reason = "invocation-failure"
        alternatives = [item for item in candidates if item["name"] != attempted]
        route = alternatives[0]["name"] if alternatives else None
        if route is not None:
            fallback = {"from": attempted, "to": route, "reason": category}

    blocker = None
    if route is None:
        blocker = f"No confirmed safe capability for {role}."
        if failure is None:
            failure = {"facility": None, "category": "unavailable capability"}

    return {
        "route": route,
        "capability_map": {role: capability_records},
        "discovery": {
            "roles": [role],
            "scanned": scanned,
            "required_capabilities": required_capabilities,
            "missing_requirements": missing_requirements,
        },
        "deep_inspection": deep_inspection,
        "fallback": fallback,
        "failure": failure,
        "blocker": blocker,
        "cache_invalidated": cache_invalidated,
        "invalidation_reason": invalidation_reason,
        "commands": [],
    }
