import requests
from requests.exceptions import RequestException, Timeout
import tiktoken


def filter_broken_links(
        urls_list: list[dict]
) -> list[dict]:
    """

    """
    valid_links = []

    # Define a common user-agent to make requests appear more like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Starting link check...")
    # Iterate over the values (URLs) of the input dictionary
    for url_dict in urls_list:
        try:
            # Make a GET request to the URL with a timeout of 10 seconds
            response = requests.get(url_dict['link'], timeout=10, headers=headers)

            # Check the HTTP status code
            if response.status_code == 200:
                valid_links.append(url_dict)
                print(f"✅ OK: {url_dict['name']}")
            elif response.status_code == 404:
                print(f"❌ 404 Not Found: {url_dict['name']}")
            else:
                print(f"⚠️ Status {response.status_code}: {url_dict['name']}")

        except ConnectionError:
            # Catch errors related to network problems (e.g., DNS failure, refused connection)
            print(f"🚫 Connection Error: {url_dict['name']}")
        except Timeout:
            # Catch timeout errors if the server doesn't respond within the specified time
            print(f"⏳ Timeout Error: {url_dict['name']}")
        except RequestException as e:
            # Catch any other requests-related exceptions (e.g., invalid url, too many redirects)
            print(f"❗ Request Error for {url_dict['name']}: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"🛑 An unexpected error occurred for {url_dict['name']}: {e}")

    print("\nLink check completed.")
    return valid_links

def estimate_tokens(
        text: str
) -> int:
    try:
        # Not exact token length as doesn't have google doesn't disclose how they tokenise
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))
    except Exception as e:
        print(f"<UNK> An unexpected error occurred for {text}: {e}")
        print("Token estimation reverted to max length of string (overestimate)")
        return len(text)

def string_search_and_replace(
        text: str,
        replacement_strings_dict: dict[str, str]
) -> str:
    for placeholder, replacement_string in replacement_strings_dict.items():
        text = text.replace(placeholder, replacement_string)
    return text
