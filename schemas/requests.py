# schemas/requests.py
"""Pydantic request schemas"""

from pydantic import BaseModel, Field
from typing import Optional

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")

class ComprehensiveCheckRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")
    check_gibberish: bool = Field(True, description="Enable gibberish detection")
    check_toxicity: bool = Field(True, description="Enable toxicity detection")
    check_jailbreak: bool = Field(True, description="Enable jailbreak detection")
    check_prompt_injection: bool = Field(True, description="Enable prompt injection detection")
    check_pii: bool = Field(True, description="Enable PII detection")
    check_entropy: bool = Field(True, description="Enable Shannon entropy detection")
    check_jailbreak_rules: bool = Field(True, description="Enable rule-based jailbreak detection")
    entropy_threshold: float = Field(4.5, description="Threshold for high entropy detection")

class PIIDetectionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze for PII")
    detect_email: bool = True
    detect_phone: bool = True
    detect_ssn: bool = True
    detect_credit_card: bool = True
    detect_ip_address: bool = True
    detect_url: bool = True
    detect_api_keys: bool = True

class PIIRedactionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to redact PII from")
    redact_email: bool = True
    redact_phone: bool = True
    redact_ssn: bool = True
    redact_credit_card: bool = True
    redact_ip_address: bool = True
    redact_url: bool = True
    redact_api_keys: bool = True
    mask_char: str = Field("*", max_length=1, description="Character to use for masking")
    show_redacted_count: bool = True

class GeminiGenerateRequest(BaseModel):
    text: str = Field(..., min_length=1)
    gemini_api_key: str = Field(..., min_length=20)
    model: str = Field("gemini-2.5-flash", description="Gemini model to use")
    
    # optional safety toggles
    check_gibberish: bool = True
    check_toxicity: bool = True
    check_jailbreak: bool = True
    check_prompt_injection: bool = True
    check_entropy: bool = True
    check_jailbreak_rules: bool = True

class SanitizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to sanitize")
    gemini_api_key: str = Field(..., min_length=20)
    model: str = Field("gemini-2.5-flash", description="Gemini model to use")

class EntropyRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze entropy")
    threshold: float = Field(4.5, description="Threshold for high entropy detection") 