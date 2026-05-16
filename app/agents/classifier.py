import json
import re

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from app.prompts.classifier import CLASSIFIER_SYSTEM_PROMPT, CLASSIFIER_USER_TEMPLATE
from app.telemetry.llm import get_llm


def classify_incident(state: dict, config: RunnableConfig) -> dict:
    """Classify an incident by category and severity using the LLM."""
    llm = get_llm()
    incident = state["incident"]

    messages = [
        SystemMessage(content=CLASSIFIER_SYSTEM_PROMPT),
        HumanMessage(content=CLASSIFIER_USER_TEMPLATE.format(
            incident_id=incident["id"],
            title=incident["title"],
            description=incident["description"],
            service=incident["service"],
            reported_severity=incident["severity"],
            tags=", ".join(incident.get("tags", [])),
            timestamp=incident["timestamp"],
        )),
    ]

    response = llm.invoke(messages, config=config)

    # Parse JSON from response, stripping markdown fences if present
    content = response.content.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    parsed = json.loads(content)

    return {
        "category": parsed["category"],
        "severity": parsed["severity"],
        "classification_reasoning": parsed["reasoning"],
    }
