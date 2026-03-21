"""Text parsing and normalization layer for NarrativePulse."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

WORD_PATTERN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)
SENTENCE_PATTERN = re.compile(r"[^.!?]+[.!?]?")


@dataclass(frozen=True)
class ParsedDocument:
    """Normalized document representation used by analysis modules."""

    path: Path
    raw_text: str
    paragraphs: list[str]
    sentences: list[str]
    tokens: list[str]

    @property
    def paragraph_count(self) -> int:
        return len(self.paragraphs)

    @property
    def sentence_count(self) -> int:
        return len(self.sentences)

    @property
    def token_count(self) -> int:
        return len(self.tokens)


def read_text(file_path: Path) -> str:
    """Read UTF-8 text from disk with clear user-facing errors."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {file_path}") from exc
    except OSError as exc:
        message = exc.strerror or str(exc)
        raise ValueError(f"Could not read file {file_path}: {message}") from exc


def normalize_token(token: str) -> str:
    """Normalize token for stable counting/comparison."""
    return token.replace("’", "'").lower()


def split_paragraphs(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped:
        return []
    return [part.strip() for part in re.split(r"\n\s*\n+", stripped) if part.strip()]


def split_sentences(text: str) -> list[str]:
    compact = text.replace("\n", " ")
    return [part.strip() for part in SENTENCE_PATTERN.findall(compact) if part.strip()]


def tokenize_words(text: str) -> list[str]:
    return [normalize_token(match.group(0)) for match in WORD_PATTERN.finditer(text)]


def parse_text(text: str, *, path: Path = Path("<memory>")) -> ParsedDocument:
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)
    tokens = tokenize_words(text)
    return ParsedDocument(
        path=path,
        raw_text=text,
        paragraphs=paragraphs,
        sentences=sentences,
        tokens=tokens,
    )


def parse_file(file_path: Path) -> ParsedDocument:
    return parse_text(read_text(file_path), path=file_path)
