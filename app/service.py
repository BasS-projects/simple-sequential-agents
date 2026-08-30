from agents import Runner, set_default_openai_client
from openai import AsyncOpenAI

from app.agents import build_formatter_agent, build_retriever_agent
from app.config import Settings
from app.rag import PolicyRag


class TravelPolicyService:
    def __init__(self, settings: Settings) -> None:
        client = AsyncOpenAI(api_key=settings.api_key, base_url=settings.base_url)
        set_default_openai_client(client, use_for_tracing=False)
        rag = PolicyRag(settings.knowledge_base_path, client, settings.embedding_model)
        self.retriever = build_retriever_agent(rag, settings.chat_model, settings.top_k)
        self.formatter = build_formatter_agent(settings.chat_model)

    async def answer(self, question: str) -> str:
        retrieved = await Runner.run(self.retriever, question)
        formatted = await Runner.run(
            self.formatter,
            f"คำถาม: {question}\n\nคำตอบจากตัวดึงข้อมูล:\n{retrieved.final_output}",
        )
        return formatted.final_output
