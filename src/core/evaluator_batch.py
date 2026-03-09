import re

def normalize_title(title: str) -> str:
    """
    Normalizes a job title to create a unique hash key.
    Converts to lowercase, removes emojis/special chars, and strips trailing spaces.
    e.g. 'Software Engineer Intern 🎓' -> 'software_engineer_intern'
    """
    if not title:
        return "unknown"
    
    # 1. Lowercase
    normalized = title.lower()
    
    # 2. Remove emojis and special characters (keep alphanumeric and spaces)
    # This regex replaces anything that isn't a letter, number, or space with nothing
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    
    # 3. Replace multiple spaces with a single underscore, strip leading/trailing
    normalized = re.sub(r'\s+', '_', normalized.strip())
    
    return normalized

def extract_unique_profiles(internships: list) -> dict:
    """
    Takes a list of internship records and returns a dictionary 
    mapping the unique 'hash' to the original title string.
    """
    unique_profiles = {}
    
    for item in internships:
        title = item.get("role", "")
        profile_hash = normalize_title(title)
        
        # Only add it if we haven't seen this exact hash before
        if profile_hash not in unique_profiles:
            unique_profiles[profile_hash] = title
            
    return unique_profiles

# ----------------- LLM EVALUATION ----------------- #
from typing import Dict, List, Any
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load API keys
load_dotenv("src/.env")

class JobEvaluation(BaseModel):
    score: int = Field(description="A strict match score from 0-100 indicating how well the job title aligns with the resume's experience.")
    reasoning: str = Field(description="A 1-sentence explanation for the score assigned.")

class BatchEvaluationResponse(BaseModel):
    results: Dict[str, JobEvaluation] = Field(description="A dictionary mapping the EXACT job title string provided to its evaluation.")

class ResumeBatchEvaluator:
    def __init__(self, resume_text: str):
        self.resume_text = resume_text
        # We use gemini-1.5-pro-latest for deep reasoning tasks like resume matching
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.0
        ).with_structured_output(BatchEvaluationResponse)
        
        self.prompt = PromptTemplate.from_template(
            """You are an elite Tech Recruiter AI.

YOUR OBJECTIVE:
Evaluate a list of Unique Job Titles against a candidate's resume.

CANDIDATE RESUME:
{resume}

LIST OF JOB TITLES TO EVALUATE:
{titles_list}

INSTRUCTIONS:
For every single job title provided in the list, generate a match score (0-100) based purely on how well the title aligns with the core focus of the candidate's resume (e.g. Software Engineering vs Marketing). Do not skip any titles.
Return your answer in the requested structured JSON format, where the key is the exact job title string provided.
"""
        )

    def evaluate_batch(self, unique_titles: List[str]) -> Dict[str, dict]:
        """
        Takes a list of unique title strings and returns a map of scores.
        """
        # Format the list of titles into a readable string
        titles_formatted = "\n".join([f"- {title}" for title in unique_titles])
        
        # Invoke the LLM with structured output
        chain = self.prompt | self.llm
        response: BatchEvaluationResponse = chain.invoke({
            "resume": self.resume_text,
            "titles_list": titles_formatted
        })
        
        # Convert Pydantic objects back to raw dicts for easy merging
        return {
            title: {"score": eval_obj.score, "reasoning": eval_obj.reasoning} 
            for title, eval_obj in response.results.items()
        }
