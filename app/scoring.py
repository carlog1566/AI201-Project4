from llm_detector import llm_score
from stylometric_detector import stylometric_score

def compute_confidence(text: str):
    llm = llm_score(text)              # semantic
    style = stylometric_score(text)    # structural

    # weighted ensemble (LLM slightly stronger)
    confidence = (llm * 0.65) + (style * 0.35)

    return {
        "llm_score": llm,
        "stylometric_score": style,
        "confidence": confidence
    }

def generate_label(confidence: float):
    if confidence >= 0.65:
        return "Our automated review found strong evidence that this content was generated using AI. This result is based on multiple detection methods and may be appealed by the creator."
    elif confidence < 0.4:
        return "Our automated review found strong evidence that this content was written by a human author."
    else:
        return "Our automated review could not confidently determine whether this content was human-written or AI-generated. Readers should interpret this result with caution."