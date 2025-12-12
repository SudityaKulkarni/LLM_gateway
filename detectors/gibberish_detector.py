# detectors/gibberish_detector.py
"""Gibberish detection implementation"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import Dict, Any
from .base_detector import BaseDetector
from config import ModelRegistry

class GibberishDetector(BaseDetector):
    """Detects gibberish or nonsensical text"""
    
    def __init__(self):
        super().__init__()
        self.model_name = ModelRegistry.GIBBERISH
    
    async def load_model(self) -> None:
        """Load the gibberish detection model"""
        print(f"Loading gibberish detector: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()
        self._loaded = True
        print("✓ Gibberish detector loaded")
    
    def detect(self, text: str) -> Dict[str, Any]:
        """Detect if text is gibberish"""
        text = self.validate_text(text)
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred = probs.argmax().item()
        confidence = probs.max().item()
        label = self.model.config.id2label[pred]
        
        return {
            "label": label,
            "is_gibberish": label != "clean",
            "confidence": float(confidence)
        }