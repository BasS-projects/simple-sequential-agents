import re
from dataclasses import dataclass
from math import sqrt
from pathlib import Path

from openai import AsyncOpenAI


@dataclass(frozen=True)
class Document:
    title: str
    content: str


def split_sections(text: str) -> list[Document]:
    sections = re.split(r"(?=^\d+\.\s)", text, flags=re.MULTILINE)
    documents = []

    for section in sections:
        lines = section.strip().splitlines()
        if not lines or not re.match(r"^\d+\.\s", lines[0]):
            continue
        documents.append(Document(title=lines[0], content="\n".join(lines[1:]).strip()))

    if not documents:
        raise ValueError("knowledge base must contain numbered sections")
    return documents


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_size = sqrt(sum(value * value for value in left))
    right_size = sqrt(sum(value * value for value in right))
    return numerator / (left_size * right_size) if left_size and right_size else 0.0


class PolicyRag:
    def __init__(self, path: Path, client: AsyncOpenAI, embedding_model: str) -> None:
        self.documents = split_sections(path.read_text(encoding="utf-8"))
        self.client = client
        self.embedding_model = embedding_model
        self.document_embeddings: list[list[float]] | None = None

    async def search(self, query: str, top_k: int) -> list[Document]:
        if self.document_embeddings is None:
            self.document_embeddings = await self._embed([doc.content for doc in self.documents])

        query_embedding = (await self._embed([query]))[0]
        ranked = sorted(
            zip(self.documents, self.document_embeddings, strict=True),
            key=lambda item: cosine_similarity(query_embedding, item[1]),
            reverse=True,
        )
        return [document for document, _ in ranked[:top_k]]

    async def _embed(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(model=self.embedding_model, input=texts)
        return [item.embedding for item in response.data]
