# Model Evaluation: Gemini vs OpenAI for Automation

When building an AI workflow, choosing the right LLM for each node is a critical architectural decision. 

Since you have a Gemini Advanced/Developer subscription, let's evaluate if you should use **Gemini 1.5 Flash** instead of OpenAI's models for this project.

## The Short Answer
**Yes, you should absolutely use Gemini 1.5 Flash.** 
For a filtering node dealing with 1,800+ rows of data, Flash is the mathematically perfect model. It is faster, significantly cheaper, and more than capable of handling the semantic logic of "Is this location in Texas?"

## Evaluating Models by Use Case

In Agentic Workflows like LangGraph, we categorize models into two buckets:

### 1. The "Router/Filter" Models (Layer 2)
These models need to be incredibly fast and very cheap. They perform repetitive, structured tasks (like classifying data, routing queries, or extracting JSON).
*   **OpenAI:** `gpt-4o-mini` or `gpt-3.5-turbo`
*   **Google:** `gemini-1.5-flash`
*   **Anthropic:** `claude-3-haiku`

**Winner for your project: Gemini 1.5 Flash**
Flash is specifically designed by Google for these high-volume, repetitive data-processing tasks. If you run 1,851 internships through `gpt-4o-mini`, it will cost you API credits. If you use your Gemini subscription, you can hit the Google Developer API using your existing quota.

### 2. The "Brain" Models (Layer 3)
These models need deep reasoning capabilities, complex logic, and high context windows. They do the heavy lifting (like comparing your resume to a job description and writing the tailored bullets).
*   **OpenAI:** `gpt-4o` or `gpt-o1`
*   **Google:** `gemini-1.5-pro`
*   **Anthropic:** `claude-3.5-sonnet`

**Winner for your project: Gemini 1.5 Pro**
Since you are already in the Google ecosystem, using Gemini 1.5 Pro for the final evaluation node is ideal. It has a massive context window (meaning it can easily read your entire resume and the job description without forgetting details) and excellent reasoning capabilities.

---

## How to Switch to Gemini in LangChain

If you want to use Gemini, we just need to change two lines of code in your environment and script!

### 1. Update your Environment Variables (`src/.env`)
Instead of `OPENAI_API_KEY`, you need to get a free API key from Google AI Studio (`aistudio.google.com`).
```env
# Delete the OpenAI key and add:
GOOGLE_API_KEY=AIzaSyYourKeyHere...
```

### 2. Update your Dependencies
You need to install the LangChain Google package instead of the OpenAI one.
Run this in your terminal (with the venv active):
```powershell
pip install langchain-google-genai
```

### 3. Update the Python Script (`src/nodes/filter.py`)
In the guide, I showed you this for OpenAI:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

**Simply replace it with this for Gemini:**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
# Use Gemini Flash for the fast filtering node!
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
```

*(Everything else in the script, like `llm.with_structured_output(FilterDecision)`, works exactly the same! That's the beauty of using LangChain—it abstracts the specific model away so you can swap them instantly).*
