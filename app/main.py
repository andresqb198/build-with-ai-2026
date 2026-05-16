"""Punto de entrada CLI para el Sistema de Respuesta a Incidentes de IA."""
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
        title="Incidentes Activos — Panel de Confiabilidad de IA",
        show_lines=True,
    )
    table.add_column("ID", style="bold cyan", width=8)
    table.add_column("Título", width=55)
    table.add_column("Severidad", width=10)
    table.add_column("Servicio", width=28)
    table.add_column("Etiquetas", width=30)

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

    # Clasificación
    console.print(Panel(
        f"[bold]Categoría:[/bold] {result.get('category', 'N/A')}\n"
        f"[bold]Severidad:[/bold] {result.get('severity', 'N/A')}\n"
        f"[bold]Razonamiento:[/bold] {result.get('classification_reasoning', 'N/A')}",
        title="[bold blue]1. Clasificación[/bold blue]",
        border_style="blue",
    ))

    # Análisis
    console.print(Panel(
        result.get("analysis", "Omitido (severidad baja)"),
        title="[bold yellow]2. Análisis de Logs[/bold yellow]",
        border_style="yellow",
    ))

    # Mitigación
    actions = result.get("recommended_actions", [])
    actions_text = "\n".join(f"  - {a}" for a in actions) if actions else "Ninguna"
    iterations = result.get("iteration_count", 1)
    console.print(Panel(
        f"{result.get('mitigation_plan', 'N/A')}\n\n"
        f"[bold]Acciones Recomendadas:[/bold]\n{actions_text}\n\n"
        f"[dim]Iteraciones de análisis: {iterations}[/dim]",
        title="[bold magenta]3. Plan de Mitigación[/bold magenta]",
        border_style="magenta",
    ))

    # Resumen Ejecutivo
    console.print(Panel(
        result.get("executive_summary", "N/A"),
        title="[bold green]4. Resumen Ejecutivo[/bold green]",
        border_style="green",
    ))


def run_incident(incident_id: str) -> None:
    """Run the full incident response graph for a given incident."""
    incidents = load_incidents()
    incident = next((i for i in incidents if i["id"] == incident_id.upper()), None)

    if not incident:
        console.print(f"[red]Incidente {incident_id} no encontrado.[/red]")
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

    console.print(f"\n[bold]Procesando incidente:[/bold] {incident['title']}")
    console.print("[dim]Ejecutando pipeline de agentes... esto puede tomar un momento.[/dim]\n")

    with console.status("[bold green]Agentes trabajando...[/bold green]"):
        result = graph.invoke(
            initial_state,
            config={"callbacks": [handler]},
        )

    display_results(result)

    console.print(f"\n[bold green]Trazas disponibles en:[/bold green] {LANGFUSE_HOST}")
    console.print(f"[dim]ID de sesión: {incident['id']}[/dim]\n")


def main():
    console.print("\n[bold]Sistema de Respuesta a Incidentes de IA[/bold]")
    console.print("[dim]Google Cloud — Equipo de Confiabilidad de IA[/dim]\n")

    incidents = load_incidents()
    display_incidents(incidents)

    console.print()
    choice = console.input("[bold]Ingresa el ID del incidente a investigar (ej. INC-001): [/bold]")

    if not choice.strip():
        console.print("[yellow]Ningún incidente seleccionado. Saliendo.[/yellow]")
        return

    run_incident(choice.strip())


if __name__ == "__main__":
    main()
