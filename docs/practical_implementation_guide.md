# How Low-Code AI Workflows Are Built in Practice

If Jordan (the Sales Engineer) asks you, "How would you actually *build* this?" you need to be able to walk him through the tangible, practical steps. This document outlines the modern tech stack and the step-by-step logic used in enterprise sales floors today.

## 1. The Platforms Used (The "Low-Code" Stack)
When 1finity says "low-code," they are likely referring to one of two categories of platforms:

*   **Enterprise Integration Platforms (iPaaS):** 
    *   *Examples:* Microsoft Power Automate, Make (formerly Integromat), SnapLogic, Workato, Appian, OutSystems.
    *   *What they do:* These have deep, native integrations into CRMs (like Salesforce) and Enterprise software (like Microsoft 365). They are secure and compliant.
*   **Orchestration / Node-Based Builders:**
    *   *Examples:* n8n (popular for self-hosting and AI agent building), Zapier, Vertex AI Agent Builder.
    *   *What they do:* Provide visual, drag-and-drop canvases where you connect "nodes" (Triggers, API calls, AI models, Actions) via physical lines on the screen.

## 2. The Practical Step-by-Step Workflow Build
Here is the exact lifecycle of how a sales workflow is developed on these platforms. **Memorize these 5 steps** to sound like a seasoned developer in this space.

### Step 1: The Trigger (Event-Driven Architecture in Action)
Every workflow needs a starting point. In the visual canvas, you drag a "Trigger Node."
*   *Practical Example:* A web-hook listens for a state change in Salesforce. The trigger is: `"Lead Status changed to 'Meeting Booked'."`

### Step 2: Data Fetching & Context Gathering
The AI agent needs context before it can reason. You add API nodes to fetch data.
*   *Practical Example:* The workflow automatically pulls the prospect's LinkedIn profile, company news from a SERP API, and the history of their previous emails from the CRM.

### Step 3: The AI "Brain" Node (LLM Integration)
This is where the agentic reasoning happens. You drag an "OpenAI / Anthropic" node onto the canvas. Instead of writing Python scripts, you provide a "System Prompt" inside the node's settings.
*   *Practical Example:* You configure the node: `"Take the LinkedIn profile and CRM history provided. Draft a highly personalized, 3-paragraph summary preparing the sales rep for their 1PM meeting."`

### Step 4: The Human-in-the-Loop (HITL) Checkpoint
*This is where your software engineering architecture shines.* Instead of acting immediately, the workflow pauses.
*   *Practical Example:* The workflow sends a slack message to the assigned Sales Rep with the AI's drafted summary. The Slack message has two buttons: **[Approve & Save to CRM]** or **[Reject. Send to me for editing]**.

### Step 5: The Final Action (Integration)
Based on the human's decision, the workflow branches and executes the final API call.
*   *Practical Example:* If approved, an HTTP Request node or native CRM node pushes the final summary into the Salesforce 'Meeting Notes' field.

## 3. How to Frame This in the Interview

If Jordan asks about implementation, you can say:

> *"In practice, I know we'll be using visual node-based platforms like Microsoft Power Automate, Make, or OutSystems to build these flows. But connecting a trigger to an LLM node is the easy part.*
> 
> *The real engineering comes into play with what happens between those nodes. For example, how do we handle data sanitization before it hits the LLM? What is the branching logic if the CRM API Times Out? Where do we place the Human-in-the-Loop checkpoint to ensure a hallucinated email isn't automatically sent?*
> 
> *My approach is to use the low-code platform canvas to map out the business logic, but apply my software engineering mindset to handle rate limits, testing, and error recovery—ensuring the workflow doesn't just look good on the canvas, but actually survives in production."*
