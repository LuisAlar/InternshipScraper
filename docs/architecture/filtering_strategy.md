# Filtering Strategies: Where should data be filtered?

A great architectural question to ask when building AI pipelines is: **"Where should I filter the data?"**

You mentioned wanting to only see internships in **Texas** or **Remote**. 

## The Three Layers of Filtering
In our LangGraph architecture, there are three distinct places where filtering *could* happen.

### 1. Ingestion Layer (Python & BeautifulSoup)
This is exactly what you proposed: adding an `if` statement to the `github.py` script.
**Code Example:**
```python
location = cells[2].get_text(strip=True).lower()

# Only keep Texas or Remote
if 'tx' not in location and 'texas' not in location and 'remote' not in location:
    continue 
```

*   **Pros:** This is the absolute cheapest and fastest way to do it. You instantly reduce the 1,851 internships down to a few hundred before the data ever touches the expensive AI model.
*   **Cons:** It's rigid. What if a company writes "Dallas, US" instead of "TX"? A simple python keyword search might accidentally filter out a great opportunity just because of a typo.

### 2. LangGraph Filter Node (Heuristic / Simple LLM)
This is the `Filter relevant internships` node we outlined in your architecture. 

*   **Pros:** You can use a very cheap, extremely fast LLM (like `gpt-3.5-turbo` or Claude Haiku) strictly for sorting data. You give the LLM the list of locations and ask it: `"Is this location in Texas or Remote?"` An LLM is smart enough to know that "Dallas, US" means Texas, solving the problem from Layer 1.
*   **Cons:** You are paying tokens for the LLM to read 1,851 locations. 

### 3. The Core Evaluation Node (Complex LLM)
This is where we evaluate the internship against your resume.

*   **Pros:** Deep logic. The AI determines "Does this person have the skills for this?" 
*   **Cons:** This requires an expensive, smart model (`gpt-4o`). You absolutely **DO NOT** want this node to be evaluating the location. You would be paying premium AI prices just to check if a job is in Texas!

## The Professional Blueprint: Hybrid Filtering

When designing AI Automation Workflows professionally, you almost always want a **Hybrid Approach**:

1.  **The "Dumb" Python Filter (Layer 1):** 
    Use your ingestion script to filter out absolute garbage. We already do this by filtering out roles where the location contains "Closed". We know for a fact we don't want those. 

2.  **The "Smart" AI Filter (Layer 2):** 
    Pass the surviving data to a cheap LLM node in LangGraph to do the nuanced filtering (like Location and Role Title matching). This LLM filters down the 1,800 jobs to the ~50 that actually match your criteria.

3.  **The "Brain" Node (Layer 3):**
    You send those 50 highly-relevant jobs to `gpt-4o` to be scored against your resume. 

### Conclusion for your MVP
*   **Yes, you can and should filter out obvious things in Python (BeautifulSoup).**
*   **However, for "Location", you might want to leave that for the first LangGraph Node.** 

Why? Because right now we are only scraping one GitHub repo. But later, when your system tracks 5 different websites, they will all format their locations differently. Instead of writing Custom Python `if` statements for every website, you can just let LangGraph normalize and filter the locations using a fast LLM!
