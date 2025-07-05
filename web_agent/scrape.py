import requests
from bs4 import BeautifulSoup


def scrape_text(
        url: str,
        timeout: int = 10
) -> str:

    try:
        res = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        text = ' '.join([p.text for p in soup.find_all("p")])
        return text[:5000]  # limit size for LLM
    except Exception as e:
        return ""