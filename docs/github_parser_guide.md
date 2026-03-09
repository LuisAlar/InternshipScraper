# Part 2: Building the Data Ingestion Layer (GitHub Parser)

Welcome to the **Data Ingestion** phase of your AI Automation pipeline! 

Since you are preparing for an AI Workflow Automation internship interview, we will frame this tutorial around how this is handled in professional, enterprise environments.

## 1. The Theory: Data Ingestion in AI Systems

In any production AI system, whether it is an RAG (Retrieval-Augmented Generation) application, an automation workflow, or an Agentic system, everything starts with data. 

### Why is Ingestion so critical?
As you correctly noted in your task file: **"making sure the data is clean and reliable so that no extra token / compute is done."** This is the golden rule of AI Engineering. 

If you feed raw, messy HTML or unstructured text to an LLM (like GPT-4), you are:
1.  **Wasting Money:** You pay per token. Junk data = wasted tokens.
2.  **Increasing Latency:** The more tokens the LLM has to read, the longer it takes to generate a response.
3.  **Risking Hallucination:** If the LLM has to dig through noise to find the signal, it's more likely to misunderstand the data.

### The Professional Workflow: E-T-L (Extract, Transform, Load)
In the industry, Data Engineers and AI Engineers build systems using the ETL pattern. Currently, you are building the "E" and the "T":
*   **Extract:** Fetching the data from the source (GitHub).
*   **Transform:** Cleaning the data, stripping out the "noise", and converting it into a structured format (like JSON or Python dictionaries).
*   *Load:* Sending it to the next step (which, for us, will be the LangGraph LLM evaluation node).

## 2. Analyzing our Source: The GitHub Repository

**Question:** *Does the README contain the internships available? Should they be fetched somewhere else, or is the README the ideal place?*

**Answer:** For the `SimplifyJobs/Summer2026-Internships` repository, the `README.md` **is exactly what we want**. 
Community-driven tech internship repos primarily use massive Markdown tables inside the README file to track openings. The community submits Pull Requests to update this table.

While some companies offer formal APIs (like Greenhouse or Lever job board APIs), aggregating data is difficult because every company uses a different system. The SimplifyJobs GitHub repo has already done the "aggregation" for us. Our job is now to extract those markdown tables and turn them into structured data.

## 3. Writing the Parser (Step-by-Step)

We are going to write a script that fetches the raw Markdown text of the README and parses the table into Python dictionaries.

Open `src\ingest\github.py` and let's start writing:

### Step 3.1: Import Libraries
Start by importing what you need at the top of the file:
```python
import httpx     # For making HTTP requests to GitHub
import re        # Regular expressions for parsing text
from typing import List, Dict, Any
```
*(Professional tip: Always use Type Hinting (`List`, `Dict`) in Python for AI automation. It makes your code much more predictable for both you and LangChain).*

### Step 3.2: Fetching the Data (The "Extract" Phase)
We don't want to scrape the pretty GitHub UI; that contains too much HTML noise. We want the **RAW** Markdown file.

Add this function to fetch the raw text:
```python
def fetch_readme(repo_url: str = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md") -> str:
    """Fetches the raw Markdown content of the GitHub repository's README."""
    print("Fetching data from GitHub...")
    
    # httpx is a modern, fast HTTP client (similar to requests but often preferred in modern async workflows)
    response = httpx.get(repo_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")
```

### Step 3.3: Parsing the Table (The "Transform" Phase)
This is where we save LLM tokens. Instead of passing the whole README to the AI, we use standard Python to chop it up into neat little dictionaries.

If you look at the raw README, the tables look like this:
`| Company | Role | Location | Application/Link | Date Posted |`

Add this function to parse those rows:
```python
def parse_markdown_table(markdown_text: str) -> List[Dict[str, Any]]:
    """Parses standard Markdown tables into a list of dictionaries."""
    print("Parsing Markdown tables...")
    internships = []
    
    # We split the text by newlines to look at it line by line
    lines = markdown_text.split('\n')
    
    headers = []
    parsing_table = False
    
    for line in lines:
        line = line.strip()
        
        # A markdown table row always starts and ends with a pipe '|'
        if line.startswith('|') and line.endswith('|'):
            # Split the row by '|' and strip whitespace
            # We ignore the first and last empty elements caused by the split
            cols = [col.strip() for col in line.split('|')[1:-1]]
            
            # If we haven't found headers yet, this must be the header row
            if not parsing_table:
                headers = [col.lower() for col in cols] # lowercase for easier dictionary keys
                parsing_table = True
                continue
                
            # If the row is just the separator (e.g., |---|---|), skip it
            if set(cols[0]) == {'-'} or set(cols[0]) == {':', '-'}:
                continue
                
            # If it's a data row, map it to the headers
            if len(cols) == len(headers):
                internship_data = dict(zip(headers, cols))
                internships.append(internship_data)
                
        else:
            # If we were parsing a table and stop seeing '|', the table is over
            parsing_table = False
            
    return internships
```

### Step 3.4: Cleaning the Data
Markdown links look like this: `[Apply Here](https://link.com)`. If we pass this to LangChain, we actually just want the hyperlink url, or the company name. We need one more transformation step.

```python
def clean_parsed_data(internships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Cleans up markdown links and artifacts from the parsed data."""
    cleaned = []
    
    # A regex to match markdown links: [text](URL)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    for item in internships:
        # Example: if the "company" field is "[Google](https://google.com)", 
        # let's just extract "Google"
        if 'company' in item:
            match = link_pattern.search(item['company'])
            if match:
                item['company'] = match.group(1) # Gets the text part
        
        # Let's clean the link field too
        link_key = next((k for k in item.keys() if 'link' in k or 'application' in k), None)
        if link_key and item[link_key]:
            # Some roles might be marked as closed like "🔒" or "Closed"
            if 'close' in item[link_key].lower() or '🔒' in item[link_key]:
                continue # Skip closed internships! (Saves compute!)
                
            match = link_pattern.search(item[link_key])
            if match:
                item['url'] = match.group(2) # Gets the URL part
        
        cleaned.append(item)
        
    return cleaned
```
*Notice how we filter out "Closed" internships right here in Python? If we let the LLM do that filtering, it would cost us tokens and time unnecessarily. This is great AI engineering practice!*

### Step 3.5: Tying it Together
Finally, let's create a main function to run inside `src\ingest\github.py` to test it!

```python
def extract_github_internships() -> List[Dict[str, Any]]:
    """The main entry point for this ingestion module."""
    raw_md = fetch_readme()
    raw_internships = parse_markdown_table(raw_md)
    clean_internships = clean_parsed_data(raw_internships)
    
    print(f"Successfully extracted {len(clean_internships)} open internships!")
    return clean_internships

# This block lets you run this file directly to test it:
if __name__ == "__main__":
    results = extract_github_internships()
    if results:
        print("Here is the first extracted internship:")
        print(results[0])
```

## 4. Run and Test Your Ingestion Layer

1. Open your terminal.
2. Ensure you are in the `InternshipScraper` directory and your virtual environment is active `(venv)`.
3. Run the script:
   ```powershell
   python src/ingest/github.py
   ```

You should see it fetch the data, parse the tables, filter out the closed ones, and print a clean Python dictionary representing the very first internship!

---
**Once you have written and tested this code, let me know! We will then take this clean data and plug it into our LangGraph node to start combining it with the AI!**
