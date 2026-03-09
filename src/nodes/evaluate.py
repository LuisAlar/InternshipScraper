import json
import os
from src.core.evaluator_batch import normalize_title, extract_unique_profiles

def evaluate_internships_node(state: dict) -> dict:
    print("--- NODE: Evaluating Internships (Layer 3 Batch Processing) ---")
    
    # In full LangGraph, this would be state.get("filtered_internships", [])
    # For local testing, we might pass in the raw JSON
    internships = state.get("filtered_internships", [])
    
    if not internships:
        print("No internships to evaluate!")
        return {"evaluated_internships": []}
        
    print(f"Received {len(internships)} total internships.")
    
    # 1. Deduplcation Phase
    unique_map = extract_unique_profiles(internships)
    print(f"Extracted {len(unique_map)} UNQIUE job titles for evaluation.")
    
    # For now, let's just print them so we can verify before we build the LLM call!
    print("\n--- Unique Job Titles Discovered ---")
    
    # We only need to send the ACTUAL titles to the LLM, not the hash keys
    unique_titles_list = list(unique_map.values())
    
    # For local debugging, we limit printing so it doesn't flood the console
    for profile_hash, original_title in list(unique_map.items())[:5]:
        safe_title = original_title.encode('ascii', 'ignore').decode('ascii')
        print(f" - [{profile_hash}]: '{safe_title}'")
    print(f" ... and {len(unique_titles_list) - 5} more.")
        
    print("\n--- 2. Batch LLM Evaluation Phase ---")
    try:
        # 1. Grab resume (this should ideally be passed in via State, but loading here for MVP)
        resume_path = "resumes/luis_Alarcon_se.tex"
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_content = f.read()
            
        from src.core.evaluator_batch import ResumeBatchEvaluator
        evaluator = ResumeBatchEvaluator(resume_content)
        
        # 2. Fire the SINGLE prompt! O(1) Architecture
        print("Sending batch evaluation request to Gemini-1.5-Pro (this may take 10-20 seconds)...")
        evaluation_map = evaluator.evaluate_batch(unique_titles_list)
        print(f"Successfully evaluated {len(evaluation_map)} unique titles!")
        
    except Exception as e:
        print(f"Error during LLM Batch Evaluation: {e}")
        return {"evaluated_internships": []}
        
    print("\n--- 3. Map Resolution Phase (O(N) Python Loop) ---")
    evaluated_list = []
    
    # Iterate through the original 185 internships instantly
    for item in internships:
        title = item.get("role", "")
        # Look up the score the LLM gave this title
        evaluation = evaluation_map.get(title, {"score": 0, "reasoning": "Failed to map title."})
        
        # Merge the evaluation directly into the internship dictionary
        scored_item = {**item, **evaluation}
        evaluated_list.append(scored_item)
        
    print(f"Done! Successfully mapped scores back to all {len(evaluated_list)} internships in milliseconds.")
    
    # Export it to a JSON file so you can inspect the matches!
    try:
        import json
        with open("evaluated_matches.json", "w", encoding="utf-8") as f:
            json.dump(evaluated_list, f, indent=4)
        print("Successfully saved matches to 'evaluated_matches.json'!")
    except Exception as e:
        print(f"Could not save JSON: {e}")
        
    return {"evaluated_internships": evaluated_list}

if __name__ == "__main__":
    # Test script to run the deduplication on our filtered matches JSON locally
    # without making any LLM API calls yet.
    
    json_path = "filtered_matches.json"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Please run the filter node first.")
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)
            
        mock_state = {
            "filtered_internships": test_data
        }
        
        # Run just the deduplication logic to verify it works
        evaluate_internships_node(mock_state)
