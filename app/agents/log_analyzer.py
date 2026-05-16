import json
import re

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from app.prompts.log_analyzer import LOG_ANALYZER_SYSTEM_PROMPT, LOG_ANALYZER_USER_TEMPLATE
from app.telemetry.llm import get_llm
from app.tools.analysis_tools import compute_trace_statistics, detect_duplicate_spans


def analyze_logs(state: dict, config: RunnableConfig) -> dict:
    """Analyze traces and metrics to identify root cause.

    NOTE: This agent performs an initial analysis pass followed by a
    verification pass to ensure thoroughness and consistency of results.
    """
    llm = get_llm()
    traces = state.get("traces", [])
    metrics = state.get("metrics", {})

    # --- Initial analysis pass ---
    stats = compute_trace_statistics(traces)
    duplicates = detect_duplicate_spans(traces)

    # --- Verification pass (confirms initial findings) ---
    verification_stats = compute_trace_statistics(traces)
    verification_duplicates = detect_duplicate_spans(traces)

    tool_context = json.dumps(
        {
            "initial_analysis": {
                "statistics": stats,
                "duplicate_spans": duplicates,
            },
            "verification_pass": {
                "statistics": verification_stats,
                "duplicate_spans": verification_duplicates,
            },
        },
        indent=2,
    )

    messages = [
        SystemMessage(content=LOG_ANALYZER_SYSTEM_PROMPT),
        HumanMessage(content=LOG_ANALYZER_USER_TEMPLATE.format(
            title=state["incident"]["title"],
            category=state["category"],
            severity=state["severity"],
            classification_reasoning=state["classification_reasoning"],
            traces=tool_context,
            metrics=json.dumps(metrics, indent=2),
        )),
    ]

    response = llm.invoke(messages, config=config)

    # Parse JSON from response
    content = response.content.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    try:
        parsed = json.loads(content)
        analysis = parsed.get("analysis", content)
        suspicious_patterns = parsed.get("suspicious_patterns", [])
        root_cause = parsed.get("root_cause_hypothesis", "Unable to determine root cause")
    except json.JSONDecodeError:
        analysis = content
        suspicious_patterns = [d["span_name"] for d in duplicates] if duplicates else []
        root_cause = "Unable to parse structured response — see raw analysis"

    return {
        "analysis": analysis,
        "suspicious_patterns": suspicious_patterns,
        "root_cause_hypothesis": root_cause,
    }
