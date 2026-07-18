# Invocation Failure Contract

Use this contract only after a real task invocation fails.

## Failure Record

Record:

- selected facility and attempted operation;
- authority requested;
- exit status or equivalent observable result;
- one sanitized failure category;
- confirmed fallbacks considered and the selected next route;
- whether the failure changes a user/project-designated gate, reviewer independence, or other assurance.

Never include secrets, credentials, tokens, personal paths, private endpoints, or raw payloads in the record.

## Stable Categories

Choose the narrowest supported category:

- capability unavailable;
- authority denied;
- permission or sandbox rejection;
- invocation rejected;
- transport or network failure;
- resource or quota limit;
- timeout or interruption;
- malformed brief or input;
- unknown.

Do not infer a category not supported by the observed error. Mark uncertainty explicitly.

## Immediate User Notification

When the selected facility becomes unavailable and the next route changes facility/controller, a designated gate can no longer be satisfied, or the assurance/independence status changes, notify the user immediately before invoking the fallback. The existence of a safe fallback does not make a selected-facility failure silent. A facility that the current task selected or designated is no longer an optional missing facility.

The notification must contain only:

```text
facility: <selected facility>
category: <sanitized failure category>
fallback: <selected next route | none>
assurance: <preserved | changed, with the affected gate>
user action: <none now | minimum action needed>
```

Do not require the user to inspect tool logs or reasoning to discover the failure. Continue automatically when a safe fallback preserves the required assurance and `user action` is `none now`; notification is status, not a request for permission. If the fallback weakens or cannot satisfy a required gate, mark the task `BLOCKED` or the gate unsatisfied rather than presenting fallback verification as equivalent.

A bounded same-facility retry may remain quiet only when it uses the same capability and authority, does not change assurance, and follows locally confirmed invocation guidance. If that retry fails, leaves the selected facility, or changes assurance, notify immediately.

## Fallback Decision

1. Build and emit any required immediate notification before invoking the fallback.
2. If another confirmed facility has the required capability and authority, invoke it with the same bounded brief.
3. If the task can be narrowed safely, reduce scope and use a confirmed facility with sufficient authority.
4. If the current controller can complete the task within its authority, execute directly and verify.
5. Otherwise report the blocker, sanitized category, attempted route, assurance gap, and minimum user decision needed.

Do not expose the raw failure while handing off. A fallback still requires fresh task-appropriate verification.
