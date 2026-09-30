import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from agent.models import RequirementAnalysis, ScenarioList, TestCaseList, CoverageReview

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"
MAX_ATTEMPTS = 3


def call_model(prompt: str, schema):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
        except errors.ServerError:
            if attempt == MAX_ATTEMPTS:
                raise
            wait_seconds = 2 ** attempt
            print(f"Model server busy (attempt {attempt}/{MAX_ATTEMPTS}) — retrying in {wait_seconds}s...")
            time.sleep(wait_seconds)


def analyze_requirement(user_story: str) -> RequirementAnalysis:
    prompt = f"""You are a senior QA analyst reviewing a user story before test design begins.

Read the user story below and extract:
- The key business flows it describes
- The explicit business rules
- The acceptance criteria as stated
- Anything ambiguous, missing, or unclear that a QA engineer would need clarified before writing test cases

User story:
{user_story}
"""
    response = call_model(prompt, RequirementAnalysis)
    return response.parsed


def design_scenarios(analysis: RequirementAnalysis) -> ScenarioList:
    prompt = f"""You are a Senior QA Analyst who is designing the scenarios

    Based on the RequirementAnalysis
    - Generate a mix of Positive, Negative, Boundary, and Validation scenarios.

Requirement Analysis:
{analysis.model_dump_json(indent=2)}
"""
    response = call_model(prompt, ScenarioList)
    return response.parsed


def write_test_cases(scenarios: ScenarioList) -> TestCaseList:
    prompt = f"""You are a Senior QA Analyst who is about to write down the test cases based on the analysis of the scenarios

    Based on the Scenarios
    - Write down the test cases that include the fields: tc_id, scenario, type, preconditions, test_steps, expected_result, priority

    Scenarios
    {scenarios.model_dump_json(indent=2)}
    """
    response = call_model(prompt, TestCaseList)
    return response.parsed


def review_coverage(analysis: RequirementAnalysis, scenarios: ScenarioList, test_cases: TestCaseList) -> CoverageReview:
    prompt = f"""You are a senior QA lead reviewing a completed test design before release sign-off.

You are given three things: the original requirement analysis, the test scenarios designed from it,
and the final test cases written from those scenarios.

Based on all three:
- Write a coverage summary: which business flows and rules are well covered by the test cases, and call out any gaps.
- Write a risk summary: which areas carry the highest risk if left untested or under-tested, and why.
- Turn the ambiguities/missing info from the requirement analysis into clear, professional questions
  a Business Analyst or Product Owner could directly answer.

Requirement Analysis:
{analysis.model_dump_json(indent=2)}

Test Scenarios:
{scenarios.model_dump_json(indent=2)}

Test Cases:
{test_cases.model_dump_json(indent=2)}
"""
    response = call_model(prompt, CoverageReview)
    return response.parsed
