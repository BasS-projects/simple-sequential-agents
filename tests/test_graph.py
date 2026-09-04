from pathlib import Path

from app.config import Settings
from app.graph import build_travel_policy_graph


def test_graph_has_a_fixed_retrieve_then_format_path() -> None:
    settings = Settings(
        api_key="test-key",
        base_url="https://example.test/v1",
        chat_model="test-model",
        embedding_model="test-embedding",
        knowledge_base_path=Path("knowledge_base.txt"),
        top_k=2,
        app_api_key=None,
        api_host="127.0.0.1",
        api_port=8000,
    )

    graph = build_travel_policy_graph(settings).get_graph()
    edges = {(edge.source, edge.target) for edge in graph.edges}

    assert ("__start__", "retrieve") in edges
    assert ("retrieve", "format") in edges
    assert ("format", "__end__") in edges
