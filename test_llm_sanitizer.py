import google.generativeai as genai

# ----------------------------
#  CONFIGURATION
# ----------------------------
API_KEY = "AIzaSyDql6wVFDRAFA5eZk4LjFOYyuJlRVpVc5o"  # ← put your Gemini API key here
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# ----------------------------
#  SANITIZER FUNCTION
# ----------------------------
def sanitize(text: str) -> str:
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

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()


# ----------------------------
#  MAIN LOOP
# ----------------------------
if __name__ == "__main__":
    print("✨ Gemini Sanitizer Ready!")
    while True:
        user_input = input("\nEnter text: ")
        print("Sanitized →", sanitize(user_input))