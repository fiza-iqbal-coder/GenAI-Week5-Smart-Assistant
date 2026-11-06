
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key not found in .env")
    raise SystemExit

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"

print("Testing Gemini connection...")
print("Model:", MODEL_NAME)

try:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Reply with only the word SUCCESS."
    )

    print("\nGemini connection successful!")
    print("Response:", response.text)

except Exception as error:
    print("\nGemini connection failed!")
    print("Error:", error)
