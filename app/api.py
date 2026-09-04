from time import time
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config import Settings
from app.service import TravelPolicyService


class ChatMessage(BaseModel):
    role: Literal["system", "developer", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: bool = False


def error_response(message: str, error_type: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"message": message, "type": error_type, "param": None, "code": None}},
    )


def create_app(
    settings: Settings,
    service: TravelPolicyService | None = None,
) -> FastAPI:
    app = FastAPI(title="Travel Policy API")
    policy_service = service or TravelPolicyService(settings)

    @app.exception_handler(Exception)
    async def unhandled_error(_: Request, __: Exception) -> JSONResponse:
        return error_response("Unable to process the request", "server_error", 500)

    @app.middleware("http")
    async def require_api_key(request: Request, call_next):
        if (
            settings.app_api_key
            and request.url.path.startswith("/v1/")
            and request.headers.get("authorization") != f"Bearer {settings.app_api_key}"
        ):
            return error_response("Invalid API key", "authentication_error", 401)
        return await call_next(request)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/v1/models")
    async def list_models() -> dict[str, object]:
        return {
            "object": "list",
            "data": [{"id": settings.chat_model, "object": "model", "owned_by": "travel-policy"}],
        }

    @app.post("/v1/chat/completions")
    async def chat_completions(payload: ChatCompletionRequest) -> JSONResponse:
        if payload.stream:
            return error_response("Streaming is not supported", "invalid_request_error", 400)

        question = next(
            (message.content for message in reversed(payload.messages) if message.role == "user"),
            None,
        )
        if not question:
            return error_response("A user message is required", "invalid_request_error", 400)

        answer = await policy_service.answer(question)

        return JSONResponse(
            content={
                "id": f"chatcmpl-{uuid4().hex}",
                "object": "chat.completion",
                "created": int(time()),
                "model": settings.chat_model,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": answer, "refusal": None},
                        "finish_reason": "stop",
                    }
                ],
            }
        )

    return app
