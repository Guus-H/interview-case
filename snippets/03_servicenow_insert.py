"""
Snippet 03 — Inserting records into a ServiceNow table via the Table API.

This example inserts records into the 'incident' table.
The same pattern works for any ServiceNow table — just change the table name
in the URL and adjust the payload fields to match the target table's schema.

Authentication uses HTTP Basic Auth (username + password).
Credentials and instance URL are loaded from environment variables.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SN_INSTANCE = os.getenv("SN_INSTANCE")   # e.g. https://dev12345.service-now.com
SN_USERNAME  = os.getenv("SN_USERNAME")
SN_PASSWORD  = os.getenv("SN_PASSWORD")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def insert_record(table: str, payload: dict) -> dict:
    """
    Insert a single record into a ServiceNow table.

    Args:
        table:   The table name, e.g. "incident" or "rm_story"
        payload: A dict of field names and values to set on the new record

    Returns:
        The created record as returned by the API (includes sys_id, number, etc.)
    """
    url = f"{SN_INSTANCE}/api/now/table/{table}"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
        headers=HEADERS,
        json=payload,
    )
    response.raise_for_status()
    return response.json()["result"]


# --- Example: insert two incidents ---
sample_incidents = [
    {
        "short_description": "Printer on floor 3 not responding",
        "description": "The network printer in room 3.14 has been offline since this morning. "
                       "Multiple employees have reported being unable to print. "
                       "Restarting the printer did not resolve the issue.",
        "category": "hardware",
        "urgency": "3",
        "impact": "2",
    },
    {
        "short_description": "Unable to access shared drive after password reset",
        "description": "Employee reports losing access to the departmental shared drive "
                       "immediately after completing a mandatory password reset. "
                       "Other network resources are accessible.",
        "category": "network",
        "urgency": "2",
        "impact": "3",
    },
]

if __name__ == "__main__":
    for incident_data in sample_incidents:
        record = insert_record("incident", incident_data)
        print(f"Created: {record['number']} — {record['short_description']}")
