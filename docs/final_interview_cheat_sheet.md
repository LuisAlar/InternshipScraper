# Final Interview Cheat Sheet: The "Humans as a Feature" Strategy

Review this document 10 minutes before you get on the interview ping.

## 1. The Core Narrative (Your Brand)
*   **The Pitch:** "I am a software engineer approaching low-code. I build workflows that solve problems for humans. Low-code determines *how fast* we build; software engineering architecture determines *if it breaks* and *if sales reps actually use it*."
*   **The Philosophy:** Humans are a feature, not a bug. Ambiguity is handled by Decoupled Architecture, allowing the workflow to adapt to the rep's unique style rather than forcing the rep to adapt to a monolithic workflow.

## 2. The 3 Stories (STAR Method)
Use these when asked about experience or how you handle ambiguity:
1.  **Indigo Magazine (Unstructured Data/Ambiguity):** Turned messy, unstructured media inputs into a predictable, zero-friction pipeline to Cloudflare/Box.
2.  **Orbital Mentorship (Discovery/Friction):** Decreased onboarding friction by 50% by building an API observability layer to expose ambiguous, hidden backend metrics.
3.  **YourOwn (Trust/Edge Cases):** Built automated validation around AI-generated test suites because you never blindly trust AI output; you engineer guardrails around it.

## 3. The Technical Terms to Drop
When they ask how you'd build a workflow or handle an issue, naturally weave in:
*   **Human-In-The-Loop (HITL):** "I’d architect a HITL checkpoint before the AI sends an email to prevent hallucination risks."
*   **Headless / Decoupled Architecture:** "We should build one central AI engine and serve it across multiple detached interfaces (Slack, CRM) depending on the rep's preference."
*   **Event-Driven Architecture:** "The workflow should be triggered by intent signals (CRM updates, lead forms), not manual clicks."
*   **Fallback Logic / Rate Limiting:** "Between the low-code nodes, I apply my SWE background to handle API rate limits and build fallback logic for when external LLMs time out."

## 4. Discovery Questions to Ask Them
If asked to design something on the spot:
*   *"Before I establish the architecture, what is our primary data source, and what are our API rate limits?"*
*   *"What is the fallback logic if the AI misinterprets the data?"*
*   *"Where does the sales rep prefer to receive this output to minimize friction?"*

---

# What NOT to Say (To Maintain Your Strategy)

This narrative works because it is mature and high-level. To protect it, avoid these conversational traps:

### 1. DON'T pivot the conversation to deep code syntax.
*   **Why:** They explicitly said they don't want a traditional CS major holding onto pure coding. They want business value.
*   **What to say instead:** If they ask a technical question, answer with *architecture* (how systems connect) rather than *syntax* (how a specific python loop works).

### 2. DON'T bash low-code platforms.
*   **Why:** You might be tempted (as an engineer) to talk about how limited drag-and-drop tools are compared to raw code. This is a trap. They chose low-code for a reason (speed, cost).
*   **What to say instead:** "Low-code is an incredibly powerful execution layer for speed to market. My job is to bring the structural rigor to ensure that speed doesn't create technical debt."

### 3. DON'T claim AI can perfectly automate a salesperson's job.
*   **Why:** The interviewers (especially the Executive Sponsor) know that sales requires ultimate human empathy. If you suggest building a fully autonomous, zero-human-contact sales agent, you will sound naive to how enterprise B2B sales actually works.
*   **What to say instead:** Pitch "Agentic Assistance" or "Human-in-the-Loop." The AI does the heavy lifting (research, data entry, drafting), but the human is the final, empathetic decision-maker.

### 4. DON'T just "agree" if they propose a rigid, monolithic workflow.
*   **Why:** If Jordan suggests an idea that forces every single sales rep to use a clunky new dashboard they will hate, don't just say "Yes, I can build that."
*   **What to say instead:** Push back respectfully using your philosophy. *"Yes, we can build that dashboard. However, knowing that adoption is our biggest hurdle, what if we decoupled the backend and delivered the exact same AI insights via a Slack bot for reps who prefer that interface? We get the same data outcome but higher adoption."*
