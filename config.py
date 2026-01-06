import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not GOOGLE_API_KEY or not ELEVEN_API_KEY:
    raise EnvironmentError("Missing API keys")

genai.configure(api_key=GOOGLE_API_KEY)


LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi",
    "Bengali": "Bengali",
    "Telugu": "Telugu",
    "Marathi": "Marathi",
    "Tamil": "Tamil"
}
