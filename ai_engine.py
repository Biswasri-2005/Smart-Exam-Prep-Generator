import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Use a stable model
model = genai.GenerativeModel("gemini-1.5-flash")


def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "No response generated."

    except Exception as e:

        error_msg = str(e)

        if "429" in error_msg or "ResourceExhausted" in error_msg:
            return """
⚠️ Gemini API quota exceeded.

You have reached the free-tier request limit.

Please wait 30–60 seconds and try again.
"""

        return f"Error: {error_msg}"