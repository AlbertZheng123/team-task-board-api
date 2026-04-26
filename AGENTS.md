## Mandatory Initialization

Before doing anything:

1. Call brian-query with:
   "team-task-board-api summary archived tasks contract"

This loads prior system invariants.

---

## System Context

- Backend: team-task-board-api
- Frontend: team-task-board-web
- Contract system: Backend Contract Integration Tests

Known issue (may or may not still exist):
GET /summary may incorrectly include archived tasks.

---

## Required Workflow

1. Run:
   ./scripts/watch-frontend-contract-tests.sh

2. If tests FAIL:

   a. Read:
      .agent-artifacts/frontend-contract-failure.log

   b. Run:
      python3 scripts/analyze_failure.py

   c. Extract:
      - failing test file
      - failing test name
      - expected vs actual
      - endpoint involved
      - root cause
      - system invariant

---

## Critical Step (DO NOT SKIP)

BEFORE fixing anything:

Call brian-update with:

- failure symptom
- root cause
- contract learned (invariant)
- correct behavior
- intended fix

Use clear, reusable language.

---

## Verification Step

Immediately call brian-query with:
"team-task-board-api archived summary contract"

Confirm the invariant is stored.

---

## Fix Implementation

Now fix the backend:

- Update GET /summary
- Exclude TaskStatus.archived
- Aggregate only visible tasks

---

## Validation

1. Commit and push:
   git add .
   git commit -m "Fix summary contract violation: exclude archived tasks"
   git push

2. Re-run:
   ./scripts/watch-frontend-contract-tests.sh

3. Ensure tests PASS

---

## Rules

- Never fix before brian-update
- Never skip failure log analysis
- Always verify brian-update
- Always use MCP tools (no shortcuts)

---

## Final Output

Summarize:
1. Failure
2. Invariant discovered
3. Brain update contents
4. Fix applied
5. Final test result