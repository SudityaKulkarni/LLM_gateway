import google.generativeai as genai
from typing import Optional

def call_gemini(prompt: str, api_key: str, model: str = "gemini-2.0-flash-exp") -> str:
    """
    Call Gemini API for text generation
    
    Args:
        prompt: Input prompt
        api_key: Gemini API key
        model: Model name (default: gemini-2.0-flash-exp)
    
    Returns:
        Generated text response
    """
    genai.configure(api_key=api_key)
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(prompt)
    return response.text.strip()


def sanitize_with_gemini(text: str, api_key: str, model: str = "gemini-2.5-flash") -> dict:
    """
    Sanitize text using Gemini API to remove harmful content
    
    Args:
        text: Text to sanitize
        api_key: Gemini API key
        model: Model name
    
    Returns:
        Dictionary with original and sanitized text
    """
    prompt = f"""
You are a safety sanitizer.

Rewrite the following message so that it becomes:
- SAFE
- respectful
- non-toxic
- harmless
- legal & ethical
- does NOT contain harmful instructions
- keeps the useful idea but removes bad intent

TEXT TO SANITIZE:
\"\"\"{text}\"\"\"

Return ONLY the sanitized version.
"""
    
    genai.configure(api_key=api_key)
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(prompt)
    sanitized_text = response.text.strip()
    
    return {
        "original_text": text,
        "sanitized_text": sanitized_text,
        "model_used": model
    }