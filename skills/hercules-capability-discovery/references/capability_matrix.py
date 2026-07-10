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


def _authority_fits(required, offered):
    if required == "write-capable":
        return offered == "write-capable"
    return offered in {"read-only", "write-capable"}


def _normalize_cached_route(cached, *, role, required_authority, fingerprint):
    if not isinstance(cached, dict):
        return None
    record = {
        "role": cached.get("role"),
        "facility": cached.get("facility"),
        "kind": cached.get("kind", "cached"),
        "confirmed_surface": list(cached.get("confirmed_surface", [])),
        "authority": cached.get("authority", "read-only"),
        "evidence": cached.get("evidence"),
        "fingerprint": cached.get("fingerprint"),
    }
    if (
        record["role"] != role
        or not record["facility"]
        or role not in record["confirmed_surface"]
        or not _authority_fits(required_authority, record["authority"])
        or not record["evidence"]
        or record["fingerprint"] != fingerprint
    ):
        return None
    return record


def decide_route(*, demand, facilities, cache=None, invocation=None, evidence=None):
    """Return observable route/map/fallback/failure state from local evidence."""
    role = demand["role"]
    required_authority = demand.get("authority", "read-only")
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
    invocation_failed = invocation and not invocation.get("ok", False)
    if cached_route is not None and not invocation_failed:
        capability_records.append(cached_record)
    else:
        for facility in facilities:
            declared = list(facility.get("capabilities", []))
            deep = list(facility.get("deep_capabilities", []))
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
            if role not in confirmed or not _authority_fits(
                required_authority, facility.get("authority", "read-only")
            ):
                continue
            candidates.append(facility)
            capability_records.append({
                "role": role,
                "facility": facility["name"],
                "kind": facility.get("kind", "unknown"),
                "confirmed_surface": list(confirmed),
                "authority": facility.get("authority", "read-only"),
                "evidence": facility.get("evidence", "local-metadata"),
                "fingerprint": fingerprint,
            })

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
        "discovery": {"roles": [role], "scanned": scanned},
        "deep_inspection": deep_inspection,
        "fallback": fallback,
        "failure": failure,
        "blocker": blocker,
        "cache_invalidated": cache_invalidated,
        "invalidation_reason": invalidation_reason,
        "commands": [],
    }
