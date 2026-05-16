from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from app.prompts.summary import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_TEMPLATE
from app.telemetry.llm import get_llm


def generate_summary(state: dict, config: RunnableConfig) -> dict:
    """Generate an executive summary of the incident response."""
    llm = get_llm(temperature=0.7)

    messages = [
        SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
        HumanMessage(content=SUMMARY_USER_TEMPLATE.format(
            title=state["incident"]["title"],
            category=state["category"],
            severity=state["severity"],
            analysis=state["analysis"],
            root_cause_hypothesis=state["root_cause_hypothesis"],
            mitigation_plan=state["mitigation_plan"],
            recommended_actions=", ".join(state.get("recommended_actions", [])),
            description=state["incident"]["description"],
        )),
    ]

    response = llm.invoke(messages, config=config)

    return {
        "executive_summary": response.content,
    }
