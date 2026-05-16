import json
from app.config import DATASETS_DIR


def load_incidents() -> list[dict]:
    """Load all incidents from the local dataset."""
    with open(DATASETS_DIR / "incidents.json") as f:
        return json.load(f)


def get_incident_by_id(incident_id: str) -> dict | None:
    """Get a single incident by its ID."""
    for incident in load_incidents():
        if incident["id"] == incident_id:
            return incident
    return None


def load_traces_for_incident(incident_id: str) -> list[dict]:
    """Load trace data for a specific incident."""
    with open(DATASETS_DIR / "traces.json") as f:
        all_traces = json.load(f)
    for entry in all_traces:
        if entry["incident_id"] == incident_id:
            return entry["traces"]
    return []


def load_metrics_for_incident(incident_id: str) -> dict | None:
    """Load metrics for a specific incident."""
    with open(DATASETS_DIR / "metrics.json") as f:
        all_metrics = json.load(f)
    for entry in all_metrics:
        if entry["incident_id"] == incident_id:
            return entry
    return None
