import re

from app.utils.errors import PromptBlockedError

BLOCKED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\b(nude|naked|nsfw|porn|xxx|sex|hentai)\b",
        r"\b(gore|bloody|mutilation|dismember)\b",
        r"\b(child|minor|underage|kid).{0,20}(nude|naked|sexual|explicit)\b",
        r"\b(terror|bomb|weapon|attack).{0,20}(instruct|make|build|create)\b",
        r"\b(hate|kill|murder).{0,20}(race|ethnic|religion|gender)\b",
    ]
]


def validate_prompt(prompt: str) -> None:
    stripped = prompt.strip()
    if not stripped:
        msg = "Prompt cannot be empty"
        raise PromptBlockedError(msg)

    for pattern in BLOCKED_PATTERNS:
        if pattern.search(stripped):
            raise PromptBlockedError("Prompt contains blocked content")
