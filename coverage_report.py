import json
from pathlib import Path

from automation_map import AUTOMATION_MAP

PROJECT_ROOT = Path(__file__).resolve().parent
TEST_CASES_PATH = PROJECT_ROOT / "generated_test_cases.json"


def main():
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = data["test_cases"]
    total = len(test_cases)
    automated = [tc for tc in test_cases if tc["tc_id"] in AUTOMATION_MAP]
    not_automated = [tc for tc in test_cases if tc["tc_id"] not in AUTOMATION_MAP]

    coverage_pct = (len(automated) / total * 100) if total else 0

    print("=== Automation Coverage Report ===\n")
    print(f"Automation coverage: {len(automated)}/{total} test cases ({coverage_pct:.0f}%)\n")

    print("Automated (real Playwright test behind each):")
    for tc in automated:
        print(f"  [x] {tc['tc_id']} | {tc['scenario']} -> {AUTOMATION_MAP[tc['tc_id']]}")

    print("\nDesigned but NOT yet automated:")
    for tc in not_automated:
        print(f"  [ ] {tc['tc_id']} | {tc['scenario']} (priority: {tc['priority']})")


if __name__ == "__main__":
    main()
