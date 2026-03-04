"""
SOLUTION — Meeting Transcript to ServiceNow User Stories

End-to-end script that:
  1. Loads a meeting transcript (.vtt or .docx)
  2. Strips it to clean text
  3. Calls OpenAI to extract user stories in structured JSON
  4. Saves output as JSON and CSV to the output/ folder
  5. Optionally pushes stories into ServiceNow (rm_story table)

Usage:
    python SOLUTION/solution.py                                     # uses VTT by default
    python SOLUTION/solution.py transcripts/meeting_transcript.vtt
    python SOLUTION/solution.py transcripts/meeting_transcript.docx
    python SOLUTION/solution.py transcripts/meeting_transcript.vtt --servicenow
"""

import os
import re
import sys
import json
import csv
import requests
from requests.auth import HTTPBasicAuth
from openai import OpenAI
from dotenv import load_dotenv

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SN_INSTANCE = os.getenv("SN_INSTANCE")
SN_USERNAME  = os.getenv("SN_USERNAME")
SN_PASSWORD  = os.getenv("SN_PASSWORD")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are a business analyst assistant specialising in agile requirements.
You will receive a meeting transcript. Your task is to identify every distinct
functional requirement discussed and convert each one into a well-formed user story.

Return a JSON object with a single key "user_stories" containing an array of objects.
Each object must have exactly these three fields:

- "short_description": A one-line title in the format
  "As a [user type], I want [goal] so that [benefit]."
  Maximum 80 characters. Be specific and user-facing.

- "description": 2–4 sentences providing context, rationale, and any constraints
  mentioned in the meeting. Written in plain English.

- "acceptance_criteria": An array of 3–5 strings. Each string is a specific,
  independently testable condition. Use plain statements (not Given/When/Then).

Rules:
- Only include clearly functional requirements — things to be built.
- Do NOT include UI preferences, design opinions, or unresolved debates
  (e.g. button placement discussions are not user stories).
- Do NOT include meeting logistics (scheduling, follow-ups).
- If a requirement was discussed across multiple parts of the conversation,
  consolidate it into one story.

Return only valid JSON. No markdown, no explanation.
"""

# ---------------------------------------------------------------------------
# Transcript loading
# ---------------------------------------------------------------------------

def load_vtt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"^WEBVTT[^\n]*\n", "", content, flags=re.MULTILINE)
    content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}[^\n]*\n", "", content)
    content = re.sub(r"^\d+\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"<v ([^>]+)>(.*?)</v>", r"\1: \2", content)
    content = re.sub(r"<[^>]+>", "", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def load_docx(filepath: str) -> str:
    if DocxDocument is None:
        raise ImportError("python-docx is not installed. Run: pip install python-docx")
    doc = DocxDocument(filepath)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def load_transcript(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".vtt":
        return load_vtt(filepath)
    elif ext == ".docx":
        return load_docx(filepath)
    else:
        raise ValueError(f"Unsupported file type '{ext}'. Provide a .vtt or .docx file.")

# ---------------------------------------------------------------------------
# LLM extraction
# ---------------------------------------------------------------------------

def extract_user_stories(transcript: str) -> list[dict]:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("user_stories", [])

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_json(stories: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    print(f"  Saved JSON  → {path}")


def save_csv(stories: list[dict], path: str) -> None:
    if not stories:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["short_description", "description", "acceptance_criteria"])
        writer.writeheader()
        for story in stories:
            row = story.copy()
            ac = row.get("acceptance_criteria", [])
            row["acceptance_criteria"] = "\n".join(ac) if isinstance(ac, list) else ac
            writer.writerow(row)
    print(f"  Saved CSV   → {path}")

# ---------------------------------------------------------------------------
# ServiceNow
# ---------------------------------------------------------------------------

def _sn_headers() -> dict:
    return {"Content-Type": "application/json", "Accept": "application/json"}


def insert_story(story: dict) -> dict:
    ac = story.get("acceptance_criteria", [])
    payload = {
        "short_description": story["short_description"],
        "description": story["description"],
        "acceptance_criteria": "\n".join(ac) if isinstance(ac, list) else ac,
    }
    url = f"{SN_INSTANCE}/api/now/table/rm_story"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
        headers=_sn_headers(),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["result"]


def push_to_servicenow(stories: list[dict]) -> None:
    print(f"\nPushing {len(stories)} stories to ServiceNow (rm_story)...")
    for story in stories:
        result = insert_story(story)
        print(f"  Created {result.get('number', '?')} — {result.get('short_description', '')}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    transcript_path = "transcripts/meeting_transcript.vtt"
    push_sn = False

    for arg in sys.argv[1:]:
        if arg == "--servicenow":
            push_sn = True
        elif not arg.startswith("--"):
            transcript_path = arg

    print(f"Loading transcript: {transcript_path}")
    transcript = load_transcript(transcript_path)

    print("Calling OpenAI to extract user stories...")
    stories = extract_user_stories(transcript)
    print(f"Extracted {len(stories)} user stories.\n")

    save_json(stories, os.path.join(OUTPUT_DIR, "user_stories.json"))
    save_csv(stories,  os.path.join(OUTPUT_DIR, "user_stories.csv"))

    if push_sn:
        push_to_servicenow(stories)
    else:
        print("\nTip: add --servicenow to push stories directly into ServiceNow.")


if __name__ == "__main__":
    main()
