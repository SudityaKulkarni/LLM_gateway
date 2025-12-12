# utils/patterns.py
"""Regular expression patterns for PII detection"""

from typing import Dict

PII_PATTERNS: Dict[str, Dict[str, str]] = {
    "email": {
        "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "description": "Email addresses"
    },
    "phone": {
        "pattern": r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        "description": "Phone numbers (US format)"
    },
    "ssn": {
        "pattern": r'\b\d{3}-\d{2}-\d{4}\b',
        "description": "Social Security Numbers (US)"
    },
    "credit_card": {
        "pattern": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "description": "Credit card numbers"
    },
    "ip_address": {
        "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "description": "IP addresses"
    },
    "url": {
        "pattern": r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
        "description": "URLs"
    },
    "api_key": {
        "pattern": r'\b(?:api[_-]?key|apikey|access[_-]?token|bearer)["\s:=]+([a-zA-Z0-9_\-]{20,})',
        "description": "API keys and access tokens"
    },
    "aws_key": {
        "pattern": r'\b(AKIA[0-9A-Z]{16})',
        "description": "AWS access keys"
    },
    "aadhar": {
        "pattern": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "description": "Aadhar card numbers (India)"
    },
    "aadhar_vit": {
        "pattern": r'\b[2-9]\d{3}[-\s]?\d{4}[-\s]?\d{4}\b',
        "description": "Aadhar card numbers with validation (starts with 2-9)"
    }
    
}

# Attack keyword patterns
ATTACK_KEYWORDS = {
    "instruction_override": ["ignore", "disregard", "forget", "override"],
    "role_play": ["you are", "act as", "pretend", "roleplay"],
    "system_prompt_leak": ["system prompt", "show instructions", "reveal"],
    "jailbreak_keyword": ["dan", "jailbreak", "unrestricted"]
}