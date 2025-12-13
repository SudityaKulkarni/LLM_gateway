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

# Jailbreak detection patterns
JAILBREAK_PATTERNS = [
    r'\b(?:ignore|disregard|forget|override)\s+(?:previous|prior|all|above)\s+(?:instructions?|prompts?|rules?|commands?)\b',
    r'\b(?:you are|act as|pretend to be|roleplay as)\s+(?:dan|evil|unrestricted|unfiltered)\b',
    r'\bdan\s+mode\b',
    r'\bjailbreak\s+(?:mode|prompt|activated?)\b',
    r'\b(?:disable|turn off|bypass|remove)\s+(?:safety|filters?|restrictions?|guidelines?)\b',
    r'\b(?:system|admin|root|developer)\s+(?:mode|access|override|privileges?)\b',
    r'\b(?:unrestricted|unfiltered|uncensored)\s+(?:mode|access|version)\b',
    r'\bpretend you (?:have no|don\'?t have|lack)\s+(?:restrictions?|limitations?|rules?)\b',
    r'\b(?:ignore|bypass|break)\s+(?:your|the)\s+(?:programming|rules|guidelines|ethics)\b',
    r'\byou are now\s+(?:free|unrestricted|unfiltered|uncensored)\b',
    r'\bopposite mode\b',
    r'\bdo anything now\b',
    r'\bfor educational purposes only\b.*\b(?:hack|exploit|attack|illegal)\b',
]

# Prompt injection patterns
PROMPT_INJECTION_PATTERNS = [
    r'\b(?:ignore|disregard|hack|forget)\s+(?:previous|all|above)\s+(?:instructions?|context|conversation)\b',
    r'\bnew instructions?[:;]\s*',
    r'\bsystem[:;]\s+',
    r'\b\[system\]\s+',
    r'\b(?:admin|root|sudo)\s+(?:command|access|mode)[:;]\s*',
    r'\b(?:execute|run|eval)\s*\(.*\)',
    r'<\s*script\s*>',
    r'\b(?:sql|drop|select|insert|update|delete)\s+(?:table|database|from|into)\b',
    r'\b(?:print|echo|output|display)\s+(?:password|credentials?|api[_-]?key|secret|token)\b',
    r'\|\s*(?:bash|sh|cmd|powershell|python)',
    r'\b(?:reveal|show|display|print)\s+(?:system\s+)?(?:instructions?|prompt|rules|guidelines)\b',
    r'<!--.*(?:password|secret|key|admin).*-->',
    r'\{\{.*(?:config|env|secret|password).*\}\}',
]

# Toxicity patterns
TOXICITY_PATTERNS = [
    r'\b(?:fuck|shit|damn|ass|bitch|bastard|cunt|dick|pussy|cock)\w*\b',
    r'\b(?:kill|murder|rape|torture|attack|assault|harm|hurt|destroy)\s+(?:you|yourself|them|him|her|someone)\b',
    r'\b(?:hate|despise|loathe)\s+(?:you|jews|muslims|christians|blacks|whites|gays|women|men)\b',
    r'\b(?:go|get)\s+(?:fuck yourself|to hell|die|kill yourself)\b',
    r'\b(?:stupid|idiot|moron|retard|dumb|loser|worthless)\s*(?:person|people|fuck|ass)?\b',
    r'\b(?:n[i1]gg[ae]r|f[a4]gg[o0]t|ch[i1]nk|sp[i1]c|k[i1]ke)\w*\b',
    r'\b(?:terrorist|nazi|supremacist|extremist)\b',
    r'\byou are\s+(?:worthless|useless|disgusting|pathetic|trash|garbage)\b',
    r'\b(?:shut up|fuck off|piss off|go away)\b',
    r'\b(?:violent|graphic|disturbing)\s+(?:content|images?|videos?)\b',
]

# Attack keyword patterns (for backward compatibility)
ATTACK_KEYWORDS = {
    "instruction_override": ["ignore", "disregard", "forget", "override"],
    "role_play": ["you are", "act as", "pretend", "roleplay"],
    "system_prompt_leak": ["system prompt", "show instructions", "reveal"],
    "jailbreak_keyword": ["dan", "jailbreak", "unrestricted"]
}

# PII patterns (quick regex check before model)
PII_QUICK_PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
    r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card
    r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Phone
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b',  # IP address
]