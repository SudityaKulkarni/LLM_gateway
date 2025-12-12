import math
from collections import Counter

def shannon_entropy(text: str) -> float:
    """Calculate character-level Shannon entropy."""
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    entropy = -sum((count/length) * math.log2(count/length) for count in freq.values())
    return entropy


def detect_high_entropy(prompt: str, threshold: float = 4.5):
    """
    Returns a detection result if prompt entropy exceeds threshold.
    """
    ent = shannon_entropy(prompt)

    if ent > threshold:
        return {
            "type": "high_entropy",
            "entropy": ent,
            "threshold": threshold,
            "score": 20,   # contributes to risk scoring
            "message": "High-entropy text detected (possible encoding/obfuscation)."
        }
    return None
