import json
import csv
import os

def export_json_to_csv(json_filepath: str, csv_filepath: str):
    """
    Reads a JSON file of internships and converts it to a CSV file.
    Adds custom columns for application tracking: 'Applied', 'Status', and 'Notes'.
    """
    if not os.path.exists(json_filepath):
        print(f"Error: {json_filepath} not found. Please make sure the filtering ran successfully.")
        return

    print(f"Reading {json_filepath}...")
    
    with open(json_filepath, 'r', encoding='utf-8') as f:
        try:
            internships = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {json_filepath} is not a valid JSON file.")
            return

    if not internships:
        print("No internships to export.")
        return

    print(f"Exporting {len(internships)} internships to {csv_filepath}...")

    # We want to add these columns to the standard data from the scraper
    headers = [
        "company", 
        "role", 
        "location", 
        "link", 
        "date_posted",
        "Applied",      # Blank column for user tracking (e.g., Yes/No)
        "Status",       # Blank column for user tracking (e.g., Applied, Interview, Rejected)
        "Notes"         # Blank column for user tracking
    ]

    try:
        with open(csv_filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
            
            # Write the column headers to the top of the file
            writer.writeheader()
            
            # Write each internship row. 
            # We initialize our custom tracking columns as empty strings so the CSV has empty cells for them.
            for item in internships:
                # Prepare row data, defaulting missing keys to empty strings
                row = {
                    "company": item.get("company", ""),
                    "role": item.get("role", ""),
                    "location": item.get("location", ""),
                    "link": item.get("link", ""),
                    "date_posted": item.get("date_posted", ""),
                    "Applied": "",
                    "Status": "",
                    "Notes": ""
                }
                writer.writerow(row)
                
        print(f"Successfully created {csv_filepath}!")
        print("You can now open this file in Excel, Google Sheets, or Numbers to track your applications.")

    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    # Define file paths. Assuming they run this from the project root.
    JSON_FILE = "filtered_matches.json"
    CSV_FILE = "application_tracker.csv"
    
    export_json_to_csv(JSON_FILE, CSV_FILE)
