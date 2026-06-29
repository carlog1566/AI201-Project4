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