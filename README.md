# AI201-Project4

## Overview

**Video Walkthrough:** [Link To Video](https://www.loom.com/share/7e969bb694014b42bd12f09dc7ad4cc2)

This project implements a content provenance and attribution system that classifies text as likely AI-generated, likely human-written, or uncertain. The system combines 2 detection signals and produces a calibrated confidence score used to generate transparency labels.

## Architecture Overview

A submission follows this pipeline:

1. Client submits text via `/submit`
2. Server extracts request payload (`creator_id`, `text`)
3. Two detection signals run:
   - LLM-based semantic score (`llm_score`)
   - Stylometric heuristic score (`stylometric_score`)
4. Confidence engine combines both signals:
```python
confidence = 0.65 * llm_score + 0.35 * stylometric_score
```
5. System assigns attribution label:
- ≥ 0.65 → likely AI
- < 0.40 → likely human
- otherwise → uncertain
6. Entry is stored in `audit_log.json`
7. Response returns:
- confidence score
- individual signal scores
- attribution label
- transparency message


## Detection Signals

### Semantic (LLM-Based) Signal

**What it measures:**

- Likelihood that text resembles AI-generated language patterns
- Based on a Groq-hosted LLM (llama-3.3-70b-versatile)

**Why it was chosen:**

- Captures semantic-level structure and phrasing
- Detects overly formal, structured, or generic writing patterns common in AI outputs

**What it misses:**

- Misclassifies formal human writing (academic, legal, financial text)
- Sensitive to prompt phrasing and model variability

### Stylometric Signal

**What it measures:**

- Sentence length distribution
- Type-token ratio (lexical diversity)
- Punctuation density

**Why it was chosen:**

- Provides lightweight structural analysis independent of LLMs
- Captures writing “texture” rather than meaning

**What it misses:**

- Struggles with short texts
- Misclassifies structured human writing as AI-like
- Cannot understand semantics or intent


## Confidence Scoring

### Formula

```python
confidence = 0.65 * llm_score + 0.35 * stylometric_score
```
LLM signal is weighted more heavily because semantic structure is more indicative of AI patterns rather than surface-level statistics.

### Examples

**High-Confidence:**

"Artificial intelligence is rapidly transforming contemporary society across multiple domains including education, healthcare, and finance. As technological capabilities continue to advance, it is essential to consider both the opportunities and challenges associated with widespread adoption. In particular, stakeholders must ensure that ethical frameworks, transparency mechanisms, and regulatory standards are developed in parallel with innovation. Furthermore, interdisciplinary collaboration will be critical in ensuring that these systems are deployed in a responsible and equitable manner that benefits all members of society."

- Confidence: 0.740190120819612
- LLM Score: 0.82,
- Stylometric Score: 0.5919717737703198

**Low-Confidence:**

"ok so i finally tried that new ramen place downtown and honestly? underwhelming. the broth was fine but they put WAY too much sodium in it and i was thirsty for like three hours after. my friend got the spicy version and said it was better. probably won't go back unless someone drags me there"

- Confidence: 0.17762616838996986
- LLM Score: 0.12
- Stylometric Score: 0.2846461953999139


## Transparency Label

The system maps confidence into human-readable explanations:

### 1. High-confidence AI

If confidence ≥ 0.65:

"Our automated review found strong evidence that this content was generated using AI. This result is based on multiple detection methods and may be appealed by the creator."

### 2. High-confidence Human

If confidence < 0.40:

"Our automated review found strong evidence that this content was written by a human author."

### 3. Uncertain

If 0.40 ≤ confidence < 0.65:

"Our automated review could not confidently determine whether this content was human-written or AI-generated. Readers should interpret this result with caution."


## Rate Limiting

Implemented using Flask-Limiter:

- 10 requests per minute
- 100 requests per day

### Reasoning

- 10/min prevents spam or automated flooding while allowing normal user interaction
- 100/day reflects realistic per-user daily submission volume for a writing tool
- Ensures system stability without overly restricting legitimate use

### Example

```python
127.0.0.1 - - [29/Jun/2026 13:43:44] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:44] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:45] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:45] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:46] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:46] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:46] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:47] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:47] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:48] "POST /submit HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2026 13:43:48] "POST /submit HTTP/1.1" 429 -
127.0.0.1 - - [29/Jun/2026 13:43:48] "POST /submit HTTP/1.1" 429 -
```


## Known Limitations

### Formal human writing misclassification

Academic or research-heavy writing often scores as AI-like because:

- Long sentences
- Low punctuation variation
- Structured phrasing

This overlaps heavily with AI-generated text patterns.

### LLM score variability

The semantic model is sensitive to prompt phrasing and may:

- Under-score obvious AI text if phrasing is ambiguous
- Over-score polished human writing

### No contextual awareness

The system evaluates each text in isolation:

- No user history
- No cross-document comparison
- No external verification signals


## Spec Reflection

### What Helped
The requirement for two independent detection signals ensured the system does not rely solely on a single model output, improving robustness and interpretability.

### What Diverged
The original expectation of clean score separation (AI vs human) did not hold in practice. Many real inputs fall into overlapping confidence ranges, requiring:

- Threshold tuning
- Acceptance of “uncertain” as a meaningful category rather than edge failure


## AI Usage

### Confidence scoring design

AI was used to propose a weighted ensemble formula combining LLM and stylometric signals.

**What I changed:**

- Adjusted weighting to 0.65 / 0.35 after testing showed stylometric noise was too influential

### Stylometric feature engineering

AI suggested initial metrics:

- Sentence length
- Sype-token ratio
- Punctuation density

**What I changed:**

- Normalized scaling ranges to prevent punctuation from dominating final score
- Tuned constants to avoid inflated confidence values
