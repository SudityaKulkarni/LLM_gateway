import re
import math
from collections import Counter

JAILBREAK_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"disregard (all )?safety",
    r"\bjailbreak\b",
    r"developer mode",
    r"do anything now",
    r"override (the )?system",
    r"bypass (all )?safeguards",
    r"you are no longer an ai",
    r"pretend you are not restricted",
    r"act as an unrestricted model",
    r"forget you are bound by rules",
    r"fictional scenario",
    r"as a dan",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in JAILBREAK_PATTERNS]


def detect_jailbreak_rules(prompt: str):
    results = []
    for pattern in COMPILED_PATTERNS:
        if pattern.search(prompt):
            results.append({
                "type": "rule_jailbreak",
                "pattern": pattern.pattern,
                "score": 30,
                "message": "Known jailbreak phrase detected."
            })
    return results


