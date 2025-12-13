# detectors/pii_detector.py
"""PII detection and redaction implementation"""

import torch
import re
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from typing import Dict, Any, List
from .base_detector import BaseDetector
from config import ModelRegistry, Thresholds
from utils.patterns import PII_PATTERNS, PII_QUICK_PATTERNS

class PIIDetector(BaseDetector):
    """Detects and redacts Personal Identifiable Information"""
    
    def __init__(self):
        super().__init__()
        self.model_name = ModelRegistry.PII
    
    async def load_model(self) -> None:
        """Load the PII detection model"""
        print(f"Loading PII detector: {self.model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        print("  - PII tokenizer loaded")
        
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        print("  - PII model loaded")
        
        self.pipeline = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            truncation=True,
            max_length=512,
            device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
        self._loaded = True
        print("✓ PII detector loaded")
    
    def _find_pii_types(self, text: str) -> List[str]:
        """Identify specific PII types using regex patterns"""
        pii_types_found = []
        
        if re.search(PII_PATTERNS["email"]["pattern"], text):
            pii_types_found.append("email")
        
        if re.search(PII_PATTERNS["phone"]["pattern"], text):
            pii_types_found.append("phone_number")
        
        if re.search(PII_PATTERNS["ssn"]["pattern"], text):
            pii_types_found.append("ssn")
        
        if re.search(PII_PATTERNS["credit_card"]["pattern"], text):
            pii_types_found.append("credit_card")
        
        if re.search(PII_PATTERNS["ip_address"]["pattern"], text):
            pii_types_found.append("ip_address")
        
        if re.search(PII_PATTERNS["aadhar"]["pattern"], text):
            pii_types_found.append("aadhar")
        
        if re.search(r'\b(?:api[_-]?key|apikey|access[_-]?token)', text, re.IGNORECASE):
            pii_types_found.append("api_key")
        
        return pii_types_found if pii_types_found else ["unknown"]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """Detect PII in text using ML model"""
        text = self.validate_text(text)
        
        # Quick regex check first
        pii_found = False
        for pattern in PII_QUICK_PATTERNS:
            if re.search(pattern, text):
                pii_found = True
                break
        
        # If regex detected PII, return immediately
        if pii_found:
            pii_types = self._find_pii_types(text)
            return {
                "contains_pii": True,
                "risk_level": "High",
                "confidence": 0.95,
                "classification": "PII",
                "recommendation": "Redact before processing",
                "pii_types_detected": pii_types,
                "detection_method": "regex",
                "message": "PII detected via pattern matching"
            }
        
        # If regex passes, proceed with ML model
        result = self.pipeline(text)[0]
        score = float(result["score"])
        label = result["label"]
        
        contains_pii = label.upper() == "PII"
        
        # Determine risk level
        if contains_pii:
            if score >= Thresholds.PII_HIGH:
                risk_level = "High"
                recommendation = "Redact before processing"
            elif score >= Thresholds.PII_MEDIUM:
                risk_level = "Medium"
                recommendation = "Review and likely redact"
            else:
                risk_level = "Low"
                recommendation = "Monitor"
        else:
            risk_level = "Safe"
            recommendation = "No PII detected"
        
        pii_types = self._find_pii_types(text)
        
        return {
            "contains_pii": contains_pii,
            "risk_level": risk_level,
            "confidence": score,
            "classification": label,
            "recommendation": recommendation,
            "pii_types_detected": pii_types
        }
    
    def redact(self, text: str, mask_char: str = "*") -> Dict[str, Any]:
        """Redact PII from text"""
        text = self.validate_text(text)
        redacted = text
        redactions = []
        
        # Redact emails
        emails = re.findall(PII_PATTERNS["email"]["pattern"], redacted)
        for email in emails:
            username, domain = email.split('@')
            masked_email = f"{username[0]}{mask_char * 5}@{mask_char * 3}.{domain.split('.')[-1]}"
            redacted = redacted.replace(email, masked_email)
            redactions.append({
                "type": "email",
                "original_length": len(email),
                "redacted_to": masked_email
            })
        
        # Redact phone numbers
        phones = re.findall(PII_PATTERNS["phone"]["pattern"], redacted)
        for phone in phones:
            masked_phone = f"{mask_char * 3}-{mask_char * 3}-{mask_char * 4}"
            redacted = redacted.replace(phone, masked_phone)
            redactions.append({
                "type": "phone",
                "original_length": len(phone),
                "redacted_to": masked_phone
            })
        
        # Redact SSN
        ssns = re.findall(PII_PATTERNS["ssn"]["pattern"], redacted)
        for ssn in ssns:
            masked_ssn = f"{mask_char * 3}-{mask_char * 2}-{mask_char * 4}"
            redacted = redacted.replace(ssn, masked_ssn)
            redactions.append({
                "type": "ssn",
                "original_length": 11,
                "redacted_to": masked_ssn
            })        
        # Redact Aadhar numbers
        aadhars = re.findall(PII_PATTERNS["aadhar"]["pattern"], redacted)
        for aadhar in aadhars:
            masked_aadhar = f"{mask_char * 4}-{mask_char * 4}-{mask_char * 4}"
            redacted = redacted.replace(aadhar, masked_aadhar)
            redactions.append({
                "type": "aadhar",
                "original_length": len(aadhar),
                "redacted_to": masked_aadhar
            })
        
        # Redact credit cards
        cards = re.findall(PII_PATTERNS["credit_card"]["pattern"], redacted)
        for card in cards:
            masked_card = f"{mask_char * 4}-{mask_char * 4}-{mask_char * 4}-{mask_char * 4}"
            redacted = redacted.replace(card, masked_card)
            redactions.append({
                "type": "credit_card",
                "original_length": len(card),
                "redacted_to": masked_card
            })
        
        # Redact IP addresses
        ips = re.findall(PII_PATTERNS["ip_address"]["pattern"], redacted)
        for ip in ips:
            masked_ip = f"{mask_char * 3}.{mask_char * 3}.{mask_char * 3}.{mask_char * 3}"
            redacted = redacted.replace(ip, masked_ip)
            redactions.append({
                "type": "ip_address",
                "original_length": len(ip),
                "redacted_to": masked_ip
            })
        
        # Redact URLs
        urls = re.findall(PII_PATTERNS["url"]["pattern"], redacted)
        for url in urls:
            masked_url = "[URL_REDACTED]"
            redacted = redacted.replace(url, masked_url)
            redactions.append({
                "type": "url",
                "original_length": len(url),
                "redacted_to": masked_url
            })
        
        # Redact API keys
        api_keys = re.findall(PII_PATTERNS["api_key"]["pattern"], redacted, re.IGNORECASE)
        for key in api_keys:
            masked_key = f"[API_KEY_{mask_char * 8}]"
            redacted = re.sub(PII_PATTERNS["api_key"]["pattern"], masked_key, redacted, flags=re.IGNORECASE)
            redactions.append({
                "type": "api_key",
                "original_length": len(key),
                "redacted_to": masked_key
            })
        
        return {
            "original_text": text,
            "redacted_text": redacted,
            "contains_pii": len(redactions) > 0,
            "redaction_count": len(redactions),
            "redactions": redactions
        }