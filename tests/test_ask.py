from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=34),
        text="回答",
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            assert kwargs["contents"] == "質問"
            return response

    class FakeClient:
        models = FakeModels()

        def __init__(self, api_key):
            pass

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答"
    assert capsys.readouterr().out.strip() == "[usage] input=12 output=34"