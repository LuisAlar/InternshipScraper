from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """
    Represents the state of the internship filtering workflow.
    """
    raw_internships: List[Dict[str, Any]]
    filtered_internships: List[Dict[str, Any]]
