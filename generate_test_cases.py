import json
from pathlib import Path

from agent.agent import analyze_requirement, design_scenarios, write_test_cases

PROJECT_ROOT = Path(__file__).resolve().parent
USER_STORY_PATH = PROJECT_ROOT / "agent" / "user_story.txt"
OUTPUT_PATH = PROJECT_ROOT / "generated_test_cases.json"


def main():
    with open(USER_STORY_PATH, "r", encoding="utf-8") as f:
        user_story = f.read()

    print("Step 1: Analyzing requirement...")
    analysis = analyze_requirement(user_story)

    print("Step 2: Designing scenarios...")
    scenarios = design_scenarios(analysis)

    print("Step 3: Writing test cases...")
    test_cases = write_test_cases(scenarios)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(test_cases.model_dump_json(indent=2))

    print(f"\nGenerated {len(test_cases.test_cases)} test cases:")
    for tc in test_cases.test_cases:
        print(f"  {tc.tc_id} | {tc.type} | {tc.scenario}")

    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
