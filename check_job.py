import requests
import json

token = "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"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

run_id = "12993153863"
url = (
    f"https://api.github.com/repos/yuyu0317/python-serverless-demo/actions/runs/{run_id}/jobs"
)
response = requests.get(url, headers=headers)
data = response.json()

print(json.dumps(data, indent=2)) 