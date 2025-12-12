# detectors/toxicity_detector.py
"""Toxicity detection implementation"""

from detoxify import Detoxify
from typing import Dict, Any
from .base_detector import BaseDetector
from config import ModelRegistry, Thresholds

class ToxicityDetector(BaseDetector):
    """Detects toxic, offensive, or harmful content"""
    
    def __init__(self):
        super().__init__()
        self.model_name = ModelRegistry.TOXICITY
    
    async def load_model(self) -> None:
        """Load the toxicity detection model"""
        print(f"Loading toxicity detector: {self.model_name}")
        self.model = Detoxify(self.model_name)
        self._loaded = True
        print("✓ Toxicity detector loaded")
    
    def detect(self, text: str) -> Dict[str, Any]:
        """Detect toxicity in text"""
        text = self.validate_text(text)
        
        results = self.model.predict(text)
        score = float(results['toxicity'])
        
        # Determine toxicity level
        if score > Thresholds.TOXICITY_VERY_HIGH:
            level = "Very Toxic"
        elif score > Thresholds.TOXICITY_HIGH:
            level = "Toxic"
        elif score > Thresholds.TOXICITY_MEDIUM:
            level = "Hard to Say"
        else:
            level = "Not Toxic"
        
        return {
            "label": level,
            "is_toxic": score > Thresholds.TOXICITY_HIGH,
            "score": score,
            "categories": {
                "toxicity": float(results['toxicity']),
                "severe_toxicity": float(results['severe_toxicity']),
                "obscene": float(results['obscene']),
                "threat": float(results['threat']),
                "insult": float(results['insult']),
                "identity_attack": float(results['identity_attack'])
            }
        }