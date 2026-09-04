from typing import NotRequired, TypedDict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph

from app.config import Settings
from app.rag import PolicyRag


class TravelPolicyState(TypedDict):
    question: str
    retrieved: NotRequired[str]
    answer: NotRequired[str]


def build_travel_policy_graph(settings: Settings):
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.api_key,
        base_url=settings.base_url,
    )
    rag = PolicyRag(settings.knowledge_base_path, embeddings)
    retriever = ChatOpenAI(
        model=settings.chat_model,
        api_key=settings.api_key,
        base_url=settings.base_url,
    )
    formatter = ChatOpenAI(
        model=settings.chat_model,
        api_key=settings.api_key,
        base_url=settings.base_url,
    )

    async def retrieve(state: TravelPolicyState) -> dict[str, str]:
        documents = await rag.search(state["question"], settings.top_k)
        context = "\n\n".join(f"[{doc.title}]\n{doc.content}" for doc in documents)
        response = await retriever.ainvoke(
            [
                (
                    "system",
                    (
                        "Answer only from the supplied travel-policy sections. "
                        "Include the relevant section title in square brackets for every claim. "
                        "If the sections do not answer the question, say that the policy does not specify it."
                    ),
                ),
                ("human", f"Question: {state['question']}\n\nPolicy sections:\n{context}"),
            ]
        )
        return {"retrieved": str(response.content).strip()}

    async def format_answer(state: TravelPolicyState) -> dict[str, str]:
        response = await formatter.ainvoke(
            [
                (
                    "system",
                    (
                        "Turn the supplied retrieval answer into a concise Thai answer for an employee. "
                        "Do not add, remove, or infer policy facts. Preserve all bracketed section citations. "
                        "Use short paragraphs or bullets only when they improve readability."
                    ),
                ),
                (
                    "human",
                    f"คำถาม: {state['question']}\n\nคำตอบจากตัวดึงข้อมูล:\n{state['retrieved']}",
                ),
            ]
        )
        return {"answer": str(response.content).strip()}

    graph = StateGraph(TravelPolicyState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("format", format_answer)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "format")
    graph.add_edge("format", END)
    return graph.compile()
