import os
import uuid

from langfuse.langchain import CallbackHandler
from app.config import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST


def _incident_to_trace_id(incident_id: str) -> str:
    """Convert an incident ID to a deterministic 32-char hex UUID."""
    return uuid.uuid5(uuid.NAMESPACE_DNS, incident_id).hex


def get_langfuse_handler(session_id: str | None = None) -> CallbackHandler:
    """Create a Langfuse CallbackHandler for LangChain/LangGraph tracing."""
    os.environ.setdefault("LANGFUSE_PUBLIC_KEY", LANGFUSE_PUBLIC_KEY)
    os.environ.setdefault("LANGFUSE_SECRET_KEY", LANGFUSE_SECRET_KEY)
    os.environ.setdefault("LANGFUSE_HOST", LANGFUSE_HOST)
    trace_context = {"trace_id": _incident_to_trace_id(session_id)} if session_id else None
    return CallbackHandler(trace_context=trace_context)
