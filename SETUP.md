# Interviewer Setup Notes

This file is for the interviewer only. Do not share with the candidate.

---

## One-time setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate the DOCX transcript** (the VTT file is already in the repo)
   ```bash
   python setup/generate_docx.py
   ```
   This creates `transcripts/meeting_transcript.docx`.

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in the OpenAI API key and ServiceNow credentials
   - On Replit: add these as Secrets (not in the `.env` file directly)

---

## How to run the interview

### Opening (2 min)
Briefly introduce the context: we turn messy meeting transcripts into user stories for ServiceNow. Show them the README and give them a moment to read it.

### Step 1 — Approach first (3–5 min)
**Before** handing over the OpenAI API key, ask:

> "How would you approach building this? What steps would your script go through?"

Listen for:
- Do they identify the parsing problem (VTT/DOCX → clean text)?
- Do they think about how to extract *structured* output from *unstructured* text?
- Do they consider reusability / parameterization?

After they've shared their approach, let them know an OpenAI API key is available in the environment (`.env` / Replit Secrets).

### Step 2 — Coding (8–10 min)
Let them work. They have access to:
- The transcript files
- The user story definition
- The snippets folder (hint at its existence if they seem stuck)

You are looking for:
- Practical judgment (which file format to pick, why)
- Ability to prompt an LLM effectively
- Clean, readable Python code
- Structured output (JSON or CSV) that maps to the user story fields

### Step 3 — Bonus: ServiceNow (remaining time)
If they finish Part 1 early, direct them to Part 2. The ServiceNow snippet is a close analog to what they need — the main change is the table name (`rm_story`) and the fields.

---

## What to look for

| Signal | Green flag | Yellow flag |
|---|---|---|
| File format choice | Explains reasoning (VTT is cleaner) | Just picks one without thinking |
| LLM prompting | Clear system prompt, asks for JSON | Vague prompt, no structure |
| Output format | JSON or CSV with correct fields | Works but hard to reuse |
| Code quality | Functions, readable variable names | One big script, no structure |
| Reusability | Parameterized filepath, could handle any transcript | Hardcoded paths |
| Part 2 | Adapts the snippet confidently | Needs step-by-step guidance |

---

## The 4 requirements in the transcript

The meeting discusses these four portal features (not in this order, and not neatly):

1. **Personalized Homepage** — dashboard with announcements widget, open requests summary, and role-based quick links
2. **Service Request Catalog** — browse categories, dynamic forms, file attachments, free-text notes
3. **Knowledge Base** — searchable, categorized articles with helpfulness rating; suggests articles when submitting a request
4. **My Approvals Dashboard** — managers can see, approve/reject pending approvals with mandatory comments; overdue items highlighted

There is also a side discussion about the submit button position (top-right vs sticky footer) — this is *not* a functional requirement and should ideally not appear as a user story. It's a good conversation starter if the candidate includes it.
