from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GOOGLE_API_KEY, MODEL_NAME


def get_llm(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    """Create a shared Gemini LLM instance."""
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
    )
