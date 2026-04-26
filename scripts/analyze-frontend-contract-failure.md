# Frontend Contract Failure Analysis Protocol

When `.agent-artifacts/frontend-contract-failure.log` exists, analyze it before fixing code.

## Required analysis

Extract:

1. failing workflow
2. failing test file
3. failing test name
4. expected value
5. received value
6. backend endpoint or behavior involved
7. root cause
8. durable cross-repo invariant
9. future guidance for agents

## Required KB update shape

Call the MCP knowledge-base update tool with:

{
  "type": "cross_repo_contract_failure",
  "backend_repo": "team-task-board-api",
  "frontend_repo": "team-task-board-web",
  "failing_workflow": "Backend Contract Integration Tests",
  "failing_test_file": "...",
  "failing_test_name": "...",
  "failure_symptom": "...",
  "root_cause": "...",
  "contract_learned": "...",
  "future_agent_guidance": "...",
  "evidence": {
    "github_actions_log": ".agent-artifacts/frontend-contract-failure.log",
    "backend_files_changed": ["..."],
    "frontend_test_file": "..."
  }
}

## Rule

Do not patch the backend until the KB update has been written.
