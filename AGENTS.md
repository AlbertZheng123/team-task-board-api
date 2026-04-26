# Agent Instructions

This repository participates in a cross-repo contract testing system.

## System Overview

- Backend repo: team-task-board-api
- Frontend repo: team-task-board-web
- Frontend workflow: Backend Contract Integration Tests
- Watcher script: ./scripts/watch-frontend-contract-tests.sh
- Failure log path: .agent-artifacts/frontend-contract-failure.log

## Required Workflow

When implementing or modifying backend behavior:

1. Run:
   ./scripts/watch-frontend-contract-tests.sh

2. If tests FAIL:
   - Read: .agent-artifacts/frontend-contract-failure.log
   - Run: python3 scripts/analyze_failure.py
   - Extract the system invariant

3. BEFORE fixing code:
   - Call MCP tool to store:
     - failure log
     - invariant
     - root cause

4. Then fix backend code

5. Re-run watcher until tests PASS

## Rule

Never fix a failing contract test without first recording the invariant.