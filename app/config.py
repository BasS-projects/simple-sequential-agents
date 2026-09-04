import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    chat_model: str
    embedding_model: str
    knowledge_base_path: Path
    top_k: int
    app_api_key: str | None
    api_host: str
    api_port: int

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        api_key = os.getenv("TRAVEL_POLICY_LLM_API_KEY")
        if not api_key:
            raise ValueError("TRAVEL_POLICY_LLM_API_KEY is required")

        return cls(
            api_key=api_key,
            base_url=os.getenv("TRAVEL_POLICY_LLM_BASE_URL", "https://api.openai.com/v1"),
            chat_model=os.getenv("TRAVEL_POLICY_LLM_MODEL", "gpt-5.6"),
            embedding_model=os.getenv(
                "TRAVEL_POLICY_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
            knowledge_base_path=Path(
                os.getenv("TRAVEL_POLICY_KNOWLEDGE_BASE_PATH", "knowledge_base.txt")
            ),
            top_k=int(os.getenv("TRAVEL_POLICY_RAG_TOP_K", "3")),
            app_api_key=os.getenv("TRAVEL_POLICY_APP_API_KEY") or None,
            api_host=os.getenv("TRAVEL_POLICY_API_HOST", "127.0.0.1"),
            api_port=int(os.getenv("TRAVEL_POLICY_API_PORT", "8000")),
        )
