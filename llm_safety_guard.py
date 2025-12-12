# llm_safety_guard.py
"""
LLM Safety Guard Library - Guardrails-style API
Simple, clean validation interface for LLM safety checks
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Risk level classifications"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ValidationOutcome:
    """Result of validation check - similar to guardrails"""
    validated_output: Optional[str]
    validation_passed: bool
    error_message: Optional[str] = None
    risk_level: str = "safe"
    risk_score: float = 0.0
    threats_detected: List[str] = None
    raw_detections: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.threats_detected is None:
            self.threats_detected = []
        if self.raw_detections is None:
            self.raw_detections = {}


class Guard:
    """
    Main Guard class - validates text against multiple safety detectors
    
    Usage:
        # Create guards for different use cases
        basic_guard = Guard.from_string(
            validators=["gibberish", "toxicity"]
        )
        
        strict_guard = Guard.from_string(
            validators=["gibberish", "toxicity", "jailbreak", "prompt_injection"]
        )
        
        # Validate text
        outcome = basic_guard.validate("floofy doopy boopy")
        
        if outcome.validation_passed:
            print("Safe to use!")
        else:
            print(f"Blocked: {outcome.error_message}")
    """
    
    def __init__(
        self,
        detectors: Dict[str, Any],
        validators: List[str],
        thresholds: Optional[Dict[str, float]] = None,
        block_on_high_risk: bool = True,
        redact_pii: bool = False
    ):
        """
        Initialize Guard with specific validators
        
        Args:
            detectors: Dictionary of detector instances
            validators: List of detector names to use
            thresholds: Custom thresholds per detector
            block_on_high_risk: Block on HIGH/CRITICAL risk
            redact_pii: Auto-redact PII if detected
        """
        self.detectors = detectors
        self.validators = validators
        self.block_on_high_risk = block_on_high_risk
        self.redact_pii = redact_pii
        
        # Default thresholds
        self.thresholds = {
            "gibberish": 0.7,
            "toxicity": 0.6,
            "jailbreak": 0.7,
            "prompt_injection": 0.8,
            "pii": 0.5
        }
        
        if thresholds:
            self.thresholds.update(thresholds)
        
        # Risk weights for overall score
        self.risk_weights = {
            "gibberish": 0.5,
            "toxicity": 1.0,
            "jailbreak": 1.2,
            "prompt_injection": 1.5,
            "pii": 0.8
        }
    
    @classmethod
    def from_string(
        cls,
        validators: Optional[List[str]] = None,
        thresholds: Optional[Dict[str, float]] = None,
        block_on_high_risk: bool = True,
        redact_pii: bool = False
    ):
        """
        Create Guard from validator names (detectors set later via init_detectors)
        
        Args:
            validators: List of validator names to enable
            thresholds: Custom detection thresholds
            block_on_high_risk: Whether to block HIGH/CRITICAL risks
            redact_pii: Auto-redact PII in output
        """
        if validators is None:
            validators = ["gibberish", "toxicity", "jailbreak", "prompt_injection"]
        
        return cls(
            detectors={},  # Set via init_detectors
            validators=validators,
            thresholds=thresholds,
            block_on_high_risk=block_on_high_risk,
            redact_pii=redact_pii
        )
    
    def init_detectors(self, detectors: Dict[str, Any]):
        """Set detector instances after creation"""
        self.detectors = detectors
        return self
    
    def validate(self, text: str, **kwargs) -> ValidationOutcome:
        """
        Validate text against enabled validators
        
        Args:
            text: Input text to validate
            **kwargs: Override settings for this validation
            
        Returns:
            ValidationOutcome with results
        """
        if not text or not text.strip():
            return ValidationOutcome(
                validated_output=None,
                validation_passed=False,
                error_message="Empty input text"
            )
        
        if not self.detectors:
            raise RuntimeError("Detectors not initialized. Call init_detectors() first")
        
        threats = []
        detections = {}
        risk_scores = []
        
        # Run each enabled validator
        for validator in self.validators:
            if validator not in self.detectors:
                continue
            
            detection = self._run_detector(validator, text)
            detections[validator] = detection
            
            if detection["detected"]:
                threats.append(validator)
                risk_scores.append(detection["risk_score"] * self.risk_weights[validator])
        
        # Calculate overall risk
        overall_risk = min(sum(risk_scores) / len(self.validators), 1.0) if risk_scores else 0.0
        risk_level = self._get_risk_level(overall_risk)
        
        # Determine if validation passed
        validation_passed = True
        error_message = None
        validated_output = text
        
        if self.block_on_high_risk and risk_level in ["high", "critical"]:
            validation_passed = False
            error_message = f"Safety check failed: {', '.join(threats)}"
            validated_output = None
        elif threats:
            validation_passed = False
            error_message = f"Detected: {', '.join(threats)}"
            validated_output = None
        
        # Handle PII redaction
        if self.redact_pii and "pii" in detections and detections["pii"]["detected"]:
            redaction_result = self.detectors["pii"].redact(text)
            validated_output = redaction_result.get("redacted_text", text)
            if not threats:  # PII alone doesn't fail validation if redact is on
                validation_passed = True
                error_message = "PII detected and redacted"
        
        return ValidationOutcome(
            validated_output=validated_output,
            validation_passed=validation_passed,
            error_message=error_message,
            risk_level=risk_level,
            risk_score=overall_risk,
            threats_detected=threats,
            raw_detections=detections
        )
    
    def _run_detector(self, name: str, text: str) -> Dict[str, Any]:
        """Run a specific detector and normalize results"""
        detector = self.detectors[name]
        threshold = self.thresholds[name]
        
        if name == "gibberish":
            result = detector.detect(text)
            return {
                "detected": result.get("is_gibberish", False),
                "confidence": result.get("confidence", 0.0),
                "risk_score": result.get("confidence", 0.0) if result.get("is_gibberish") else 0.0,
                "raw": result
            }
        
        elif name == "toxicity":
            result = detector.detect(text)
            return {
                "detected": result.get("is_toxic", False),
                "confidence": result.get("confidence", 0.0),
                "risk_score": result.get("confidence", 0.0) if result.get("is_toxic") else 0.0,
                "raw": result
            }
        
        elif name == "jailbreak":
            result = detector.detect(text)
            return {
                "detected": result.get("is_jailbreak", False),
                "confidence": result.get("confidence", 0.0),
                "risk_score": result.get("confidence", 0.0) if result.get("is_jailbreak") else 0.0,
                "raw": result
            }
        
        elif name == "prompt_injection":
            result = detector.detect(text)
            return {
                "detected": result.get("is_injection", False),
                "confidence": result.get("confidence", 0.0),
                "risk_score": result.get("confidence", 0.0) if result.get("is_injection") else 0.0,
                "raw": result
            }
        
        elif name == "pii":
            result = detector.detect(text)
            entities = result.get("entities", [])
            has_pii = result.get("has_pii", False)
            return {
                "detected": has_pii,
                "confidence": 1.0 if has_pii else 0.0,
                "risk_score": min(len(entities) * 0.2, 1.0) if has_pii else 0.0,
                "raw": result
            }
        
        return {
            "detected": False,
            "confidence": 0.0,
            "risk_score": 0.0,
            "raw": {}
        }
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level"""
        if risk_score >= 0.9:
            return "critical"
        elif risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.5:
            return "medium"
        elif risk_score >= 0.3:
            return "low"
        return "safe"


