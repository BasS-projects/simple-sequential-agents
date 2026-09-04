from pathlib import Path

from fastapi.testclient import TestClient

from app.api import create_app
from app.config import Settings


class FakeService:
    async def answer(self, question: str) -> str:
        return f"คำตอบสำหรับ: {question}"


def settings(app_api_key: str | None = None) -> Settings:
    return Settings(
        api_key="test-key",
        base_url="https://example.test/v1",
        chat_model="test-model",
        embedding_model="test-embedding",
        knowledge_base_path=Path("knowledge_base.txt"),
        top_k=2,
        app_api_key=app_api_key,
        api_host="127.0.0.1",
        api_port=8000,
    )


def test_chat_completions_returns_an_openai_compatible_response() -> None:
    client = TestClient(create_app(settings(), FakeService()))

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "requested-model",
            "messages": [{"role": "user", "content": "เบิกค่าอะไรได้บ้าง"}],
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["object"] == "chat.completion"
    assert body["model"] == "test-model"
    assert body["choices"][0]["message"]["content"] == "คำตอบสำหรับ: เบิกค่าอะไรได้บ้าง"


def test_chat_completions_requires_the_configured_bearer_key() -> None:
    client = TestClient(create_app(settings("client-key"), FakeService()))
    payload = {"model": "test-model", "messages": [{"role": "user", "content": "test"}]}

    denied = client.post("/v1/chat/completions", json=payload)
    allowed = client.post(
        "/v1/chat/completions",
        json=payload,
        headers={"Authorization": "Bearer client-key"},
    )

    assert denied.status_code == 401
    assert denied.json()["error"]["type"] == "authentication_error"
    assert allowed.status_code == 200
