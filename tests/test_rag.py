import pytest

from app.rag import cosine_similarity, split_sections


def test_split_sections_uses_numbered_policy_headings() -> None:
    documents = split_sections("""นโยบาย\n\n1. การอนุมัติ\nขออนุมัติก่อนเดินทาง\n\n2. ค่าใช้จ่าย\nเบิกได้ตามนโยบาย""")

    assert [document.title for document in documents] == ["1. การอนุมัติ", "2. ค่าใช้จ่าย"]
    assert documents[1].content == "เบิกได้ตามนโยบาย"


def test_cosine_similarity_matches_identical_vectors() -> None:
    assert cosine_similarity([1.0, 2.0], [1.0, 2.0]) == pytest.approx(1.0)
