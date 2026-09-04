from app.config import Settings
from app.graph import build_travel_policy_graph


class TravelPolicyService:
    def __init__(self, settings: Settings) -> None:
        self.graph = build_travel_policy_graph(settings)

    async def answer(self, question: str) -> str:
        result = await self.graph.ainvoke({"question": question})
        return result["answer"]
