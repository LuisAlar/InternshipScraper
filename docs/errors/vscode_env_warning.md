# VS Code `useEnvFile` Warning & Gemini 404 Errors

You are seeing a notification in your terminal that says: Include `python.terminal.useEnvFile` to use environment variables...

## 1. What does this warning mean?
This is actually a **VS Code specific warning**, not a Python error! 
VS Code has a feature where it tries to automatically inject your `.env` variables directly into the PowerShell terminal as soon as you open it. However, because our file is inside the `src/` folder (and not the root), VS Code is confused. 

**The Good News:** You don't actually need to enable this! Because we wrote `load_dotenv("src/.env")` inside our Python script, Python is manually opening the file and grabbing the key perfectly fine, bypassing the terminal completely. 

*If you want to make the warning go away anyway:*
1. Press `Ctrl + ,` to open VS Code Settings.
2. Search for: `python.terminal.useEnvFile`
3. Check the box.

## 2. Why is the script still crashing with `404 NOT FOUND`?
If LangChain couldn't find your `.env` key, it would crash instantly with an `Unauthorized` or `Missing API Key` error. 

**Because you are getting a `404 NOT_FOUND` error, it means your API key IS working perfectly!** Python successfully logged into your Google account, but when it asked Google to use the model `"gemini-1.5-flash"`, Google replied: "I don't have a model by that name for this account."

Google frequently updates their model names (e.g., `gemini-1.5-flash`, `gemini-1.5-flash-latest`, `gemini-2.0-flash`). Depending on when your API key was generated and your region, you have access to different names!

## 3. The Solution
I have written a diagnostic script in your root folder called `test_models.py`. Run this script! It will log into Google with your API key, ask Google "Which Gemini Flash models do I have access to?", and print out the exact string we need to put into `filter.py`.
