from model import generate
import requests
import cache
# from config import SEARCH_API_KEY, SEARCH_ENGINE_ID


def generate_search_terms(
        user_prompt: str,
        delimiter: str = ";"
): #-> list[str]:

    # Rewrite this for better results
    prompt = f'''
    Generate a list of specific search queries based on this prompt: (~ 15-20 terms)
 
    {user_prompt}
    __________________________________________________________________________
    Make sure to have at least one query per point.
    Return only the list of queries seperated by {delimiter}.
    Don't have any extra text before or after this list.
    '''
    raw = generate(prompt)
    return [line for line in raw.split(delimiter)]


def search_google(
        query: str,
        num_results: int = 5
) -> list[str]:

    key = cache.get_cache_key(query)
    if key in cache.Cache:
        # print("Cache hit")
        res = cache.Cache[key]

    else:
        from config import SEARCH_API_KEY, SEARCH_ENGINE_ID
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": SEARCH_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": num_results
        }
        res = requests.get(url, params=params).json()
        cache.Cache[key] = res

    return [item["link"] for item in res.get("items", [])]


def search_ddg(
        query: str,
        num_results: int = 5
) -> list[str]:

    raise NotImplementedError


def search_bing(
        query: str,
        num_resluts: int = 5
) -> list[str]:

    raise NotImplementedError