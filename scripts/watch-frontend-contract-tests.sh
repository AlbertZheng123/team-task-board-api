#!/usr/bin/env bash
set -euo pipefail

FRONTEND_REPO="AlbertZheng123/team-task-board-web"
WORKFLOW_NAME="Backend Contract Integration Tests"
BACKEND_SHA="$(git rev-parse HEAD)"

RUN_ID=""

for i in {1..40}; do
  RUN_ID=$(gh run list \
    --repo "$FRONTEND_REPO" \
    --workflow "$WORKFLOW_NAME" \
    --json databaseId,displayTitle \
    --limit 20 \
    --jq ".[] | select(.displayTitle | contains(\"$BACKEND_SHA\")) | .databaseId" \
    | head -n 1)

  if [ -n "$RUN_ID" ]; then
    echo "Found frontend workflow run: $RUN_ID"
    break
  fi

  echo "Waiting for frontend workflow..."
  sleep 10
done

if [ -z "$RUN_ID" ]; then
  echo "No frontend workflow found for backend SHA $BACKEND_SHA"
  exit 1
fi

gh run watch "$RUN_ID" --repo "$FRONTEND_REPO" --compact || true

CONCLUSION=$(gh run view "$RUN_ID" \
  --repo "$FRONTEND_REPO" \
  --json conclusion \
  --jq ".conclusion")

if [ "$CONCLUSION" != "success" ]; then
  mkdir -p .agent-artifacts
  gh run view "$RUN_ID" \
    --repo "$FRONTEND_REPO" \
    --log > .agent-artifacts/frontend-contract-failure.log

  echo "Frontend contract tests failed."
  echo "Logs saved to .agent-artifacts/frontend-contract-failure.log"
  exit 2
fi

echo "Frontend contract tests passed."
