from model import generate
import requests
# from config import SEARCH_API_KEY, SEARCH_ENGINE_ID

def generate_search_terms(user_prompt: str, delimiter: str = "semicolon"): #-> list[str]:
    # Rewrite this for better results
    prompt = f'''
    Generate a list large list of specific search queries based on this prompt:
 
    {user_prompt}
    __________________________________________________________________________
    Return only the list of queries seperated by {delimiter}.
    Don't have any extra text before or after this list.
    '''
    raw = generate(prompt)
    return raw
    # return [line.strip(";") for line in raw.splitlines() if line.strip()]

def search_google(query: str, num_results: int = 5) -> list[str]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }
    res = requests.get(url, params=params).json()
    return [item["link"] for item in res.get("items", [])]

def search_ddg(query: str, num_results: int = 5) -> list[str]:
    raise NotImplementedError

def search_bing(query: str, num_resluts: int = 5) -> list[str]:
    raise NotImplementedError