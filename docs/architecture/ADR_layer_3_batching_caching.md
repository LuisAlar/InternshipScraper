# Architecture Decision Record (ADR): Layer 3 Batching & Caching Strategy

## 1. Context
The `InternshipScraper` pipeline evaluates scraped internship postings to tailor recommendations based on a user's location preferences and resume experience. This evaluation process relies heavily on large language models (LLMs), specifically `gemini-1.5-pro`. Given the sheer volume of internships (e.g., thousands of roles) collected during the Extract phase, triggering an LLM reasoning task for *every individual internship* creates a 1:1 relationship between internships and LLM API calls.

This $O(N)$ architecture introduced severe bottlenecks:
- **Rate Limits Threshold:** The Gemini free tier has a strict rate limit of 5 Requests Per Minute (RPM) and a defined requests-per-day (RPD) quota.
- **Latency Issues:** The cumulative processing time grows linearly with the dataset.
- **Cost Implications:** Each prompt includes repetitive schema instructions and redundant text comparisons.

## 2. Decision
We are shifting the core evaluation architecture from a 1:1 $O(N)$ prompt mechanism to an $O(1)$ **Batching & Caching** methodology for Layer 3 (and potentially optimizing Layer 2's location semantic filtering).

The new workflow introduces three primary steps inside the LangGraph evaluate node:

1. **Deduplication (Python Layer)**
   - Prior to making any LLM call, the workflow extracts all *unique profiles* from the incoming dataset. 
   - A profile consists of an identifier composite (e.g., `job_title + company + requirements`).
   - If there are 1,500 internships, there may only be ~150 entirely distinct titles and role requirements across the dataset.

2. **Batch Prompting ($O(1)$ Strategy)**
   - The unique profiles are packaged into a single, comprehensive batch prompt.
   - The LLM receives the batch and is tasked with scoring every profile in the list against the user's resume, returning a structured JSON map.
   - Example Output Structure:
     ```json
     {
       "software_engineer_google": { "score": 95, "reasoning": "Strong match with React and Node.js..." },
       "database_intern_ibm": { "score": 70, "reasoning": "Lacks heavy SQL focus in resume..." }
     }
     ```

3. **Map Back (In-Memory Resolution)**
   - The response map is cached in memory.
   - The pipeline iterates through the original list of 1,500 internships.
   - For each internship, it queries the cache dictionary for the score and rationale, matching on the identifier, appending the result directly to the record in sub-millisecond time.

## 3. The "Profile Entity" Strategy
Based on an analysis of the extracted data (`filtered_matches.json`), the system currently only possesses the `company`, `role` (job title), `location`, `url`, and `date_posted`. 

Because actual job descriptions and technical requirements are not currently scraped, the LLM's evaluation is entirely based on comparing the **Job Title** against the user's **Resume**. Including the company name in the deduplication process is mathematically redundant: the LLM will score a "Software Engineer Intern" at Company A identically to Company B if the title is the only context provided.

### 3.1 Defining the Profile Entity (Title-Only Grouping)
We will create a `ProfileEntity` that acts as the deduplication key based strictly on the job title. Two internships will be considered "identical" for evaluation purposes if they share the same normalized title.

### 3.2 Hashing and Grouping Mechanism
1. **Normalization:** Convert the `role` (job title) to lowercase, remove emojis/punctuation, and strip whitespace. (e.g., "Software Engineer Intern 🎓" -> "software_engineer_intern").
2. **Hash Generation:** The normalized string *is* the unique identifier.
3. **The Map Bank:** In Python, iterate through the 1500+ internships.
   - Extract and normalize the role title.
   - If the sanitized title is new, add it to the `unique_profiles` list to be sent to the LLM.
4. **LLM Evaluation:** The LLM receives the `unique_profiles` list of distinct job titles. It returns a JSON map scoring how well each title aligns with the user's resume.
5. **Resolution:** Python loops through the 1500+ internships, normalizing their titles on the fly, and pulls the matching score from the cache dictionary.

## 4. Consequences
- **Maximum Deduplication:** By removing the company constraint, thousands of rows will condense into roughly 30-50 unique job titles (e.g., SWE Intern, Data Analyst Intern, QA Intern).
- **Extreme Cost Minimization:** Evaluating ~50 entities instead of 1,500 drops the token usage by over 95%, easily staying well beneath the Free Tier limits.
- **Future Proofing:** If a future scraper layer is built to actually fetch full job descriptions from the URLs, this hashing strategy will need to be updated to include extracted technical keywords to maintain accuracy.
