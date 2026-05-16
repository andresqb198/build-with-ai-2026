from langfuse.langchain import CallbackHandler
from app.config import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST


def get_langfuse_handler(session_id: str | None = None) -> CallbackHandler:
    """Create a Langfuse CallbackHandler for LangChain/LangGraph tracing."""
    return CallbackHandler(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST,
        session_id=session_id,
    )
