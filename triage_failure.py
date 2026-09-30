import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"

# Maps a test path back to the agent-generated test case it fulfills, so the
# triage prompt can include what the test was ORIGINALLY supposed to verify.
TEST_TO_TC_ID = {
    "tests/test_empty_login.py::test_empty_login": "TC_LOG_003",
}


def get_expected_result(tc_id):
    with open(PROJECT_ROOT / "generated_test_cases.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for tc in data["test_cases"]:
        if tc["tc_id"] == tc_id:
            return tc["expected_result"]
    return None


def run_test_and_capture(test_path):
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def triage(test_path):
    output = run_test_and_capture(test_path)

    if "FAILED" not in output:
        print("Test passed - nothing to triage.")
        return

    tc_id = TEST_TO_TC_ID.get(test_path)
    expected_result = get_expected_result(tc_id) if tc_id else None

    prompt = f"""You are a senior QA engineer triaging a failed automated test.

Test: {test_path}
{"Original agent-designed expected result: " + expected_result if expected_result else ""}

Raw pytest failure output:
{output}

Based on this, write a short root-cause hypothesis: is this likely a real application bug,
a bug in the test itself (wrong locator, wrong expected value, timing issue), or something else?
Be specific about what in the output supports your conclusion.
"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    print("=== AI Failure Triage ===\n")
    print(response.text)


if __name__ == "__main__":
    triage("tests/test_empty_login.py::test_empty_login")
