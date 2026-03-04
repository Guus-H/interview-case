import os, requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

r = requests.post(
    "https://dev337536.service-now.com/api/now/table/rm_story",
    auth=HTTPBasicAuth(os.getenv("SN_USERNAME"), os.getenv("SN_PASSWORD")),
    headers={"Content-Type": "application/json", "Accept": "application/json"},
    json={"short_description": "test story"}
)
print(r.status_code)
print(r.text)
