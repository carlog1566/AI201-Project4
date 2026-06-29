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

## Transparency Labels

| Result | Label Text |
|---------|------------|
| High-confidence AI | "Our automated review found strong evidence that this content was generated using AI. This result is based on multiple detection methods and may be appealed by the creator." |
| Uncertain | "Our automated review could not confidently determine whether this content was human-written or AI-generated. Readers should interpret this result with caution." |
| High-confidence Human | "Our automated review found strong evidence that this content was written by a human author." |


## Appeals Workflow

Any creator whose submission has been analyzed may submit an appeal.

### Required Information

- content_id
- creator_id
- written explanation describing why the creator believes the decision is incorrect

### Appeal Process

1. Locate the original submission.
2. Store the creator's appeal reason.
3. Change the submission status from: "classified" to "under review"
4. Record the appeal in the structured audit log.
5. Return confirmation that the appeal was received.

No automatic re-classification occurs.

## Human Reviewer View

A reviewer would see:

- Content ID
- Creator ID
- Original submission
- Original detector scores
- Final confidence score
- Attribution result
- Appeal reason
- Timestamp
- Current status
