"""
Snippet 01 — Calling OpenAI with unstructured input and getting structured JSON back.

This example extracts structured action items from a freeform email.
The pattern (system prompt + json_object response format) is reusable for
any task where you want to convert unstructured text into structured data.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- The unstructured input ---
email_text = """
Hi team,

Quick follow-up from our call this morning.

David needs to share the updated network diagram with the security team before Thursday.
We agreed that Anna will reach out to the vendor about the license renewal — she said she'd
handle it by end of next week. Also, the infra team should schedule a maintenance window
for the storage migration; Marcus mentioned Friday night works if it's confirmed by Wednesday.

Let me know if I missed anything.

Cheers,
Rob
"""

# --- System prompt: tell the model exactly what structure you want ---
SYSTEM_PROMPT = """
You are an assistant that extracts action items from emails or meeting notes.

Return a JSON object with a single key "action_items" containing an array of objects.
Each object must have these fields:
- "owner": the person responsible (string)
- "task": a concise description of what needs to be done (string)
- "due_date": the deadline if mentioned, otherwise null (string or null)

Return only valid JSON. Do not include any explanation or markdown.
"""

# --- Make the API call ---
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": email_text},
    ],
    response_format={"type": "json_object"},  # guarantees valid JSON output
)

# --- Parse and use the result ---
result = json.loads(response.choices[0].message.content)

print(json.dumps(result, indent=2))

# Example output:
# {
#   "action_items": [
#     { "owner": "David", "task": "Share updated network diagram with security team", "due_date": "Thursday" },
#     { "owner": "Anna", "task": "Contact vendor about license renewal", "due_date": "end of next week" },
#     { "owner": "Marcus", "task": "Confirm and schedule storage migration maintenance window", "due_date": "Wednesday" }
#   ]
# }
