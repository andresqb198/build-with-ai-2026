"""CLI entry point for the AI Incident Response System."""
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from app.tools.incident_tools import load_incidents, load_traces_for_incident, load_metrics_for_incident
from app.telemetry import get_langfuse_handler
from app.graphs.incident_graph import build_incident_graph
from app.config import LANGFUSE_HOST

console = Console()


def display_incidents(incidents: list[dict]) -> None:
    """Display all incidents in a formatted table."""
    table = Table(
        title="Active Incidents — AI Reliability Dashboard",
        show_lines=True,
    )
    table.add_column("ID", style="bold cyan", width=8)
    table.add_column("Title", width=55)
    table.add_column("Severity", width=10)
    table.add_column("Service", width=28)
    table.add_column("Tags", width=30)

    severity_colors = {
        "critical": "bold red",
        "high": "red",
        "medium": "yellow",
        "low": "green",
    }

    for inc in incidents:
        sev = inc["severity"]
        table.add_row(
            inc["id"],
            inc["title"],
            f"[{severity_colors.get(sev, 'white')}]{sev}[/]",
            inc["service"],
            ", ".join(inc.get("tags", [])),
        )

    console.print(table)


def display_results(result: dict) -> None:
    """Display the pipeline results in formatted panels."""
    console.print()

    # Classification
    console.print(Panel(
        f"[bold]Category:[/bold] {result.get('category', 'N/A')}\n"
        f"[bold]Severity:[/bold] {result.get('severity', 'N/A')}\n"
        f"[bold]Reasoning:[/bold] {result.get('classification_reasoning', 'N/A')}",
        title="[bold blue]1. Classification[/bold blue]",
        border_style="blue",
    ))

    # Analysis
    console.print(Panel(
        result.get("analysis", "Skipped (low severity)"),
        title="[bold yellow]2. Log Analysis[/bold yellow]",
        border_style="yellow",
    ))

    # Mitigation
    actions = result.get("recommended_actions", [])
    actions_text = "\n".join(f"  - {a}" for a in actions) if actions else "None"
    iterations = result.get("iteration_count", 1)
    console.print(Panel(
        f"{result.get('mitigation_plan', 'N/A')}\n\n"
        f"[bold]Recommended Actions:[/bold]\n{actions_text}\n\n"
        f"[dim]Analysis iterations: {iterations}[/dim]",
        title="[bold magenta]3. Mitigation Plan[/bold magenta]",
        border_style="magenta",
    ))

    # Executive Summary
    console.print(Panel(
        result.get("executive_summary", "N/A"),
        title="[bold green]4. Executive Summary[/bold green]",
        border_style="green",
    ))


def run_incident(incident_id: str) -> None:
    """Run the full incident response graph for a given incident."""
    incidents = load_incidents()
    incident = next((i for i in incidents if i["id"] == incident_id.upper()), None)

    if not incident:
        console.print(f"[red]Incident {incident_id} not found.[/red]")
        return

    traces = load_traces_for_incident(incident["id"])
    metrics = load_metrics_for_incident(incident["id"])
    handler = get_langfuse_handler(session_id=incident["id"])

    graph = build_incident_graph()

    initial_state = {
        "incident_id": incident["id"],
        "incident": incident,
        "traces": traces,
        "metrics": metrics or {},
        "iteration_count": 0,
        "max_iterations": 3,
    }

    console.print(f"\n[bold]Processing incident:[/bold] {incident['title']}")
    console.print("[dim]Running agent pipeline... this may take a moment.[/dim]\n")

    with console.status("[bold green]Agents working...[/bold green]"):
        result = graph.invoke(
            initial_state,
            config={"callbacks": [handler]},
        )

    display_results(result)

    console.print(f"\n[bold green]Traces available at:[/bold green] {LANGFUSE_HOST}")
    console.print(f"[dim]Session ID: {incident['id']}[/dim]\n")


def main():
    console.print("\n[bold]AI Incident Response System[/bold]")
    console.print("[dim]Google Cloud — AI Reliability Team[/dim]\n")

    incidents = load_incidents()
    display_incidents(incidents)

    console.print()
    choice = console.input("[bold]Enter incident ID to investigate (e.g. INC-001): [/bold]")

    if not choice.strip():
        console.print("[yellow]No incident selected. Exiting.[/yellow]")
        return

    run_incident(choice.strip())


if __name__ == "__main__":
    main()
