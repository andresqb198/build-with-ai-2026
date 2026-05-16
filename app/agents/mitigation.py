import json
import re

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from app.prompts.mitigation import MITIGATION_SYSTEM_PROMPT, MITIGATION_USER_TEMPLATE
from app.telemetry.llm import get_llm
from app.tools.mitigation_tools import get_runbook, check_circuit_breaker_status


def propose_mitigation(state: dict, config: RunnableConfig) -> dict:
    """Propose mitigation actions based on the analysis."""
    llm = get_llm()

    category = state["category"]
    runbook = get_runbook(category)
    circuit_breaker = check_circuit_breaker_status(state["incident"]["service"])
    iteration = state.get("iteration_count", 0)

    messages = [
        SystemMessage(content=MITIGATION_SYSTEM_PROMPT.format(iteration=iteration)),
        HumanMessage(content=MITIGATION_USER_TEMPLATE.format(
            title=state["incident"]["title"],
            category=category,
            severity=state["severity"],
            analysis=state["analysis"],
            root_cause=state["root_cause_hypothesis"],
            runbook=runbook,
            circuit_breaker=json.dumps(circuit_breaker, indent=2),
        )),
    ]

    response = llm.invoke(messages, config=config)

    # Parse JSON from response
    content = response.content.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    try:
        parsed = json.loads(content)
        mitigation_plan = parsed.get("mitigation_plan", content)
        recommended_actions = parsed.get("recommended_actions", [])
        requires_reanalysis = parsed.get("requires_reanalysis", False)
    except json.JSONDecodeError:
        mitigation_plan = content
        recommended_actions = []
        requires_reanalysis = False

    return {
        "mitigation_plan": mitigation_plan,
        "recommended_actions": recommended_actions,
        "requires_reanalysis": requires_reanalysis,
        "iteration_count": iteration + 1,
    }
