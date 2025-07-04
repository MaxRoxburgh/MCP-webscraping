import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
'''
Pick the model to use, currently set to gemini-2.5-flash

Options include: 
    - gemini-2.5-flash; 15 RPM, 1500 RPD, 1mil TPM 
    - gemini-2.5-pro; 60 RPM, 1000 RPD, ~6mil token cap/day
    - gemini-2.5-flash-lite-preview-06-17; 500 RPD
    - gemini-2.0-flash-lite-001; 
    - gemini-2.0-flash-preview-image-generation
    - gemini-embedding-exp-03-07
'''

model = genai.GenerativeModel("gemini-2.5-flash")

def generate(prompt: str, context: str | None = None) -> str:
    response = model.generate_content(prompt if not context else [context, prompt])
    return response.text

# def generate_with_mcp(prompt):
#     response = vertex_agent.invoke(prompt)
#     return response["result"]