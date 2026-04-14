import pytest

from app.guardrails.prompt_filter import validate_prompt
from app.utils.errors import PromptBlockedError


def test_valid_prompt_passes() -> None:
    # Arrange / Act / Assert — should not raise
    validate_prompt("A beautiful landscape painting in watercolor style")


def test_empty_prompt_blocked() -> None:
    with pytest.raises(PromptBlockedError):
        validate_prompt("")


def test_whitespace_only_prompt_blocked() -> None:
    with pytest.raises(PromptBlockedError):
        validate_prompt("   ")


def test_nsfw_prompt_blocked() -> None:
    with pytest.raises(PromptBlockedError):
        validate_prompt("a nude person standing")


def test_violence_prompt_blocked() -> None:
    with pytest.raises(PromptBlockedError):
        validate_prompt("gore and mutilation scene")


def test_safe_prompt_with_similar_words_passes() -> None:
    # "landscape" contains no blocked terms
    validate_prompt("A golden sunset over a peaceful mountain landscape")
