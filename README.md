# NarrativePulse

NarrativePulse is my final project for an introductory Python course.
It is a small CLI tool that analyzes writing style from plain text files and compares two documents.

## What it does

- `analyze <file>`: prints style metrics for one document
- `compare <file_a> <file_b>`: computes a style similarity score and shows metric deltas
- Finds repeated bigrams/trigrams as simple repetition hotspots

## Metrics

- `lexical_diversity`: unique tokens / all tokens
- `sentence_rhythm`: variation in sentence lengths (coefficient of variation)
- `dialogue_ratio`: share of sentences containing quote characters
- `avg_sentence_length`: average token count per sentence
- `style_signature`: compact 4-value vector used for comparison
- `style_similarity`: cosine similarity between two style signatures

## How it works (briefly)

1. Read UTF-8 `.txt` / `.md` files.
2. Split into paragraphs, sentences, and normalized tokens.
3. Compute the metrics above.
4. For comparison mode, calculate cosine similarity from the two signatures.

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

## Example output (shortened)

```text
NarrativePulse compare report
style_similarity: 0.9973 (very high)
...
metric_deltas (A - B):
- lexical_diversity:  0.0252
- sentence_rhythm:    -0.0428
```

## Limitations

- This is a rule-based project, not a deep NLP model.
- Sentence splitting is punctuation-based (`.`, `!`, `?`), so edge cases exist.
- Dialogue detection is quote-marker based.
- Very short texts can produce unstable similarity scores.

## Run Tests

```bash
python3 -m unittest discover -s tests
```
