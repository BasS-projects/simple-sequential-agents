import uvicorn

from app.api import create_app
from app.config import Settings


def main() -> None:
    settings = Settings.from_env()
    uvicorn.run(create_app(settings), host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()
