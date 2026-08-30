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

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")

        return cls(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            chat_model=os.getenv("OPENAI_MODEL", "gpt-5.6"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
            knowledge_base_path=Path(os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base.txt")),
            top_k=int(os.getenv("RAG_TOP_K", "3")),
        )
