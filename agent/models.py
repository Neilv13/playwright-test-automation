from pydantic import BaseModel


class BusinessFlow(BaseModel):
    name: str
    description: str


class RequirementAnalysis(BaseModel):
    business_flows: list[BusinessFlow]
    business_rules: list[str]
    acceptance_criteria: list[str]
    ambiguities_or_missing_info: list[str]


class Scenario(BaseModel):
    title: str
    type: str
    description: str


class ScenarioList(BaseModel):
    scenarios: list[Scenario]


class TestCase(BaseModel):
    tc_id: str
    scenario: str
    type: str
    preconditions: str
    test_steps: str
    expected_result: str
    priority: str


class TestCaseList(BaseModel):
    test_cases: list[TestCase]


class CoverageReview(BaseModel):
    coverage_summary: str
    risk_summary: str
    clarifying_questions: list[str]
