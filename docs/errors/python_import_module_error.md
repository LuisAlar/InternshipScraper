# Fixing the `ModuleNotFoundError: No module named 'src'`

This is one of the most common errors software engineers face when structuring Python projects into cleanly separated folders!

## The Problem
When you run `python src/nodes/filter.py`, Python sets the "Current Working Directory" for its import system to the folder where the script lives (`src/nodes/`).

When Python reads this line:
`from src.ingest.github import extract_github_internships`

It tries to look for a folder called `src` *inside* the `nodes` folder because that's where it thinks it is! Since there is no `src/nodes/src/ingest...`, it throws the `ModuleNotFoundError`.

## The Solution

There are two ways to fix this in the industry. The best way is to run the script as a **Python Module** from the root of the project.

Instead of running the file directly by its path (`python filepath.py`), you run it using the `-m` flag (which stands for module).

Run this exact command in your terminal while you are in the `InternshipScraper` directory:

```powershell
python -m src.nodes.filter
```

### Why does this work?
By using `python -m`, you are telling Python:
1. "Stay in this root `InternshipScraper` directory." (This becomes the base path).
2. "Look inside the `src` folder, then the `nodes` folder, and execute the `filter` module."

Because the base path is now `InternshipScraper`, when the script executes `from src.ingest.github import ...`, Python perfectly understands that `src` is sitting right there in the root directory!

### Minor Code Fixes
I noticed a few tiny typos in your `filter.py` file that would have caused the script to crash immediately after fixing the import! I went ahead and fixed them for you:
1. You were missing the import for `PromptTemplate` at the top of the file!
2. In the `prompt` string, you wrote `{location` instead of closing the bracket `{location}`.

**Try running `python -m src.nodes.filter` now and watch the AI do its work!**
