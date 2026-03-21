"""CLI entry point for NarrativePulse."""

from __future__ import annotations

import argparse
from pathlib import Path


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
        print(f"Scaffold ready: analysis for {args.file_path} will be added next.")
        return 0

    if args.command == "compare":
        print(
            "Scaffold ready: comparison for "
            f"{args.file_a} vs {args.file_b} will be added next."
        )
        return 0

    parser.error("Unknown command.")
    return 2
