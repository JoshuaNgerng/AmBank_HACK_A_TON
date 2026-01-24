import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types

env_path = Path('../../../.env')

# Load .env file
load_dotenv(dotenv_path=env_path)

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
client = genai.Client(api_key=api_key)

# Load model
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=types.Part.from_text(text='Can you give me the first 100 digits of pi?'),
    config=types.GenerateContentConfig(
        system_instruction='You are a precise math assistant.',
        temperature=0,
        top_p=0.95,
        top_k=20,
    ),
)

print("result from model")
print(response.text)
print(len(response.text or ''))