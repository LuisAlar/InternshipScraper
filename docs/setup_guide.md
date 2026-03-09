# Internship Automation Tool: Manual Setup Guide

Welcome to your first automation! This guide will walk you through setting up the environment and creating the foundational architecture for the LangChain and LangGraph internship scraper.

## 1. Environment Setup

### The Virtual Environment
**Question:** *Should the Virtual Environment (`venv`) be in the `src` folder or outside of it?*
**Answer:** The `venv` folder should be placed **outside** of the `src` folder, directly in the root of your project directory (`Workspace/projects/InternshipScraper/`). 
*   **Why?** The virtual environment contains all the installed Python packages (like LangChain) and the Python executable itself. It is not part of your *source code* (`src/`), but rather the environment that runs your code. Keeping it isolated makes it easier to tell Git to ignore it (via a `.gitignore` file).

**Your setup looks correct!** If you ran `python -m venv venv` in `c:\Users\alarc\Developer\Workspace\projects\InternshipScraper`, the `venv` folder is right where it belongs.

### Activating the Environment
Before you install packages, you must activate the virtual environment so they install locally to this project, not globally on your computer.

1.  Open your terminal inside the `InternshipScraper` directory.
2.  Run the activation script:
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
    *(You should see `(venv)` appear at the beginning of your terminal prompt).*

### Installing Dependencies
Now that you are *inside* the virtual environment, install the tools you need for the MVP:

```powershell
pip install langchain langgraph langchain-openai httpx bs4 python-dotenv
```

## 2. Directory Structure Setup

Now, let's create the folder structure we designed in the architecture manually. 

1.  Make sure you are in `c:\Users\alarc\Developer\Workspace\projects\InternshipScraper`.
2.  Create the necessary directories:
    ```powershell
    # Documentation and Obsidian tasks
    mkdir docs
    mkdir tasks

    # The Python Source Code
    mkdir src
    mkdir src\ingest
    mkdir src\nodes
    mkdir src\core
    ```
3.  Create the empty files needed to get started:
    ```powershell
    New-Item -Path "src\.env" -ItemType File
    New-Item -Path "src\main.py" -ItemType File
    New-Item -Path "src\ingest\github.py" -ItemType File
    New-Item -Path "src\nodes\extract.py" -ItemType File
    New-Item -Path "src\nodes\load_resumes.py" -ItemType File
    New-Item -Path "src\nodes\evaluate.py" -ItemType File
    New-Item -Path "src\nodes\export.py" -ItemType File
    New-Item -Path "src\core\state.py" -ItemType File
    ```

## 3. Link Your Resumes (Symlink)

As discussed in your architecture, you want to link the `resumes` folder directly into this project without copying the files.

Run this command from the root of the `InternshipScraper` directory:

```powershell
New-Item -ItemType SymbolicLink -Path "resumes" -Target "c:\Users\alarc\OneDrive\Documents\Academic\Applications\resumes"
```
*(If this fails, you may need to open PowerShell as Administrator or enable "Developer Mode" in Windows Settings).*

## 4. Setup Your Environment Variables

Open the `src\.env` file you created and add your necessary API keys. For example:

```env
OPENAI_API_KEY=sk-your-key-here
```

## Next Steps for the MVP

Once you've run through the steps above, your environment is ready to go!

The first step in writing the code will be to open `src\ingest\github.py` and write a Python script that uses the `httpx` or `requests` library to fetch the raw README file from the SimplifyJobs repo you provided:
`https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md`

Let me know when you've finished setting this up, and we can start working on the Github parsing logic!
