from typing import TypedDict, Literal


IncidentCategory = Literal[
    "hallucination", "latency", "security", "cost",
    "tool_misuse", "infrastructure", "unknown",
]

IncidentSeverity = Literal["critical", "high", "medium", "low"]


class IncidentState(TypedDict, total=False):
    # Input
    incident_id: str
    incident: dict
    traces: list[dict]
    metrics: dict

    # Classifier output
    category: IncidentCategory
    severity: IncidentSeverity
    classification_reasoning: str

    # Log analyzer output
    analysis: str
    suspicious_patterns: list[str]
    root_cause_hypothesis: str

    # Mitigation output
    mitigation_plan: str
    recommended_actions: list[str]
    requires_reanalysis: bool

    # Summary output
    executive_summary: str

    # Control flow
    iteration_count: int
    max_iterations: int