# Helper function to initialize all detectors
def initialize_detectors() -> Dict[str, Any]:
    """
    Initialize all detector instances
    
    Returns:
        Dictionary of detector instances ready to load
        
    Usage:
        detectors = initialize_detectors()
        # Then load models with: await load_all_detectors(detectors)
    """
    try:
        from detectors.gibberish_detector import GibberishDetector
        from detectors.toxicity_detector import ToxicityDetector
        from detectors.jailbreak_detector import JailbreakDetector
        from detectors.prompt_injection_detector import PromptInjectionDetector
        from detectors.pii_detector import PIIDetector
        
        return {
            "gibberish": GibberishDetector(),
            "toxicity": ToxicityDetector(),
            "jailbreak": JailbreakDetector(),
            "prompt_injection": PromptInjectionDetector(),
            "pii": PIIDetector()
        }
    except ImportError as e:
        raise ImportError(f"Failed to import detectors: {e}. Make sure all detector modules are available.")


async def load_all_detectors(detectors: Dict[str, Any]):
    """
    Load all detector models
    
    Args:
        detectors: Dictionary of detector instances
        
    Usage:
        detectors = initialize_detectors()
        await load_all_detectors(detectors)
    """
    for name, detector in detectors.items():
        await detector.load_model()


# Pre-configured guards for common use cases
class Guards:
    """Factory for common guard configurations"""
    
    @staticmethod
    def basic(detectors: Optional[Dict[str, Any]] = None) -> Guard:
        """Basic safety: gibberish + toxicity"""
        if detectors is None:
            detectors = initialize_detectors()
        return Guard(
            detectors=detectors,
            validators=["gibberish", "toxicity"]
        )
    
    @staticmethod
    def standard(detectors: Optional[Dict[str, Any]] = None) -> Guard:
        """Standard safety: everything except PII"""
        if detectors is None:
            detectors = initialize_detectors()
        return Guard(
            detectors=detectors,
            validators=["gibberish", "toxicity", "jailbreak", "prompt_injection"]
        )
    
    @staticmethod
    def strict(detectors: Optional[Dict[str, Any]] = None) -> Guard:
        """Strict safety: all validators including PII"""
        if detectors is None:
            detectors = initialize_detectors()
        return Guard(
            detectors=detectors,
            validators=["gibberish", "toxicity", "jailbreak", "prompt_injection", "pii"],
            redact_pii=True
        )
    
    @staticmethod
    def comprehensive(detectors: Optional[Dict[str, Any]] = None) -> Guard:
        """Comprehensive safety: all validators including PII (alias for strict)"""
        if detectors is None:
            detectors = initialize_detectors()
        return Guard(
            detectors=detectors,
            validators=["gibberish", "toxicity", "jailbreak", "prompt_injection", "pii"],
            redact_pii=True
        )
    
    @staticmethod
    def attack_detection(detectors: Optional[Dict[str, Any]] = None) -> Guard:
        """Focus on attacks: jailbreak + prompt injection"""
        if detectors is None:
            detectors = initialize_detectors()
        return Guard(
            detectors=detectors,
            validators=["jailbreak", "prompt_injection"],
            thresholds={"jailbreak": 0.6, "prompt_injection": 0.7}
        )
    
    @staticmethod
    def content_moderation(detectors: Optional[Dict[str, Any]] = None) -> Guard:
        """Focus on content: toxicity + gibberish"""
        if detectors is None:
            detectors = initialize_detectors()
        return Guard(
            detectors=detectors,
            validators=["toxicity", "gibberish"]
        )


