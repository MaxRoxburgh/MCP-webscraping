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

flowchart TD
    A[User Input<br/>(Goal + Filter Criteria)] --> B[Gemini API<br/>Generate Search Queries]
    B --> C[Search API<br/>(Google Custom Search, SerpAPI)]
    C --> D[Fetch URLs]
    D --> E[Web Scraper<br/>(Requests + BeautifulSoup or Playwright)]
    E --> F[Web Page Content]
    F --> G[Gemini API<br/>Summarize & Extract Info]
    G --> H[Filtering Logic<br/>Based on User Criteria]
    H --> I[Final JSON Output<br/>Relevant Items]

    classDef system fill=#f0f9ff,stroke=#3b82f6,stroke-width=1px;
    classDef model fill=#fefce8,stroke=#ca8a04,stroke-width=1px;
    classDef data fill=#fef2f2,stroke=#dc2626,stroke-width=1px;

    class A,B,G,H,I system;
    class C,D,E data;
    class F data;


## **MCP comparison module architecture**

User → Python or Web UI → Vertex Agent 

                             ↓
                             
           Tool Calls → Your Flask API (search_web, fetch_text, etc.)
           
                             ↓
                             
                   Returns → Agent processes results → Structured response


Example output:

[
  {
    "url": "https://example.com/startup123",
    "summary": "Startup123, founded in 2023, builds AI for carbon capture.",
    "industry": "Climate Tech",
    "founded": 2023
  }
]
