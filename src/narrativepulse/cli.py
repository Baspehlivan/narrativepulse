"""CLI entry point for NarrativePulse."""

from __future__ import annotations

import argparse
from pathlib import Path

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


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        try:
            parsed = parse_file(args.file_path)
        except ValueError as exc:
            parser.error(str(exc))

        print(f"Parsed file: {parsed.path}")
        print(f"Paragraphs: {parsed.paragraph_count}")
        print(f"Sentences: {parsed.sentence_count}")
        print(f"Tokens: {parsed.token_count}")
        return 0

    if args.command == "compare":
        try:
            parsed_a = parse_file(args.file_a)
            parsed_b = parse_file(args.file_b)
        except ValueError as exc:
            parser.error(str(exc))

        print("Parsed both files successfully.")
        print(f"A tokens: {parsed_a.token_count}")
        print(f"B tokens: {parsed_b.token_count}")
        return 0

    parser.error("Unknown command.")
    return 2
