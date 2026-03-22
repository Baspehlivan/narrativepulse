"""Core style metrics for NarrativePulse."""

from __future__ import annotations

from math import sqrt
from collections import Counter
from dataclasses import dataclass
from statistics import pstdev

from narrativepulse.parser import ParsedDocument, tokenize_words


@dataclass(frozen=True)
class Hotspot:
    phrase: str
    count: int
    n: int


@dataclass(frozen=True)
class DocumentMetrics:
    lexical_diversity: float
    sentence_rhythm: float
    dialogue_ratio: float
    avg_sentence_length: float
    style_signature: tuple[float, float, float, float]
    top_bigrams: list[Hotspot]
    top_trigrams: list[Hotspot]


@dataclass(frozen=True)
class ComparisonMetrics:
    metrics_a: DocumentMetrics
    metrics_b: DocumentMetrics
    style_similarity: float


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def sentence_lengths(document: ParsedDocument) -> list[int]:
    lengths: list[int] = []
    for sentence in document.sentences:
        count = len(tokenize_words(sentence))
        if count > 0:
            lengths.append(count)
    return lengths


def lexical_diversity(tokens: list[str]) -> float:
    return _safe_div(len(set(tokens)), len(tokens))


def sentence_rhythm(lengths: list[int]) -> float:
    if not lengths:
        return 0.0
    mean_length = _safe_div(sum(lengths), len(lengths))
    if mean_length == 0:
        return 0.0
    return _safe_div(pstdev(lengths), mean_length)


def dialogue_ratio(sentences: list[str]) -> float:
    if not sentences:
        return 0.0

    markers = ('"', "“", "”")
    dialogue_sentences = 0
    for sentence in sentences:
        if any(marker in sentence for marker in markers):
            dialogue_sentences += 1
    return _safe_div(dialogue_sentences, len(sentences))


def _top_ngrams(tokens: list[str], n: int, top: int) -> list[Hotspot]:
    if top <= 0 or len(tokens) < n:
        return []

    ngram_counts: Counter[tuple[str, ...]] = Counter(
        tuple(tokens[index : index + n])
        for index in range(len(tokens) - n + 1)
    )

    repeated = [
        (ngram, count)
        for ngram, count in ngram_counts.items()
        if count >= 2
    ]
    repeated.sort(key=lambda item: (-item[1], item[0]))

    return [
        Hotspot(phrase=" ".join(ngram), count=count, n=n)
        for ngram, count in repeated[:top]
    ]


def analyze_document(document: ParsedDocument, *, top: int = 10) -> DocumentMetrics:
    lengths = sentence_lengths(document)
    lex = lexical_diversity(document.tokens)
    rhythm = sentence_rhythm(lengths)
    dialog = dialogue_ratio(document.sentences)
    avg_sentence_len = _safe_div(sum(lengths), len(lengths))

    signature = (lex, rhythm, dialog, avg_sentence_len)
    return DocumentMetrics(
        lexical_diversity=lex,
        sentence_rhythm=rhythm,
        dialogue_ratio=dialog,
        avg_sentence_length=avg_sentence_len,
        style_signature=signature,
        top_bigrams=_top_ngrams(document.tokens, n=2, top=top),
        top_trigrams=_top_ngrams(document.tokens, n=3, top=top),
    )


def cosine_similarity(
    vector_a: tuple[float, ...],
    vector_b: tuple[float, ...],
) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have equal length for cosine similarity.")

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = sqrt(sum(a * a for a in vector_a))
    norm_b = sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def compare_documents(
    document_a: ParsedDocument,
    document_b: ParsedDocument,
    *,
    top: int = 10,
) -> ComparisonMetrics:
    metrics_a = analyze_document(document_a, top=top)
    metrics_b = analyze_document(document_b, top=top)
    similarity = cosine_similarity(
        metrics_a.style_signature,
        metrics_b.style_signature,
    )
    return ComparisonMetrics(
        metrics_a=metrics_a,
        metrics_b=metrics_b,
        style_similarity=similarity,
    )
