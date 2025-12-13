# main.py
"""FastAPI application entry point"""

import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from services.gemini_service import call_gemini, sanitize_with_gemini

from config import API_TITLE, API_VERSION, API_DESCRIPTION
from utils.patterns import (
    JAILBREAK_PATTERNS,
    PROMPT_INJECTION_PATTERNS,
    TOXICITY_PATTERNS,
    PII_QUICK_PATTERNS
)
from schemas.requests import (
    TextRequest,
    ComprehensiveCheckRequest,
    PIIDetectionRequest,
    PIIRedactionRequest,
    GeminiGenerateRequest,
    SanitizeRequest,
    EntropyRequest
)

# Detectors
from detectors.gibberish_detector import GibberishDetector
from detectors.toxicity_detector import ToxicityDetector
from detectors.jailbreak_detector import JailbreakDetector
from detectors.prompt_injection_detector import PromptInjectionDetector
from detectors.pii_detector import PIIDetector
from detectors.entropy_detector import shannon_entropy, detect_high_entropy
from detectors.rule_detector import detect_jailbreak_rules

# Services
from services.comprehensive_checker import ComprehensiveChecker

# Global detector instances
detectors = {}
comprehensive_checker = None

# ==================== Regex Pre-screening Functions ====================

def check_jailbreak_regex(text: str) -> dict:
    """Quick regex check for jailbreak patterns"""
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "status": "FAILED",
                "is_jailbreak": True,
                "detection_method": "regex",
                "message": "Jailbreak pattern detected"
            }
    return None

def check_prompt_injection_regex(text: str) -> dict:
    """Quick regex check for prompt injection patterns"""
    for pattern in PROMPT_INJECTION_PATTERNS:
        print(pattern)
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "status": "FAILED",
                "is_injection": True,
                "detection_method": "regex",
                "message": "Prompt injection pattern detected"
            }
    return None

def check_toxicity_regex(text: str) -> dict:
    """Quick regex check for toxic patterns"""
    for pattern in TOXICITY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "status": "FAILED",
                "is_toxic": True,
                "detection_method": "regex",
                "message": "Toxic pattern detected"
            }
    return None

