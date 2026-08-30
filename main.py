import asyncio
import sys

from app.config import Settings
from app.service import TravelPolicyService


async def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python main.py "คำถามเกี่ยวกับนโยบาย"')

    service = TravelPolicyService(Settings.from_env())
    print(await service.answer(question))


if __name__ == "__main__":
    asyncio.run(main())
