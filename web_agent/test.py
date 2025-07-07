from search import *
from utils import string_search_and_replace
from scrape import scrape_text


'''
Pick the model to use, currently set to gemini-2.5-flash

Options include: 
    - gemini-2.5-flash; 15 RPM, 1500 RPD, 1mil TPM 
    - gemini-2.5-pro; 60 RPM, 1000 RPD, ~6mil token cap/day
    - gemini-2.5-flash-lite-preview-06-17; 500 RPD
    - gemini-2.0-flash-lite-001; 
    - gemini-2.0-flash-preview-image-generation
    - gemini-embedding-exp-03-07
'''
file_path = 'prompts/user_goal.txt' # Replace with your actual file path

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    print("File content as a single string:")
    # print(file_content)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
user_goal = '''
Find <COUNTRY>-specific data for the following categories related to the property market. For each category, provide a variety of queries that would be effective for sourcing raw data, reports, and news.

Categories:

Macroeconomic Indicators: <COUNTRY> GDP growth rate, Central bank base rate history, <COUNTRY> currency to USD exchange rate forecast, <COUNTRY> inflation rate (CPI), <COUNTRY> housing starts data, and <COUNTRY> housing market activity reports.

Real Estate Market Data: historical <COUNTRY> house price index, current average rental prices by <COUNTRY> city, <COUNTRY> property ownership demographics, and typical rental yields in the <COUNTRY>.

Demographics: <COUNTRY> population growth by region, median household income <COUNTRY>, cost of living comparison between <COUNTRY> cities, and primary languages spoken in major <COUNTRY> urban centers.

Real Estate Industry: top real estate and letting agencies in the <COUNTRY>, leading property development corporations in the <COUNTRY>, and popular <COUNTRY>-wide property listing platforms.

Infrastructure & Services: average <COUNTRY> electricity prices, current <COUNTRY> fuel cost per litre, and traffic congestion statistics for major <COUNTRY> cities.

News & Analysis: RSS feeds for <COUNTRY> real estate news, <COUNTRY> economic news updates, and analysis of international news impacting the <COUNTRY> property market.

Regulations & Risk: legal framework for <COUNTRY> land ownership, regulations on foreign investment in <COUNTRY> property, and risk assessment reports for the <COUNTRY> real estate market.
'''
print(f"user_goal == file_content -> {user_goal==file_content}\n")

user_goal = string_search_and_replace(user_goal, {'<COUNTRY>': "UK"})
queries_list = generate_search_terms(user_goal)
print(len(queries_list), "queries generated")
if len(queries_list) < 21:
    # Google only gives you 100 free queries a day...
    links = [search_google(query, 6) for query in queries_list]
else:
    raise Exception("list too long, don't want to run out of search's too quickly")

link_list = []
for link_sub_list in links:
    for link in link_sub_list:
        link_list.append(link)
link_list = [i for i in set(link_list)]
print(len(link_list), "links generated")

print(link_list[0])
sc = scrape_text(link_list[0])
# print(sc)

from analyse import summarise_and_filter
dict_output = summarise_and_filter(sc)
print(f"output type: {type(dict_output)}")
print(f"output: {dict_output}")

from time import sleep
import json
print("Running over entire list...")
dict_output_list = []
for link in link_list:
    sc = scrape_text(link)
    dict_output = summarise_and_filter(sc)
    if dict_output:
        if dict_output["type"] != "irrelevant":
            dict_output["link"] = str(link)
            dict_output_list.append(dict_output)
    sleep(1)

print(f"number of valid links identified: {len(dict_output_list)}")
output_filename = "links_uk.json"

try:
    # Use 'utf-8' encoding for broad compatibility
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(dict_output_list, json_file, indent=4)

    print(f"Successfully wrote list of dictionaries to '{output_filename}' in human-readable format.")

except IOError as e:
    print(f"Error writing to file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")






