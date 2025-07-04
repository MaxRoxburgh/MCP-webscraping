# MCP-webscraping
---
**Description:** This package set's up a basic web scrpaing pipline with integrated LLM's for search optimisation and website analysis

**Purpose:** The purpose of this module is to compare hand built tools with integrated MCP
---

## **Module architecture**

You → main.py

       ↓
       
   User Input: (Goal, Filter Criteria)
   
       ↓
       
   model.py → Gemini API
   
     [Generate search queries]
     
       ↓
       
   search.py → Search API (Google CSE / SerpAPI/ Bing API)
     [Return list of URLs]
       ↓
   scrape.py → Requests + BeautifulSoup
     [Scrape each URL’s main text content]
       ↓
   analyze.py → LLM API
     [Summarize or extract relevant info]
       ↓
   Filtering Logic
     [Match against user-defined criteria]
       ↓
   Final Output (JSON-style list of objects)


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
