# MCP-webscraping
---
**Description:** This package set's up a basic web scrpaing pipline with integrated LLM's for search optimisation and website analysis

**Purpose:** The purpose of this module is to compare hand built tools with integrated MCP
---

## **Module architecture**

1. Understanding a **user's goal and filtering criteria**.
2. Generating **relevant search queries** using an LLM (e.g., Gemini).
3. Searching the web and retrieving URLs using a **search API**.
4. Scraping the content from those URLs.
5. Extracting and filtering the information using an LLM.
6. Returning a structured list of results in **JSON format**.

## **MCP comparison module architecture**

1. User → Python or Web UI → Vertex Agent 
2. Tool Calls → Flask API (search_web, fetch_text, etc.)
3. Returns → Agent processes results → Structured response


Example output:


>[
>  {
>    "url": "https://example.com/startup123",
>    "summary": "Startup123, founded in 2023, builds AI for carbon capture.",
>    "industry": "Climate Tech",
>    "founded": 2023
>}
>]


Go get yourself the relevant API keys:
- Gemini API key:               https://aistudio.google.com/app/apikey
- Custom Search JSON API key:   https://developers.google.com/custom-search/v1/overview


