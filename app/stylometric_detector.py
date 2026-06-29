import re
import statistics

def stylometric_score(text: str) -> float:
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = re.findall(r'\w+', text.lower())
    if not words or not sentences:
        return 0.5

    # sentence lengths
    lengths = [len(re.findall(r'\w+', s)) for s in sentences]
    avg_len = sum(lengths) / len(lengths)
    std_len = statistics.pstdev(lengths) if len(lengths) > 1 else 0

    ttr = len(set(words)) / len(words)

    punctuation = len(re.findall(r'[,:;—\-()]', text))
    punctuation_density = punctuation / len(words)

    burstiness = std_len / (avg_len + 1e-5)

    score = (
        (avg_len / 25) * 0.25 +
        (1 - ttr) * 0.25 +
        min(punctuation_density * 5, 1) * 0.15 +
        (1 - min(burstiness, 1)) * 0.35
    )

    return max(0.0, min(1.0, score))