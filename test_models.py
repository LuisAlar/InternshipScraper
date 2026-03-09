import os
from dotenv import load_dotenv

# Load the environment variables from the src/.env file
load_dotenv("src/.env")

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("NO API KEY DETECTED! Ensure your key is in src/.env")
    exit(1)

print(f"API Key successfully loaded from src/.env! (Starts with: {api_key[:5]})")
print("Authenticating with Google...\n")

try:
    # Use the new google-genai SDK 
    from google import genai
    client = genai.Client(api_key=api_key)
    
    print("Authentication successful! Here are the 'flash' models you have access to:")
    models = client.models.list()
    
    found_flash = False
    for m in models:
        if "flash" in m.name.lower():
            print(f"- {m.name}")
            found_flash = True
            
    if not found_flash:
         print("No 'flash' models found for this account. Your API key might be restricted or in a region that doesn't support them.")

except Exception as e:
    print(f"\nError connecting to Google API:\n{e}")