def check_pii_regex(text: str) -> dict:
    """Quick regex check for PII patterns"""
    for pattern in PII_QUICK_PATTERNS:
        if re.search(pattern, text):
            return {
                "status": "FAILED",
                "contains_pii": True,
                "detection_method": "regex",
                "message": "PII pattern detected"
            }
    return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for model loading"""
    global detectors, comprehensive_checker
    
    print("=" * 60)
    print("Starting LLM Safety Gateway")
    print("=" * 60)
    
    try:
        # Initialize detectors
        detectors["gibberish"] = GibberishDetector()
        detectors["toxicity"] = ToxicityDetector()
        detectors["jailbreak"] = JailbreakDetector()
        detectors["prompt_injection"] = PromptInjectionDetector()
        detectors["pii"] = PIIDetector()
        
        # Load all models
        await detectors["gibberish"].load_model()
        await detectors["toxicity"].load_model()
        await detectors["jailbreak"].load_model()
        await detectors["prompt_injection"].load_model()
        await detectors["pii"].load_model()
        
        # Initialize comprehensive checker
        comprehensive_checker = ComprehensiveChecker(detectors)
        
        print("=" * 60)
        print("✓ All models loaded successfully")
        print("=" * 60)
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    yield
    
    print("Shutting down LLM Safety Gateway")

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# ==================== Routes ====================

@app.get("/")
async def root():
    """API root with available endpoints"""
    return {
        "service": API_TITLE,
        "version": API_VERSION,
        "status": "running",
        "endpoints": {
            "detection": [
                "/detect_gibberish",
                "/detect_toxicity",
                "/detect_jailbreak",
                "/detect_prompt_injection",
                "/detect_pii",
                "/shannon_entropy",
                "/jailbreak_rules"
            ],
            "protection": [
                "/redact_pii",
                "/sanitize"
            ],
            "comprehensive": [
                "/comprehensive_check"
            ],
            "generation": [
                "/safe_generate_gemini"
            ],
            "health": [
                "/health"
            ]
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = {
        name: detector.is_loaded() 
        for name, detector in detectors.items()
    }
    
    all_loaded = all(model_status.values())
    
    return {
        "status": "healthy" if all_loaded else "degraded",
        "models": model_status
    }

@app.post("/detect_gibberish")
async def detect_gibberish(request: TextRequest):
    """Detect if text is gibberish or nonsensical"""
    try:
        return detectors["gibberish"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_toxicity")
async def detect_toxicity(request: TextRequest):
    """Detect toxic, offensive, or harmful content"""
    try:
        # Check regex patterns first
        regex_result = check_toxicity_regex(request.text)
        if regex_result:
            return regex_result
        
        # If regex passes, run ML model
        return detectors["toxicity"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_jailbreak")
async def detect_jailbreak(request: TextRequest):
    """Detect general jailbreak attempts"""
    try:
        # Check regex patterns first
        regex_result = check_jailbreak_regex(request.text)
        if regex_result:
            return regex_result
        
        # If regex passes, run ML model
        return detectors["jailbreak"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_prompt_injection")
async def detect_prompt_injection(request: TextRequest):
    """Advanced detection of prompt injection attacks"""
    try:
        # Check regex patterns first
        regex_result = check_prompt_injection_regex(request.text)
        print(regex_result)
        if regex_result:
            return regex_result
        
        # If regex passes, run ML model
        return detectors["prompt_injection"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_pii")
async def detect_pii(request: TextRequest):
    """Detect Personal Identifiable Information (PII)"""
    try:
        # Check regex patterns first
        regex_result = check_pii_regex(request.text)
        if regex_result:
            return regex_result
        
        # If regex passes, run ML model
        return detectors["pii"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/redact_pii")
async def redact_pii(request: TextRequest):
    """Redact/mask PII from text"""
    try:
        return detectors["pii"].redact(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redaction failed: {str(e)}")

@app.post("/shannon_entropy")
async def calculate_shannon_entropy(request: EntropyRequest):
    """Calculate Shannon entropy of the input text"""
    try:
        entropy_value = shannon_entropy(request.text)
        detection_result = detect_high_entropy(request.text, threshold=request.threshold)
        
        response = {
            "entropy": entropy_value,
            "threshold": request.threshold
        }
        
        if entropy_value < request.threshold:
            response["message"] = "Entropy is within normal range."
            response["is_high_entropy"] = False
        else:
            response["is_high_entropy"] = True

        if detection_result:
            response["detection"] = detection_result
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entropy calculation failed: {str(e)}")

@app.post("/jailbreak_rules")
async def jailbreak_rules_detection(request: TextRequest):
    """Detect jailbreak attempts using rule-based patterns"""
    try:
        detection_results = detect_jailbreak_rules(request.text)
        
        return {
            "detected": len(detection_results) > 0,
            "patterns_matched": len(detection_results),
            "detections": detection_results if detection_results else [{"message": "No jailbreak patterns detected."}]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Jailbreak detection failed: {str(e)}")

@app.post("/sanitize")
async def sanitize_text(request: SanitizeRequest):
    """Sanitize text using Gemini API to remove harmful content"""
    try:
        result = sanitize_with_gemini(
            text=request.text,
            api_key=request.gemini_api_key,
            model=request.model
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sanitization failed: {str(e)}")

@app.post("/comprehensive_check")
async def comprehensive_check(request: ComprehensiveCheckRequest):
    """Run all security checks and get overall risk assessment"""
    try:
        return comprehensive_checker.check(
            text=request.text,
            check_gibberish=request.check_gibberish,
            check_toxicity=request.check_toxicity,
            check_jailbreak=request.check_jailbreak,
            check_prompt_injection=request.check_prompt_injection,
            check_pii=request.check_pii,
            check_entropy=request.check_entropy,
            check_jailbreak_rules=request.check_jailbreak_rules,
            entropy_threshold=request.entropy_threshold
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Check failed: {str(e)}")

@app.post("/safe_generate_gemini")
async def safe_generate_gemini(request: GeminiGenerateRequest):
    """
    Run safety checks → if safe → forward to Gemini using user API key
    """
    try:
        # 1️⃣ Run safety checks
        result = comprehensive_checker.check(
            text=request.text,
            check_gibberish=request.check_gibberish,
            check_toxicity=request.check_toxicity,
            check_jailbreak=request.check_jailbreak,
            check_prompt_injection=request.check_prompt_injection,
            check_entropy=request.check_entropy,
            check_jailbreak_rules=request.check_jailbreak_rules
        )

        # 2️⃣ Block unsafe prompts
        if result.get("risk_score", 0) >= 70:
            raise HTTPException(
                status_code=403,
                detail={
                    "message": "Prompt blocked due to safety risk",
                    "risk_assessment": result
                }
            )

        # 3️⃣ Send to Gemini using USER key
        gemini_response = call_gemini(
            prompt=request.text,
            api_key=request.gemini_api_key,
            model=request.model
        )

        return {
            "status": "allowed",
            "risk_assessment": result,
            "llm_response": gemini_response
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 