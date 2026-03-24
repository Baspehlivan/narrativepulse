# NarrativePulse

NarrativePulse is a Python CLI package for analyzing writing style in text files and comparing two documents.

## Features

- Analyze one text (`.txt` or `.md`) and report style metrics.
- Compare two texts and compute a style similarity score.
- Show repeated bigrams/trigrams as repetition hotspots.

## Metrics

- `lexical_diversity`
- `sentence_rhythm`
- `dialogue_ratio`
- `avg_sentence_length`
- `style_signature`
- `style_similarity` (for compare mode)

## Installation

```bash
uv pip install -e .
```

## Run

```bash
uv run -m narrativepulse --help
```

Analyze one document:

```bash
uv run -m narrativepulse analyze examples/sample_a.txt --top 5
```

Compare two documents:

```bash
uv run -m narrativepulse compare examples/sample_a.txt examples/sample_b.txt --top 5
```

## Run Tests

```bash
python3 -m unittest discover -s tests
```
