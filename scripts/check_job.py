import requests
import json
import os

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable is not set")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}

run_id = "12993153863"
base_url = "https://api.github.com/repos/yuyu0317/python-serverless-demo"
url = f"{base_url}/actions/runs/{run_id}/jobs"
response = requests.get(url, headers=headers)
data = response.json()

print(json.dumps(data, indent=2))
