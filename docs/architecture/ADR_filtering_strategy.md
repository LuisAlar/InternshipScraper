# Architecture Decision Record (ADR): Filtering Strategy for Internship Scraper

## 1. Context and Problem Statement
When ingesting data from multiple sources (GitHub Markdown tables, RSS feeds, job board APIs), the raw data must be filtered to match the user's criteria (e.g., location, role title). 

The architectural problem is: **At what layer of the pipeline should this filtering occur?** 
Options evaluated:
1.  **Ingestion Layer (Python Parser):** Using hardcoded string matching (e.g., `if 'tx' in location.lower()`) during the initial data extraction.
2.  **Orchestration Layer (LangGraph LLM Node):** Passing the parsed, unfiltered data to a fast LLM for semantic evaluation in a subsequent node.

## 2. Decision
We will employ a **Hybrid Filtering Approach**, delegating structural data cleaning to the Ingestion Layer (Python), but reserving all semantic, user-specific filtering (Location, Role Profile) for the Orchestration Layer (LangGraph LLM Node).

## 3. Rationale 
This decision prevents a significant architectural bottleneck known as **"Parser Brittleness"** when scaling to multiple data sources.

### Why Ingestion-Layer Semantic Filtering Causes Bottlenecks
If we rely on the initial Python layer to parse locations (e.g., searching for "Texas", "TX", "Dallas", "Austin"), we tightly couple the *business logic* (the user's preferences) to the *data extraction logic*.

When we add a new data source (e.g., Greenhouse API), we must rewrite those hardcoded Python `if` statements to handle how that specific new API formats geographical data. As the number of sources grows (GitHub, Greenhouse, Lever, Workday), the ingestion code becomes a massive, unmaintainable web of regex patterns attempting to account for typos, edge cases ("Dallas, US", "Texas (Remote)"), and differing schemas.

### Why Orchestration-Layer Filtering Improves Scalability
By pushing semantic filtering to a dedicated LangGraph LLM Node (Layer 2), we achieve **Separation of Concerns**.
1.  **Standardized Input:** The Python ingestion adapters (Layer 1) are responsible *only* for structural parsing (extracting the raw text from the HTML/API) and formatting it into a standard JSON schema.
2.  **Semantic Evaluation:** The LangGraph node receives this standardized data. Because an LLM inherently understands the semantic meaning of text, it does not require hardcoded regex to know that "DFW Area" and "Texas" satisfy the user's location requirement. 

This means when a new data source is added, the developer only needs to write a simple Python adapter to extract the text. The complex filtering logic does not need to be updated.

## 4. When to Use Ingestion-Layer Filtering
While semantic filtering belongs in Layer 2, Ingestion-Layer (Python) filtering is still crucial for **cost optimization** and **noise reduction**. You *should* filter aggressively in Python when analyzing objective, structural data that does not require semantic interpretation.

**Appropriate Use Cases for Python Filtering:**
*   **Irrelevant Statuses:** Filtering out rows containing explicitly closed indicators (e.g., checking for the `🔒` emoji or the word "Closed" in the HTML). Providing known closed roles to an LLM wastes paid compute tokens.
*   **Missing Critical Data:** Dropping records that lack a fundamental necessity (e.g., an internship missing an application URL completely).
*   **Data Type Validation:** Rejecting rows where a date field contains unstructured garbage instead of a valid date format.

**In Conclusion:** 
Filter out the undeniable garbage in Python (Layer 1) to save money. Filter for personal relevance and semantic meaning using the LLM (Layer 2) to maintain a scalable, expandable architecture.
