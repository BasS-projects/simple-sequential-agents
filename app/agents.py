from agents import Agent, function_tool

from app.rag import PolicyRag


def build_retriever_agent(rag: PolicyRag, model: str, top_k: int) -> Agent:
    @function_tool
    async def search_policy(query: str) -> str:
        """Search the travel policy and return the most relevant numbered sections."""
        documents = await rag.search(query, top_k)
        return "\n\n".join(f"[{doc.title}]\n{doc.content}" for doc in documents)

    return Agent(
        name="Travel Policy Retriever",
        model=model,
        instructions=(
            "Answer travel-policy questions using only the knowledge-base sections. "
            "Always call search_policy before answering. "
            "If the returned sections do not answer the question, say that the policy does not specify it. "
            "Include the relevant section title in square brackets for every claim."
        ),
        tools=[search_policy],
    )


def build_formatter_agent(model: str) -> Agent:
    return Agent(
        name="Travel Policy Formatter",
        model=model,
        instructions=(
            "Turn the supplied retrieval answer into a concise Thai answer for an employee. "
            "Do not add, remove, or infer policy facts. Preserve all bracketed section citations. "
            "Use short paragraphs or bullets only when they improve readability."
        ),
    )
