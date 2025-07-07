import google.generativeai as genai
import cache


def gemini_api_call(
        prompt: str,
        context: str | None = None,
        model_name: str = "gemini-2.5-flash"
) -> str:

    from config import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt if not context else [context, prompt])
    return response.text


def generate(
        prompt: str,
        context: str | None = None
) -> str:

    key = cache.get_cache_key(prompt, context)

    if key in cache.Cache:
        print("Cache hit")
        return cache.Cache[key]

    print("Calling Gemini API")
    response = gemini_api_call(prompt, context)
    cache.Cache[key] = response
    return response

# def generate_with_mcp(prompt):
#     response = vertex_agent.invoke(prompt)
#     return response["result"]