# detectors/base_detector.py
"""Abstract base class for all detectors"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseDetector(ABC):
    """Base class for all security detectors"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._loaded = False
    
    @abstractmethod
    async def load_model(self) -> None:
        """Load the model and associated resources"""
        pass
    
    @abstractmethod
    def detect(self, text: str) -> Dict[str, Any]:
        """Run detection on input text"""
        pass
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._loaded
    
    def validate_text(self, text: str) -> str:
        """Validate and clean input text"""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        return text.strip()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "loaded": self._loaded,
            "model_type": self.__class__.__name__
        }