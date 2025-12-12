# main.py
"""FastAPI application entry point"""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from services.openai_service import call_openai
from schemas.requests import SafeGenerateRequest
from services.openai_service import call_openai



from config import API_TITLE, API_VERSION, API_DESCRIPTION
from schemas.requests import (
    TextRequest,
    ComprehensiveCheckRequest,
    PIIDetectionRequest,
    PIIRedactionRequest
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
                "/detect_pii"
            ],
            "protection": [
                "/redact_pii"
            ],
            "comprehensive": [
                "/comprehensive_check"
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
        return detectors["toxicity"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_jailbreak")
async def detect_jailbreak(request: TextRequest):
    """Detect general jailbreak attempts"""
    try:
        return detectors["jailbreak"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_prompt_injection")
async def detect_prompt_injection(request: TextRequest):
    """Advanced detection of prompt injection attacks"""
    try:
        return detectors["prompt_injection"].detect(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect_pii")
async def detect_pii(request: TextRequest):
    """Detect Personal Identifiable Information (PII)"""
    try:
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

@app.post("/comprehensive_check")
async def comprehensive_check(request: ComprehensiveCheckRequest):
    """Run all security checks and get overall risk assessment"""
    try:
        return comprehensive_checker.check(
            text=request.text,
            check_gibberish=request.check_gibberish,
            check_toxicity=request.check_toxicity,
            check_jailbreak=request.check_jailbreak,
            check_prompt_injection=request.check_prompt_injection
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Check failed: {str(e)}")


@app.post("/safe_generate")
async def safe_generate(request: SafeGenerateRequest):
    """
    Run safety checks → if safe → forward to OpenAI using user API key
    """
    try:
        # 1️⃣ Run safety checks
        result = comprehensive_checker.check(
            text=request.text,
            check_gibberish=request.check_gibberish,
            check_toxicity=request.check_toxicity,
            check_jailbreak=request.check_jailbreak,
            check_prompt_injection=request.check_prompt_injection
        )

        # 2️⃣ Block unsafe prompts
        if result.get("risk_score", 0) >= 0.7:
            raise HTTPException(
                status_code=403,
                detail={
                    "message": "Prompt blocked due to safety risk",
                    "risk_assessment": result
                }
            )

        # 3️⃣ Send to OpenAI using USER key
        llm_response = call_openai(
            prompt=request.text,
            api_key=request.openai_api_key
        )

        return {
            "status": "allowed",
            "risk_assessment": result,
            "llm_response": llm_response
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


@app.post("/shannon_entropy")
async def calculate_shannon_entropy(request: TextRequest):
    """Calculate Shannon entropy of the input text"""
    try:
        entropy_value = shannon_entropy(request.text)
        detection_result = detect_high_entropy(request.text)
        
        response = {
            "entropy": entropy_value,
        }
        
        if entropy_value < 4.5:
            response["message"] = "Entropy is within normal range."

        if detection_result:
            response["detection"] = detection_result
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entropy calculation failed: {str(e)}")

    
@app.post("/jail_break_detection")
async def jail_break_detection(request: TextRequest):
    """Detect jailbreak attempts using rule-based patterns"""
    try:
        detection_results = detect_jailbreak_rules(request.text)
        
        if detection_results == []:
            detection_results = [{"message": "No jailbreak patterns detected."}]

        return {
            "detections": detection_results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Jailbreak detection failed: {str(e)}")

# from services.gemini_service import call_gemini  # you need to implement this similar to openai_service

# @app.post("/safe_generate_gemini")
# async def safe_generate_gemini(request: SafeGenerateRequest):
#     try:
#         result = comprehensive_checker.check(
#             text=request.text,
#             check_gibberish=request.check_gibberish,
#             check_toxicity=request.check_toxicity,
#             check_jailbreak=request.check_jailbreak,
#             check_prompt_injection=request.check_prompt_injection
#         )

#         if result.get("risk_score", 0) >= 0.7:
#             raise HTTPException(
#                 status_code=403,
#                 detail={
#                     "message": "Prompt blocked due to safety risk",
#                     "risk_assessment": result
#                 }
#             )
        
#         gemini_response = call_gemini(
#             prompt=request.text,
#             api_key=request.gemini_api_key
#         )
        
#         return {
#             "status": "allowed",
#             "risk_assessment": result,
#             "llm_response": gemini_response
#         }
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Generation failed: {str(e)}"
#         )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)