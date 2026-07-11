# Hercules Collaborative Workflow

## Purpose

This internal workflow turns task capability roles and a confirmed capability map into bounded, facility-neutral invocations. Select by demonstrated task fit and authority; a facility name never implies a fixed role.

## Procedure

1. consume the confirmed capability map;
2. apply user and project preference;
3. classify read-only versus write-capable authority;
4. write a capability-aware brief without naming unavailable surfaces;
5. invoke the selected facility;
6. on failure record a sanitized failure category and choose fallback;
7. run task-appropriate verification and report evidence.

## Invocation Brief

Give the selected facility only what it can use:

- objective and relevant context;
- allowed scope and authority boundary;
- acceptance criteria and prohibited mutations;
- verification commands or observable checks;
- expected evidence and handoff shape.

Do not request a command, plugin, agent, browser, or data surface absent from the confirmed capability map. A read-only facility may inspect and report; only a confirmed write-capable facility may mutate state.

## Selection and Fallback

Use this order: explicit user preference, project instructions, confirmed task fit, least sufficient authority, then availability. If invocation fails, follow [invocation failure](invocation-failure.md), choose another confirmed suitable facility, narrow the task, or execute directly within current authority. Report a blocker only when no safe fallback can meet the task.

## Verification

Verification must match the task and be fresh after the final change. Inspect actual outputs rather than trusting a facility summary. Report the selected route, authority used, fallback if any, verification command or check, and observed result.

## Common Mistakes

- Treating a familiar facility as permanently assigned to implementation or review.
- Giving write work to a read-only surface.
- Mentioning unavailable capabilities in a brief.
- Repeating a failed invocation without classifying and sanitizing the error.
- Closing from self-report without task-appropriate evidence.
