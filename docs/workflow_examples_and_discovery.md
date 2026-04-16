# Sales AI Workflow Examples & Discovery Questions

If the interviewers ask you to build a workflow on the spot, or ask for examples of what you *could* build, this is your playbook. 

**Never just start solving the problem immediately.** That’s what a junior scripter does. An engineer and architect asks **discovery questions** first to define the scope, constraints, and edge cases.

---

## 1. Discovery Questions (To ask *before* you design the workflow)

If they say, *"Luis, how would you design a workflow to help our reps follow up with clients?"*

Respond with: *"Before I design the architecture, I need to define the constraints of the system. Let me ask a few discovery questions:"*

**Data & Integration Questions:**
*   "What is our primary data source? Are we pulling from Salesforce, a SQL database, or unstructured emails?"
*   "Do we have API rate limits we need to worry about with our LLM provider (e.g., OpenAI or Anthropic)?"

**Logic & Edge Case Questions:**
*   "What is the definition of a 'qualified lead' in this scenario? If the data is ambiguous, what is the default fallback behavior of the workflow?"
*   "If the workflow encounters an error (e.g., the CRM API times out), should it retry automatically, or alert a human?"

**User Experience (The "Human Feature") Questions:**
*   "Are we automatically sending this follow-up email, or are we drafting it and having a Human-in-the-Loop review it before sending?"
*   "Where does the sales rep prefer to receive this output? Slack? A CRM dashboard? Email?"

***By asking these questions, you instantly prove you think like a software engineer handling requirements, not just a drag-and-drop tool user.***

---

## 2. Examples of High-Value Sales AI Workflows

Here are three heavily utilized AI workflows in enterprise sales that you can confidently pitch.

### Example A: The "Pre-Meeting Intelligence Brief" (Research Automation)
*   **The Problem:** Sales reps spend 30-45 minutes researching a prospect before an introductory call.
*   **The Workflow:**
    *   **Trigger:** A calendar event is created with an external email address.
    *   **Action (Data Fetch):** The workflow scrapes the prospect's LinkedIn profile, company website, and the company's last public earnings call or news mentions.
    *   **Action (AI Agent):** An LLM summarizes this unstructured data.
    *   **Output:** 15 minutes before the call, the workflow sends a 3-bullet-point summary to the rep via Slack: (1) Company's recent strategic shift, (2) Prospect's background, (3) Suggested opening question.
*   **Why it's good:** It saves 30 minutes per meeting and is entirely internal (low risk—no AI is talking directly to the client).

### Example B: The "Post-Call CRM Updater" (Administrative Automation)
*   **The Problem:** Sales reps hate updating Salesforce. Notes are often sparse, leading to bad data downstream.
*   **The Workflow:**
    *   **Trigger:** A Zoom/Teams meeting ends.
    *   **Action (Data Fetch):** The workflow grabs the auto-generated transcript of the call.
    *   **Action (AI Agent):** The LLM is prompted to strictly extract: The client's main pain point, the proposed solution, budget constraints, and next steps.
    *   **Action (HITL & Logic):** The workflow drafts an update to the respective Salesforce fields. A Slack message is sent to the rep: *"Here is the extracted CRM data. Approve?"*
    *   **Output:** Upon the rep's click, Salesforce is updated perfectly.
*   **Why it's good:** It solves the biggest data hygiene issue in sales and uses your HITL architecture. 

### Example C: The "Intent Signal Lead Router" (Event-Driven Pipeline)
*   **The Problem:** A company gets 500 inbound leads a day, but only 20 are actually ready to buy. Human SDRs (Sales Development Reps) waste time calling bad leads.
*   **The Workflow:**
    *   **Trigger:** A new lead fills out a form on the website.
    *   **Action (Data Fetch):** The workflow cross-references the lead's company domain with an API like Clearbit or ZoomInfo to get company size and revenue.
    *   **Action (AI Agent):** The LLM scores the lead from 1-100 based on how closely they match the Ideal Customer Profile (ICP).
    *   **Logic Branch:** 
        *   If score > 80: Immediately assign to a senior Account Executive and trigger a high-priority Slack alert.
        *   If score < 80: Drop them into an automated, low-touch email nurture sequence.
*   **Why it's good:** It uses Event-Driven Architecture and conditional logic to impact top-line revenue by prioritizing the highest-value prospects instantly.

---

## Summary for the Interview

If they ask you to design something, **pick Example B (The Post-Call CRM Updater)**. It allows you to showcase all your core concepts:
1.  **Ambiguity resolution:** Taking unstructured call transcripts and making them structured CRM data.
2.  **Human-in-the-Loop:** Sending the summary to Slack for approval before touching the database.
3.  **Decoupled Architecture:** The fact that the AI engine processes the data, but the interface the human uses to approve it is Slack.
