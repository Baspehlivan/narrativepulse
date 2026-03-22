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
from narrativepulse.parser import parse_file


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


def _similarity_label(score: float) -> str:
    if score >= 0.90:
        return "very high"
    if score >= 0.75:
        return "high"
    if score >= 0.55:
        return "medium"
    return "low"


def _print_analyze_report(file_path: Path, metrics: DocumentMetrics) -> None:
    print(f"NarrativePulse report for: {file_path}")
    print(f"- lexical_diversity: {_fmt(metrics.lexical_diversity)}")
    print(f"- sentence_rhythm: {_fmt(metrics.sentence_rhythm)}")
    print(f"- dialogue_ratio: {_fmt(metrics.dialogue_ratio)}")
    print(f"- avg_sentence_length: {_fmt(metrics.avg_sentence_length)}")
    print(
        "- style_signature: ["
        + ", ".join(_fmt(item) for item in metrics.style_signature)
        + "]"
    )

    print("repetition_hotspots:")
    if not metrics.top_bigrams and not metrics.top_trigrams:
        print("- none")
        return

    for hotspot in metrics.top_bigrams:
        print(f"- [{hotspot.n}-gram] \"{hotspot.phrase}\" x{hotspot.count}")
    for hotspot in metrics.top_trigrams:
        print(f"- [{hotspot.n}-gram] \"{hotspot.phrase}\" x{hotspot.count}")


def _print_compare_header(comparison: ComparisonMetrics) -> None:
    score = comparison.style_similarity
    print("NarrativePulse compare report")
    print(
        f"style_similarity: {_fmt(score)} "
        f"({_similarity_label(score)})"
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
        _print_analyze_report(parsed.path, metrics)
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

        _print_compare_header(comparison)
        _print_analyze_report(parsed_a.path, metrics_a)
        print()
        _print_analyze_report(parsed_b.path, metrics_b)
        return 0

    parser.error("Unknown command.")
    return 2
