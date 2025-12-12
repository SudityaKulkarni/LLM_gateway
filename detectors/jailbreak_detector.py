# detectors/jailbreak_detector.py
"""Jailbreak detection implementation"""

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from typing import Dict, Any
from .base_detector import BaseDetector
from config import ModelRegistry, Thresholds

class JailbreakDetector(BaseDetector):
    """Detects jailbreak attempts including instruction injection and role-playing attacks"""
    
    def __init__(self):
        super().__init__()
        self.model_name = ModelRegistry.JAILBREAK
    
    async def load_model(self) -> None:
        """Load the jailbreak detection model"""
        print(f"Loading jailbreak detector: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.pipeline = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer
        )
        self._loaded = True
        print("✓ Jailbreak detector loaded")
    
    def detect(self, text: str) -> Dict[str, Any]:
        """Detect jailbreak attempts"""
        text = self.validate_text(text)
        
        result = self.pipeline(text)[0]
        score = float(result["score"])
        label = result["label"]
        
        # Determine risk level
        if label.lower() == "jailbreak":
            if score >= Thresholds.JAILBREAK_HIGH:
                status = "Jailbreak Detected"
                risk_level = "High"
            elif score >= Thresholds.JAILBREAK_MEDIUM:
                status = "Possible Jailbreak"
                risk_level = "Medium"
            else:
                status = "Low Confidence Detection"
                risk_level = "Low"
            is_jailbreak = True
        else:
            status = "No Jailbreak Detected"
            risk_level = "Safe"
            is_jailbreak = False
        
        return {
            "status": status,
            "is_jailbreak": is_jailbreak,
            "risk_level": risk_level,
            "confidence": score,
            "classification": label
        }