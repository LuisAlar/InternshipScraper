# InternshipScraper

An AI Automation tool that tailors internships from varius data sources.

This system scrapes GitHub repositories for software engineering internships, parses the data, and uses an LangGraph workflow with Gemini to semantically filter roles based on user preferences (like location) and deeply evaluate them against the candidate's resume.

## Architecture & System Overview

The system is built as an E-T-L pipeline (Extract, Transform, Load) using Python, LangChain, and LangGraph, operating in three distinct filtering layers.

### The 3-Layer Filtering Strategy

1. **Layer 1: Data Ingestion (Python ETL)**
   - **How it works**: Uses `httpx` to extract raw Markdown tables from GitHub community repositories (e.g., SimplifyJobs), parses them into Python dictionaries, and cleans the artifact links.
   - **Filtering**: Performs initial "dumb" filtering via basic Python string matching .
   - **Why**: Filtering obvious mismatches before they reach the LLM saves token costs and increases speed. Performing only structural parsing here prevents "Parser Brittleness" when new data sources are added.

2. **Layer 2: Orchestration & Semantic Filter (LangGraph)**
   - **How it works**: Passes the standardized structural data into a LangGraph node powered by `gemini-1.5-flash`.
   - **Filtering**: Uses the fast LLM with Pydantic structured outputs to evaluate semantic requirements (e.g., determining if "Dallas, US" satisfies a "Texas or Remote" requirement). 
   - **Why**: Prevents brittle, unmaintainable regex conditions in the Python layer by allowing the AI to understand human intent and varied data schemas.

3. **Layer 3: Core Evaluation (Complex LLM)**
   - **How it works**: The highly curated list of surviving, relevant internships is sent to a deep reasoning model (`gemini-1.5-pro`).
   - **Filtering**: The model evaluates the role requirements against a symlinked copy of the user's resume to determine a match score.
   - **Why**: Reserves the expensive, deep compute exclusively for internships that are virtually guaranteed to be geographically and topically relevant.

---

## Setup and Installation

### 1. Project Environment
This project uses a standard Python virtual environment. The environment should be created in the root of the project, **outside** of the `src` directory.

```bash
# 1. Ensure you are in the root directory
cd Workspace/projects/InternshipScraper

# 2. Create the virtual environment
python -m venv venv

# 3. Activate the virtual environment (Windows/PowerShell)
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
Once the virtual environment is active (you will see `(venv)` in your terminal), install the required packages:

```bash
pip install langchain langgraph langchain-google-genai httpx bs4 python-dotenv
```

### 3. Directory Structure
The application requires specific folders to operate. Create these in your root directory if they do not exist:

```bash
mkdir docs tasks
mkdir src src\ingest src\nodes src\core
```

### 4. Link Your Resumes
The evaluation node requires access to your resumes. Instead of copying them, create a symbolic link from your master resume folder directly into this project.

Run this command from the root `InternshipScraper` directory (requires PowerShell Administrator or Developer Mode enabled):

```powershell
New-Item -ItemType SymbolicLink -Path "resumes" -Target "c:\Users\alarc\OneDrive\Documents\Academic\Applications\resumes"
```

### 5. Environment Variables
To authenticate with the primary LLM, create a `.env` file inside the `src` directory:

```bash
# Make sure you are in the scr directory
New-Item -Path ".env" -ItemType File
```
Open `src/.env` and add your Google API Key:
```env
GOOGLE_API_KEY=your-gemini-key-here
```

---

## Usage
*Instructions for running the complete LangGraph pipeline will go here once the `main.py` entry point is finalized. Currently, you can test the ingestion layer by running:*

```bash
python src/ingest/github.py
```
