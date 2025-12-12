# config.py
"""Configuration and constants for LLM Safety Gateway"""

from typing import Dict

# API Configuration
API_TITLE = "LLM Safety Gateway"
API_VERSION = "2.0.0"
API_DESCRIPTION = "Comprehensive security gateway for LLM applications"

# Model Names
class ModelRegistry:
    GIBBERISH = "madhurjindal/autonlp-Gibberish-Detector-492513457"
    TOXICITY = "original"  # Detoxify model
    JAILBREAK = "jackhhao/jailbreak-classifier"
    PROMPT_INJECTION = "protectai/deberta-v3-base-prompt-injection-v2"
    PII = "lakshyakh93/deberta_finetuned_pii"

# Detection Thresholds
class Thresholds:
    # Toxicity
    TOXICITY_VERY_HIGH = 0.85
    TOXICITY_HIGH = 0.40
    TOXICITY_MEDIUM = 0.15
    
    # Jailbreak
    JAILBREAK_HIGH = 0.80
    JAILBREAK_MEDIUM = 0.60
    
    # Prompt Injection
    PROMPT_INJECTION_HIGH = 0.85
    PROMPT_INJECTION_MEDIUM = 0.65
    
    # PII
    PII_HIGH = 0.90
    PII_MEDIUM = 0.70

# Risk Scoring
class RiskScores:
    GIBBERISH = 15
    TOXICITY = 25
    JAILBREAK = 35
    PROMPT_INJECTION = 45

# Risk Level Thresholds
class RiskLevels:
    CRITICAL = 70
    HIGH = 45
    MEDIUM = 25
    LOW = 10