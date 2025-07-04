import requests
from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

with open("europe_old_links.json") as f:
    old_links = json.load(f)

def setup_perplexity() -> None:
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def setup_gemini() -> None:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL = "https://api.gemini.com/v1/gemini"


def collect_new_links_with_gemini(prompt):

    client = genai.Client(api_key="YOUR_API_KEY")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="prompt"
    )

    return response.text

def collect_new_links_with_perplexity(prompt):
    payload = {
        "model": "sonar-pro", 
        "messages": [
            {"role": "system", "content": "You are a research assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(PERPLEXITY_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error code: {response.status_code} - {response.text}")
    
def new_links_prompt(country, existing_links):
    return f"""
        # ROLE:
        You are a world-class real estate research assistant, trained in economic and urban data discovery. Your task is to locate downloadable, high-quality datasets relevant to the real estate market of {country}, particularly for use by institutional or foreign investors.

        # GOAL:
        Return a **structured JSON array** of **at least one** reliable source per data category listed below. Please collect **at least 15** links across categories in total. Each source must link directly to downloadable, structured datasets (e.g., CSV, XLSX, JSON, GeoJSON, Shapefile, or ZIP). 

        Do NOT include static PDF-only reports unless they contain embedded tables and allow data extraction.

        # CONTEXT:
        We have already collected a set of known useful resources for {country}. You’ll find them below under `{existing_links}`. These links were previously validated and should be included in your output **if still relevant**, with metadata added or improved.

        However, **your goal is to go beyond** these links and discover any **missing or complementary datasets** across all required categories.

        # EXISTING LINKS:
        {existing_links}

        # FOCUS METRICS (Include at least one source per category):

        1. **Macroeconomics**
        - GDP, GDP growth, GDP per capita
        - Inflation
        - Real interest rates
        - Unemployment rate
        - Saving rate
        - FDI (foreign direct investment)
        - Tax rates
        - Heritage Foundation rankings (or economic freedom index)

        2. **Demographics & Urban**
        - Population (national/urban/rural split)
        - Employment data
        - Cost of living
        - Land cover, urban expansion (prefer spatial or geospatial formats)

        3. **Climate & Environmental Risk**
        - Flood risk
        - Remote sensing outputs
        - Climate hazard maps

        4. **Real Estate Market**
        - Residential/commercial property prices
        - Historical transaction volumes
        - Rental indices
        - Mortgage statistics

        5. **Land, Legal & Regulation**
        - Large-scale land acquisitions
        - Land rights and cadastral data
        - Zoning regulations
        - Investment policy reports

        6. **Property Listings & Agencies**
        - Real estate portals listing properties for sale or rent (API endpoints or scrapable table pages)
        - Directories of real estate agencies or brokers

        7. **Infrastructure & Services**
        - Electricity prices, fuel costs
        - Water access, internet availability
        - Traffic data or transport accessibility

        8. **News & Market Analysis**
        - Real estate market trend analysis
        - Investment risk reporting
        - Regulatory announcements or reforms

        # CONSTRAINTS:
        - ❌ Exclude: login-required sites, vague landing pages, visual-only dashboards, articles with no data download
        - ✅ Prefer: open data portals, national statistics offices, real estate databases, government APIs, World Bank/IMF/UN, or reputable industry research platforms
        - 📝 If multiple formats exist, prefer **CSV**, then JSON/XLSX, then others
        - 🌍 National coverage is preferred, but subnational is acceptable where national is unavailable

        # OUTPUT FORMAT:
        Return your response as a **JSON array of objects**. Each object must include the following fields:
        - `name`: Title of the dataset or organization providing the data
        - `description`: What the dataset contains (include specific metrics or formats where applicable)
        - `type`: One of [government website, real estate portal, international database, news outlet, private sector report, regulatory body, think tank]
        - `link`: Direct URL to the data download page or structured content
        - `summary`: Brief comment on geographic or thematic scope (e.g., “National land ownership data”, “Urban rental index for capital city”)

        Format the result like this (no explanations):

        {{
        "name": "...",
        "description": "...",
        "type": "...",
        "link": "...",
        "summary": "..."
        }}

        # EXAMPLE OUTPUT:
        [
        {{
            "name": "World Bank Data - Serbia",
            "description": "Downloadable macroeconomic indicators including GDP growth, inflation, unemployment, and FDI",
            "type": "international database",
            "link": "https://data.worldbank.org/country/serbia",
            "summary": "National coverage for macro indicators (CSV export supported)"
        }},
        {{
            "name": "Republic Geodetic Authority of Serbia",
            "description": "Provides cadastral data, zoning regulations, and ownership maps; some services via Web Feature Service (WFS)",
            "type": "government website",
            "link": "https://www.rgz.gov.rs/",
            "summary": "National land data with sub-regional zoning and ownership structure (geospatial)"
        }}
        ]

        # SPECIAL NOTES:
        - If no source exists for a category, skip it — do not hallucinate.
        - For spatial data, prefer GeoJSON, Shapefile, or ZIP downloads over raw images or map viewers.
        - You may return more than one entry per category if available.


    """

def filter_broken_links(urls_list: list[dict]) -> list[dict]:
    """

    """
    valid_link = []

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
                valid_link.append(url_dict)
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
    return valid_link


example_input = [
        {{
            "name": "World Bank Data - Serbia",
            "description": "Downloadable macroeconomic indicators including GDP growth, inflation, unemployment, and FDI",
            "type": "international database",
            "link": "https://data.worldbank.org/country/serbia",
            "summary": "National coverage for macro indicators (CSV export supported)"
        }},
        {{
            "name": "Republic Geodetic Authority of Serbia",
            "description": "Provides cadastral data, zoning regulations, and ownership maps; some services via Web Feature Service (WFS)",
            "type": "government website",
            "link": "https://www.rgz.gov.rs/",
            "summary": "National land data with sub-regional zoning and ownership structure (geospatial)"
        }}
]
#%%#####################################################################################################################################################
"""
Now load the old links JSON file and iterate over countries.
For each country:
(1) Collect new links and enrich output JSON file with more existing links
(3) Each new link needs to be validated
(3) Save JSON file in the folder
"""




for country, links_dict in old_links.items():
    print(f"Processing {country}...")
    try:
        prompt = new_links_prompt(country, links_dict)
        content = collect_new_links_with_perplexity(prompt)
        filename = re.sub(r'\W+', '_', country.lower())
        filepath = os.path.join(output_folder, f"{filename}.json")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            print(f"Output for {country} not valid JSON, saving as raw text.")
            parsed = content

        with open(filepath, "w") as f:
            if isinstance(parsed, list):
                json.dump(parsed, f, indent=2)
            else:
                f.write(parsed)

        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed for {country}: {e}")

