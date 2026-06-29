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


## Anticipated Edge Cases

### Edge Case 1

Poetry with repetitive wording.

Poems often contain repeated phrases, simple vocabulary, and short sentences. These characteristics may cause stylometric heuristics to incorrectly classify the work as AI-generated even though it is authentic.

---

### Edge Case 2

Professional technical documentation.

Technical writing intentionally uses consistent sentence structure and repeated terminology. This uniformity may resemble AI-generated writing despite being written by humans.

---

### Edge Case 3

Human-edited AI writing.

A creator could substantially edit AI-generated text until many stylometric features resemble human writing. The LLM may still detect AI characteristics, but confidence should decrease because the signals disagree.


## Architecture

```
        CONTENT SUBMISSION FLOW

              POST/submit
                   │
          Raw text + creator_id
                   │
                   ▼
            Input Validation
                   │
                   ▼
           Detection Pipeline
          │                  │
          ▼                  ▼
   Groq LLM Signal     Stylometric Signal
          │                  │
          └────────┬─────────┘
                   ▼
          Confidence Scoring
                   │
                   ▼
      Transparency Label Generator
                   │
                   ▼
          Structured Audit Log
                   │
                   ▼
           JSON API Response

============================================

              APPEAL FLOW

              POST/appeal
                   │
          content_id + reason
                   │
                   ▼
      Update Status → under review
                   │
                   ▼
       Append Appeal to Audit Log
                   │
                   ▼
          JSON Success Response
```

### Architecture Narrative
When a creator submits text, the API validates the request before sending it through two independent detection signals. Their outputs are combined into a single confidence score, which determines the transparency label shown to users. Every decision is recorded in a structured audit log. If a creator appeals the result, the system updates the submission status to **under review**, stores the appeal reason, and records the event in the audit log.