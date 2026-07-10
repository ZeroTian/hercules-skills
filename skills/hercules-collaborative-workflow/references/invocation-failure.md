# Invocation Failure Contract

Use this contract only after a real task invocation fails.

## Failure Record

Record:

- selected facility and attempted operation;
- authority requested;
- exit status or equivalent observable result;
- one sanitized failure category;
- confirmed fallbacks considered and the selected next route.

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

## Fallback Decision

1. If another confirmed facility has the required capability and authority, invoke it with the same bounded brief.
2. If the task can be narrowed safely, reduce scope and use a confirmed facility with sufficient authority.
3. If the current controller can complete the task within its authority, execute directly and verify.
4. Otherwise report the blocker, the sanitized category, attempted route, and minimum user decision needed.

Do not expose the raw failure while handing off. A fallback still requires fresh task-appropriate verification.
