import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
'''
Pick the model to use, currently set to gemini-pro

Options include: 
    - 
'''

model = genai.GenerativeModel("gemini-pro")

def generate(prompt: str, context: str | None = None) -> str:
    response = model.generate_content(prompt if not context else [context, prompt])
    return response.text