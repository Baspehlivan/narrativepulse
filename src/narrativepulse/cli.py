"""CLI entry point for NarrativePulse."""

from __future__ import annotations

import argparse
from pathlib import Path

from narrativepulse.metrics import (
    ComparisonMetrics,
    DocumentMetrics,
    analyze_document,
    compare_documents,
)
from narrativepulse.parser import ParsedDocument, parse_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="narrativepulse",
        description="Analyze and compare writing style across text files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze a single text file.")
    analyze.add_argument("file_path", type=Path)
    analyze.add_argument("--top", type=int, default=10)

    compare = subparsers.add_parser("compare", help="Compare two text files.")
    compare.add_argument("file_a", type=Path)
    compare.add_argument("file_b", type=Path)
    compare.add_argument("--top", type=int, default=10)

    return parser


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def _rule() -> None:
    print("=" * 72)


def _similarity_label(score: float) -> str:
    if score >= 0.90:
        return "very high"
    if score >= 0.75:
        return "high"
    if score >= 0.55:
        return "medium"
    return "low"


def _print_analyze_report(parsed: ParsedDocument, metrics: DocumentMetrics) -> None:
    _rule()
    print(f"NarrativePulse report for: {parsed.path}")
    print(
        "document_stats: "
        f"paragraphs={parsed.paragraph_count}, "
        f"sentences={parsed.sentence_count}, "
        f"tokens={parsed.token_count}"
    )
    print()
    print("core_metrics:")
    print(f"- lexical_diversity:  {_fmt(metrics.lexical_diversity)}")
    print(f"- sentence_rhythm:    {_fmt(metrics.sentence_rhythm)}")
    print(f"- dialogue_ratio:     {_fmt(metrics.dialogue_ratio)}")
    print(f"- avg_sentence_length:{_fmt(metrics.avg_sentence_length)}")
    print(
        "- style_signature: ["
        + ", ".join(_fmt(item) for item in metrics.style_signature)
        + "]"
    )

    print()
    print("repetition_hotspots:")
    if not metrics.top_bigrams and not metrics.top_trigrams:
        print("- none")
        _rule()
        return

    if metrics.top_bigrams:
        print("- bigrams:")
    for hotspot in metrics.top_bigrams:
        print(f"  - \"{hotspot.phrase}\" x{hotspot.count}")

    if metrics.top_trigrams:
        print("- trigrams:")
    for hotspot in metrics.top_trigrams:
        print(f"  - \"{hotspot.phrase}\" x{hotspot.count}")

    _rule()


def _print_compare_header(
    parsed_a: ParsedDocument,
    parsed_b: ParsedDocument,
    comparison: ComparisonMetrics,
) -> None:
    score = comparison.style_similarity
    metrics_a = comparison.metrics_a
    metrics_b = comparison.metrics_b

    _rule()
    print("NarrativePulse compare report")
    print(
        f"style_similarity: {_fmt(score)} "
        f"({_similarity_label(score)})"
    )
    print(f"A: {parsed_a.path}")
    print(f"B: {parsed_b.path}")
    print()
    print("metric_deltas (A - B):")
    print(
        "- lexical_diversity:  "
        f"{_fmt(metrics_a.lexical_diversity - metrics_b.lexical_diversity)}"
    )
    print(
        "- sentence_rhythm:    "
        f"{_fmt(metrics_a.sentence_rhythm - metrics_b.sentence_rhythm)}"
    )
    print(
        "- dialogue_ratio:     "
        f"{_fmt(metrics_a.dialogue_ratio - metrics_b.dialogue_ratio)}"
    )
    print(
        "- avg_sentence_length:"
        f"{_fmt(metrics_a.avg_sentence_length - metrics_b.avg_sentence_length)}"
    )
    print()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        try:
            parsed = parse_file(args.file_path)
        except ValueError as exc:
            parser.error(str(exc))

        metrics = analyze_document(parsed, top=args.top)
        _print_analyze_report(parsed, metrics)
        return 0

    if args.command == "compare":
        try:
            parsed_a = parse_file(args.file_a)
            parsed_b = parse_file(args.file_b)
        except ValueError as exc:
            parser.error(str(exc))

        comparison = compare_documents(parsed_a, parsed_b, top=args.top)
        metrics_a = comparison.metrics_a
        metrics_b = comparison.metrics_b

        _print_compare_header(parsed_a, parsed_b, comparison)
        _print_analyze_report(parsed_a, metrics_a)
        print()
        _print_analyze_report(parsed_b, metrics_b)
        return 0

    parser.error("Unknown command.")
    return 2
