# Part 3: Orchestration Layer (LangGraph Setup)

Welcome to Phase 2! We will now build the **Orchestration Layer** of your AI Automation system using **LangGraph**.

## 1. What is LangGraph?
LangGraph is a framework for building stateful, multi-agent workflows. Think of it as a state machine where:
*   **The State:** A dictionary or object that holds all the data over time (e.g., the raw internships, the filtered ones, and the final scored ones).
*   **The Nodes:** Python functions that perform specific work (like an AI agent fetching data, filtering data, or generating text). They read the current State, do their work, and update the State.
*   **The Edges:** The logic that connects the Nodes (e.g., Route A goes to Node B, Route C ends the workflow).

## 2. Defining the State (`core/state.py`)
In LangGraph, you must define the "State" object so every node knows exactly what data it's working with. Because we use Type Hinting, LangGraph strictly enforces this.

Open `src\core\state.py` and write the following:

```python
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """
    This is the global state that will be handed from node to node.
    Each node will read from it and write updates back to it.
    """
    raw_internships: List[Dict[str, Any]]      # Populated by the Ingestion Layer
    filtered_internships: List[Dict[str, Any]] # Populated by the Semantic Filter Node
    final_markdown: str                        # Populated by the Export Node
```

## 3. Building the Semantic Filter Node 
Now, we build the "Layer 2" LLM filter that will evaluate the `raw_internships` list. To save tokens and run extremely fast, we'll use `gpt-4o-mini` (or `gpt-3.5-turbo`) through LangChain.

Create a new file called `src\nodes\filter.py` and write the following code:

### Step 3.1: Setup and Validation
```python
import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

# We use Pydantic to force the LLM to output Structured Data (JSON) instead of a paragraph of text.
class FilterDecision(BaseModel):
    is_match: bool = Field(description="True if the location is purely in Texas (TX) or Remote. False otherwise.")
    reason: str = Field(description="A brief 1 sentence reason for the decision.")

def filter_internships_node(state: dict) -> dict:
    """
    LangGraph Node: Evaluates all raw internships and filters them by Location.
    """
    print("--- NODE: Filtering Internships ---")
    
    # 1. Grab the raw data from the LangGraph state
    internships = state.get("raw_internships", [])
    filtered_list = []
    
    if not internships:
        print("No internships to filter!")
        return {"filtered_internships": filtered_list}
        
    print(f"Beginning semantic filter on {len(internships)} roles...")
```

### Step 3.2: The LangChain LLM Logic
Now, add the brain! We initialize the LLM and pass each location to it to let it decide if it matches "Texas" or "Remote".

*Add this to the bottom of the `filter_internships_node` function:*
```python
    # 2. Initialize the fast, cheap LLM and ask it to return our Pydantic JSON structure
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(FilterDecision)
    
    # 3. Create the prompt we will send to the AI
    prompt = PromptTemplate(
        template="""You are a strict data filter. 
The user is ONLY looking for Software Engineering Internships located in Texas (TX) or that are Remote.
If a location mentions multiple states, but one of them is Texas or Remote, it IS a match.
If the location does not explicitly include Texas or Remote, it is NOT a match.

Location text: {location}""",
        input_variables=["location"]
    )
    
    # Create the runnable chain
    chain = prompt | structured_llm
    
    # 4. Loop through the internships and let the AI decide!
    # (For the MVP to avoid API rate limits, let's just test the first 10)
    test_batch = internships[:10]
    
    for item in test_batch:
        location_text = item.get("location", "Unknown")
        company = item.get("company", "Unknown")
        
        try:
            # Tell the AI to process this location
            decision = chain.invoke({"location": location_text})
            
            if decision.is_match:
                print(f"✅ KEEP: {company} ({location_text}) - {decision.reason}")
                filtered_list.append(item)
            else:
                print(f"❌ DROP: {company} ({location_text}) - {decision.reason}")
                
        except Exception as e:
            print(f"Error processing {company}: {e}")
            
    # 5. Return the updated data back to the LangGraph state!
    return {"filtered_internships": filtered_list}
```

## 4. Testing the Node

Let's test this in isolation before we wire up the full Graph! Add this test block to the bottom of `src\nodes\filter.py`:

```python
if __name__ == "__main__":
    # Import your scraper from earlier!
    from src.ingest.github import extract_github_internships
    
    # Make sure you have your API key loaded!
    from dotenv import load_dotenv
    load_dotenv()
    
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
```

## Next Steps
1. Make sure your `.env` file in `src/.env` has a valid `OPENAI_API_KEY`.
2. Run this script in your terminal: `python src/nodes/filter.py`
3. Watch the AI print out the reasons why it is keeping or dropping the internships based on location!