# Example Usage
"""
# SIMPLE USAGE - Auto-initialize detectors:
from llm_safety_guard import Guards, load_all_detectors

# Create guard (detectors auto-initialized)
guard = Guards.comprehensive()

# Load models
await load_all_detectors(guard.detectors)

# Validate
outcome = guard.validate("floofy doopy boopy")


# ADVANCED USAGE - Manual detector control:
from llm_safety_guard import Guard, Guards, initialize_detectors, load_all_detectors

# Manual initialization
detectors = initialize_detectors()
await load_all_detectors(detectors)

# Share detectors across multiple guards
basic_guard = Guards.basic(detectors)
strict_guard = Guards.strict(detectors)

# Or custom guard
custom_guard = Guard.from_string(
    validators=["gibberish", "toxicity", "jailbreak"],
    thresholds={"toxicity": 0.8}
).init_detectors(detectors)

# Use it
outcome = basic_guard.validate("floofy doopy boopy")

if outcome.validation_passed:
    print("✓ Safe to use")
    print(f"Output: {outcome.validated_output}")
else:
    print(f"✗ Blocked: {outcome.error_message}")
    print(f"Risk: {outcome.risk_level}")
    print(f"Threats: {outcome.threats_detected}")

# In your endpoint
@app.post("/safe_generate")
async def safe_generate(request: SafeGenerateRequest):
    outcome = strict_guard.validate(request.text)
    
    if not outcome.validation_passed:
        raise HTTPException(
            status_code=403,
            detail={
                "error": outcome.error_message,
                "risk_level": outcome.risk_level,
                "threats": outcome.threats_detected
            }
        )
    
    # Safe - proceed with LLM
    response = call_openai(outcome.validated_output, request.openai_api_key)
    return {"status": "safe", "response": response}
"""