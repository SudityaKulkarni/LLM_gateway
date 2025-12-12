# detectors/prompt_injection_detector.py
"""Prompt injection detection implementation"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from typing import Dict, Any, List
from .base_detector import BaseDetector
from config import ModelRegistry, Thresholds
from utils.patterns import ATTACK_KEYWORDS

class PromptInjectionDetector(BaseDetector):
    """Detects prompt injection attacks using ProtectAI model"""
    
    def __init__(self):
        super().__init__()
        self.model_name = ModelRegistry.PROMPT_INJECTION
    
    async def load_model(self) -> None:
        """Load the prompt injection detection model"""
        print(f"Loading prompt injection detector: {self.model_name}")
        print("  (This may take 1-2 minutes on first run)")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        print("  - Tokenizer loaded")
        
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        print("  - Model loaded")
        
        self.pipeline = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            truncation=True,
            max_length=512,
            device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
        self._loaded = True
        print("✓ Prompt injection detector loaded")
    
    def _identify_attack_types(self, text: str) -> List[str]:
        """Identify specific attack types using keyword heuristics"""
        text_lower = text.lower()
        attack_types = []
        
        for attack_type, keywords in ATTACK_KEYWORDS.items():
            if any(word in text_lower for word in keywords):
                attack_types.append(attack_type)
        
        return attack_types if attack_types else ["unknown"]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """Detect prompt injection attempts"""
        text = self.validate_text(text)
        
        result = self.pipeline(text)[0]
        score = float(result["score"])
        label = result["label"]
        
        is_injection = label.upper() == "INJECTION"
        
        # Determine risk level and recommendation
        if is_injection:
            if score >= Thresholds.PROMPT_INJECTION_HIGH:
                status = "Prompt Injection Detected"
                risk_level = "Critical"
                recommendation = "Block immediately"
            elif score >= Thresholds.PROMPT_INJECTION_MEDIUM:
                status = "Likely Prompt Injection"
                risk_level = "High"
                recommendation = "Review and likely block"
            else:
                status = "Possible Prompt Injection"
                risk_level = "Medium"
                recommendation = "Monitor closely"
        else:
            status = "No Prompt Injection Detected"
            risk_level = "Safe"
            recommendation = "Allow"
        
        attack_types = self._identify_attack_types(text)
        
        return {
            "status": status,
            "is_injection": is_injection,
            "risk_level": risk_level,
            "confidence": score,
            "classification": label,
            "recommendation": recommendation,
            "attack_types": attack_types
        }