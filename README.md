# Interview Coding Exercise — Meeting Transcript to User Stories

Welcome! This is a **brief coding exercise** designed to test your ability to turn unstructured input into structured, actionable output using Python.

---

## 🚀 Getting started

### Option A — GitHub Codespaces *(recommended)*

Opens a full VS Code environment in your browser — no installation required, just a GitHub account.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Guus-H/interview-case)

Once the Codespace has loaded (~30 seconds):

1. Open the terminal (`Ctrl+`` ` or **Terminal → New Terminal**)
2. Copy `.env.example` to `.env` and fill in the credentials your interviewer provided:
   ```bash
   cp .env.example .env
   ```
3. Open `.env`, replace the placeholder values, and save
4. You're ready — create a new `.py` file and start coding

---

### Option B — Google Colab *(alternative)*

If you prefer a notebook-style environment:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Guus-H/interview-case/blob/main/interview_exercise.ipynb)

Run the **Setup** cell first, then fill in your credentials in the **Credentials** cell before starting.

---

## Context

At our company we often capture requirements from meetings and translate them into user stories that are logged in ServiceNow. This exercise simulates that workflow.

You have been given a recording of an internal requirements meeting about building an **employee self-service portal**. The meeting was real-world messy — people interrupted each other, went off-topic, and circled back. Your job is to build a tool that makes sense of it.

---

## What is available to you

| File / Folder | Description |
|---|---|
| `transcripts/` | The meeting transcript in two formats: `.vtt` (Teams export) and `.docx` (Word) — pick one |
| `user_story_definition.md` | The format and fields expected for a valid user story |
| `snippets/` | A folder of potentially useful code snippets — feel free to use them |
| `output/` | Put your output here |

---

## Part 1 — Transcript to Structured User Stories

**Your task:** Build a Python script that:

1. Ingests the meeting transcript (`.vtt` or `.docx` — your choice)
2. Extracts the functional requirements that were discussed
3. Outputs them as well-formed user stories in a structured format

A valid user story must match the format described in `user_story_definition.md`.

**Accepted output formats:** JSON, CSV, or any other structured format you prefer.

> Before you start coding: the interviewer will ask you to briefly describe your intended approach. Take a moment to think it through first.

---

## Part 2 — Create Stories in ServiceNow *(bonus)*

If you complete Part 1 with time to spare, extend your script to push the user stories directly into ServiceNow using the Table API.

- Target table: `rm_story`
- Field mapping is described in `user_story_definition.md`
- Credentials are available in your `.env` file (Codespaces) or the Credentials cell (Colab)
- There is a code snippet in `snippets/` that shows how to interact with the ServiceNow Table API

---

## Tips

- You do not need to handle every edge case — focus on getting a working solution
- Reusability matters: think about how this tool could be used for future meetings, not just this one
- The `snippets/` folder is there to help — you are free to use, adapt, or ignore them
- Put your output in the `output/` folder

---

## Note on the SOLUTION folder

A reference solution is included in the `SOLUTION/` folder. Please do not look at it during the exercise — it is there for the interviewer. Give it your own shot first!
