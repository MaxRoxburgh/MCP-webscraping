import pandas as pd
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException


def read_json(file_path: str) -> dict:
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_broken_links(urls_dict: dict[str, str]) -> dict[str, str]:
    """
    Checks a dictionary of URLs (where values are the URLs) for connectivity
    issues or 404 errors and returns a new dictionary containing only the active,
    reachable links, with new sequential string keys.

    Args:
        urls_dict: A dictionary where keys are strings (e.g., "0", "1") and
                   values are the URLs (strings) to be checked.

    Returns:
        A new dictionary where keys are sequential strings ("0", "1", "2", ...)
        and values are the URLs that are reachable and do not return a 404
        (Not Found) status code.
    """
    active_links_dict = {}
    link_counter = 0 # Initialize a counter for new keys

    # Define a common user-agent to make requests appear more like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Starting link check...")
    # Iterate over the values (URLs) of the input dictionary
    for url in urls_dict.values():
        try:
            # Make a GET request to the URL with a timeout of 10 seconds
            response = requests.get(url, timeout=10, headers=headers)

            # Check the HTTP status code
            if response.status_code == 200:
                # If status code is 200 (OK), the link is active
                active_links_dict[str(link_counter)] = url # Add to dictionary with new key
                link_counter += 1 # Increment counter for the next active link
                print(f"✅ OK: {url}")
            elif response.status_code == 404:
                # If status code is 404 (Not Found), the link is broken
                print(f"❌ 404 Not Found: {url}")
            else:
                # Handle other non-200 status codes as potentially broken or problematic
                print(f"⚠️ Status {response.status_code}: {url}")

        except ConnectionError:
            # Catch errors related to network problems (e.g., DNS failure, refused connection)
            print(f"🚫 Connection Error: {url}")
        except Timeout:
            # Catch timeout errors if the server doesn't respond within the specified time
            print(f"⏳ Timeout Error: {url}")
        except RequestException as e:
            # Catch any other requests-related exceptions (e.g., invalid URL, too many redirects)
            print(f"❗ Request Error for {url}: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"🛑 An unexpected error occurred for {url}: {e}")

    print("\nLink check completed.")
    return active_links_dict

def dataframe_to_country_links_json(df: pd.DataFrame, output_path: str) -> None:
    result = {}
    for country in df.columns:
        links = {}
        for index, link in enumerate(df[country]):
            if pd.notnull(link):
                links[index] = link
        links = filter_broken_links(links)
        result[country] = links
    with open(output_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Converted DataFrame to JSON and saved to", output_path)


# example of not working link https://bigdata-madesimple.com/6-use-cases-of-big-data-ai-in-real-estate/
#

if __name__ == '__main__':
    df = pd.read_csv('old_europe_links.csv', encoding='latin1', header=None).transpose()
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    output_path = 'europe_old_links.json'
    dataframe_to_country_links_json(df, output_path)


