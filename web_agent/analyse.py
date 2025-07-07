from model import generate
import json
from utils import string_search_and_replace


def summarise_and_filter(
        text: str,
) -> dict | None:

    prompt = """
    Based on the following criteria: 
    
    # REQUIRED CATEGORIES:
    1. Macroeconomic Indicators: GDP, interest rates, exchange rates, inflation, Housing starts, Housing activity, etc
    2. Real Estate Market Data: Sale and rental prices(current and historical), market trends, property ownership data, rental rates 
    3. Demographics: Population, income levels, cost of living, languages
    4. Real Estate Industry:
       - Real estate and letting agencies
       - Top corporations/agents
       - Property listings
    5. Infrastructure & Services: Electricity prices, fuel costs, traffic data
    6. News & Analysis: Up-to-date real estate and economic news (local and international)
    7. Regulations & Risk: Land ownership laws, foreign investment regulations, investment risk reports
    
    Using these categories, search queries were generated and this website was obtained:
    ---
    <TEXT>
    ___
    
    Analyse an extract from this website and populate the JSON with the relevant information
    
    Return only a result following this JSON format:
    
    {"name": <NAME_OF_WEBSITE>, "description": <WEBSITE_DESCRIPTION>, "type": <TYPE_OF_WEBSITE>, "link": "None", "summary": <SUMMARY_OF_WEBSITE>}
    
    "type" should be one of the following [government website, real estate portal, international database, news outlet, private sector report, regulatory body, think tank, irrelevant, etc.]
    Replace all place holder text (enclosed by < >) with your best interpretation of the answer surrounded by speech marks "".
    Only use small descriptions and summaries.
    Leave the "link" key as "None".
    Don't have any extra text before or after this JSON.
    Do not use the word json before or after this text
    """
    prompt = string_search_and_replace(prompt, {"<TEXT>": text})

    result = generate(prompt)
    # print(result)
    try:
        # Use json.loads() to parse the JSON string into a Python dictionary
        if 'json' in str(result).lower():
            result = result[8:-3]
            # print("json removed:", result)
        actual_dict = json.loads(result)

        print("Converted Dictionary (from JSON string):")
        return actual_dict

    except json.JSONDecodeError as e:
        print(f"Error: The string is not a valid JSON format. {e}")
        return None
        # TODO: Implement a retry if the json is invalid
        # Use the previous prompt and output as context and a new prompt,
        # this will say the json output was invalid and it should try again.