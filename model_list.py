import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_GEMINI_API")

if not api_key:
    raise ValueError("GOOGLE_GEMINI_API not found")

genai.configure(api_key = api_key)

print("Available Gemini Models")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f" - {model.name}")