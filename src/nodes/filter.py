import os
import json
import re
from typing import Dict,Any,List

def is_location_match(location: str) -> bool:
    """
    Evaluates if a location string matches the criteria: Texas (TX) or Remote.
    """
    if not location or location == "Unknown":
        return False
        
    location_lower = location.lower()
    
    # Check for remote
    if "remote" in location_lower:
        return True
        
    # Check for Texas using regex to match whole words like 'tx' or 'texas'
    # We use regex \b to ensure we don't accidentally match 'tx' inside another word
    if re.search(r'\b(tx|texas)\b', location_lower):
        return True
        
    return False

def filter_internships_node(state: dict) -> dict: 
    print("--- NODE: Filtering Internships (Python Regex) ---")

    # grab the raw data from the langgraph state
    internships = state.get("raw_internships",[])

    if not internships:
        print("No internships to filter!")
        return {"filtered_internships": []}
        
    print(f"Beginning Python location filter on {len(internships)} roles...")

    filtered_list = []

    for item in internships:
        loc = item.get("location", "Unknown")
        company = item.get("company", "Unknown")
        
        if is_location_match(loc):
            filtered_list.append(item)
            
    print(f"Done filtering. Found {len(filtered_list)} matches.")
    
    # Export it to a JSON file so you can inspect the matches!
    try:
        with open("filtered_matches.json", "w", encoding="utf-8") as f:
            json.dump(filtered_list, f, indent=4)
        print("Successfully saved matches to 'filtered_matches.json'!")
    except Exception as e:
        print(f"Could not save JSON: {e}")

    # Return the updated data back to the LangGraph state
    return {"filtered_internships": filtered_list}

if __name__ == "__main__":
    # Import your scraper from earlier!
    from src.ingest.github import extract_github_internships
    
    # Make sure you have your API key loaded!
    from dotenv import load_dotenv
    load_dotenv("src/.env")
    
    # 1. Run the scraper
    print("Getting raw data...")
    raw_data = extract_github_internships()
    
    # 2. Create a fake "State" dictionary manually to simulate LangGraph
    mock_state = {
        "raw_internships": raw_data
    }
    
    # 3. Run our new Node!
    result_state = filter_internships_node(mock_state)
    
    print("\n--- Final Filtered Results ---")
    print(f"Successfully filtered down to {len(result_state['filtered_internships'])} matches!")
