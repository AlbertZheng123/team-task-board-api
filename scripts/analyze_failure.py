import json
import re

LOG_PATH = ".agent-artifacts/frontend-contract-failure.log"

def extract_failure():
    with open(LOG_PATH, "r") as f:
        log = f.read()

    # Extract test name
    test_name_match = re.search(r"Backend summary contract > (.+)", log)
    test_name = test_name_match.group(1) if test_name_match else "unknown"

    # Extract expected / received
    expected_match = re.search(r"- (\d+)", log)
    received_match = re.search(r"\+ (\d+)", log)

    expected = expected_match.group(1) if expected_match else "unknown"
    received = received_match.group(1) if received_match else "unknown"

    return {
        "test_name": test_name,
        "expected": expected,
        "received": received,
        "raw_log": log[:1000]
    }

def main():
    failure = extract_failure()

    kb_entry = {
        "type": "cross_repo_contract_failure",
        "failing_test_name": failure["test_name"],
        "failure_symptom": f"Expected {failure['expected']} but got {failure['received']}",
        "root_cause": "Backend summary includes archived tasks",
        "contract_learned": "Summary must exclude archived tasks",
        "future_agent_guidance": "Filter archived tasks from summary counts"
    }

    print(json.dumps(kb_entry, indent=2))

if __name__ == "__main__":
    main()
