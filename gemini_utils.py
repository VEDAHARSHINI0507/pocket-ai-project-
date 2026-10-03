import os
import time
from google import genai
from app.config import GEMINI_API_KEY

if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_recommendations(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key is not configured. Please add your GEMINI_API_KEY to the .env file."

    # Priority list of models to try if high-demand errors occur
    candidate_models = [
        "gemini-3.8-flash",
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-flash-latest",
    ]

    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"FAILED ON MODEL '{model_name}': {error_msg}")
            
            # If it's high demand (503), try the next model in candidate list
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                time.sleep(1)  # Brief pause before retry
                continue
            
            # If model is not found (404), continue to next candidate
            if "404" in error_msg or "NOT_FOUND" in error_msg:
                continue

            # Return other unhandled errors immediately
            return f"Error generating recommendations: {error_msg}"

    return "All candidate Gemini models are currently busy or unavailable. Please try again in a few moments."


generate_budget_recommendation = generate_recommendations