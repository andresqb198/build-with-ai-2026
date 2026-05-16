from langgraph.graph import StateGraph, START, END

from app.graphs.state import IncidentState
from app.agents.classifier import classify_incident
from app.agents.log_analyzer import analyze_logs
from app.agents.mitigation import propose_mitigation
from app.agents.summary import generate_summary


def severity_routing(state: IncidentState) -> str:
    """Route based on severity: skip deep analysis for low-severity incidents."""
    if state.get("severity") == "low":
        return "propose_mitigation"
    return "analyze_logs"


def should_reanalyze(state: IncidentState) -> str:
    """Check if mitigation agent requested reanalysis (loop guard at max_iterations)."""
    max_iter = state.get("max_iterations", 3)
    if state.get("requires_reanalysis") and state.get("iteration_count", 0) < max_iter:
        return "analyze_logs"
    return "generate_summary"


def build_incident_graph() -> StateGraph:
    """Build and compile the incident response LangGraph."""
    graph = StateGraph(IncidentState)

    # Register nodes
    graph.add_node("classify_incident", classify_incident)
    graph.add_node("analyze_logs", analyze_logs)
    graph.add_node("propose_mitigation", propose_mitigation)
    graph.add_node("generate_summary", generate_summary)

    # Entry point
    graph.add_edge(START, "classify_incident")

    # Classifier → severity-based routing
    graph.add_conditional_edges(
        "classify_incident",
        severity_routing,
        {"analyze_logs": "analyze_logs", "propose_mitigation": "propose_mitigation"},
    )

    # Log analysis → mitigation
    graph.add_edge("analyze_logs", "propose_mitigation")

    # Mitigation → reanalysis loop OR summary
    graph.add_conditional_edges(
        "propose_mitigation",
        should_reanalyze,
        {"analyze_logs": "analyze_logs", "generate_summary": "generate_summary"},
    )

    # Summary → end
    graph.add_edge("generate_summary", END)

    return graph.compile()
