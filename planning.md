# AI201 Project 4 Planning

## Detection Signals

### Signal 1: LLM-Based Classification

**What it measures**

The Groq LLM analyzes the writing holistically by evaluating semantic meaning, context, and tone.

**Output**

Returns an AI likelihood score between 0 and 1.

- ~ 0.0 = Definitely Human
- ~ 1.0 = Definitely AI

**Strengths**

- Understands context
- Detects subtle stylistic patterns
- Handles many writing genres

**Blind Spots**

- May misclassify polished human writing
- Doesn't capture structure
- Can be steered by framing

### Signal 2: Stylometric Heuristics

**What it measures**

A collection of measurable writing statistics including:

- Average sentence length
- Sentence length variance
- Punctuation density
- Word repetition

**Output**

Returns an AI likelihood score between 0 and 1.

- ~ 0.0 = Definitely Human
- ~ 1.0 = Definitely AI

**Strengths**

- Fast
- Fully explainable
- Independent of LLM reasoning

**Blind Spots**

- Cannot understand meaning
- Academic writing may appear AI-generated
- Human writing widely varies


## Confidence Scoring and Uncertainty Representation

The final score is calculated using a weighted average of both detection signals.

```
Final Score = (0.60 * LLM Score) + (0.40 * Stylometric Score)
```

The LLM is weighted more due to how it considers overall context and writing quality, while the stylometric heuristics provides supporting statistical evidence based on structure.

### Confidence Thresholds

|-------------|--------|-------|
| 0.75 – 1.00 | Likely AI | High-confidence AI |
| 0.45 – 0.74 | Uncertain | Uncertain |
| 0.00 – 0.44 | Likely Human | High-confidence Human |

**Meaning of a Confidence Score**

A confidence score of **0.60** does **not** mean the system is 60% certain the content is AI-generated.

Instead, it means the evidence from both detection signals is mixed enough that the system cannot confidently classify the submission.

Because false positives are especially harmful on creative platforms, the uncertain range is intentionally wide. The system avoids confidently labeling content as AI-generated unless both signals strongly agree.


