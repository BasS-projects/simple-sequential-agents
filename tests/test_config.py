from app.config import Settings


def test_settings_ignores_generic_openai_environment(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "outside-key")
    monkeypatch.setenv("TRAVEL_POLICY_LLM_API_KEY", "project-key")

    settings = Settings.from_env()

    assert settings.api_key == "project-key"
