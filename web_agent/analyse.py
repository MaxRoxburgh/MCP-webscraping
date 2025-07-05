from model import generate

def summarise_and_filter(text: str, criteria: str) -> str:
    prompt = """
    Based on the following criteria: 
    <criteria>
    Extract or summarize any relevant information from this text:
    ---
    <web_text>
    """
    result = generate(prompt)
    return result