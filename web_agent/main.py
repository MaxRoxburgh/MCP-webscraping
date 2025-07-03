from search import generate_search_terms, search_google
from scrape import scrape_text
from analyze import summarize_and_filter

def run_agent(user_goal: str, filter_criteria: str) -> list[dict]:
    queries = generate_search_terms(user_goal)
    all_results = []

    for query in queries:
        urls = search_google(query)
        for url in urls:
            page = scrape_text(url)
            if not page:
                continue
            summary = summarize_and_filter(page, filter_criteria)
            all_results.append({
                "url": url,
                "summary": summary.strip(),
                "query": query
            })

    return all_results

if __name__ == '__main__':
    user_goal = "Find recent AI startups in climate tech"
    filter_criteria = "Must be founded after 2022, working on sustainability or carbon capture"

    results = run_agent(user_goal, filter_criteria)
    for r in results:
        print("\n---")
        print(r["url"])
        print(r["summary"])