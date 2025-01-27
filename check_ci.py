import requests
from datetime import datetime

token = "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"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

def get_latest_run():
    url = "https://api.github.com/repos/yuyu0317/python-serverless-demo/actions/runs"
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "workflow_runs" in data and len(data["workflow_runs"]) > 0:
        latest_run = data["workflow_runs"][0]
        created_at = datetime.strptime(latest_run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        
        print("\n最新运行状态：")
        print(f"运行编号: {latest_run['run_number']}")
        print(f"分支: {latest_run['head_branch']}")
        print(f"提交: {latest_run['head_commit']['message']}")
        print(f"状态: {latest_run['status']}")
        print(f"结果: {latest_run['conclusion']}")
        print(f"开始时间: {created_at}")
        print(f"详细链接: {latest_run['html_url']}")
        
        if latest_run["status"] == "completed":
            if latest_run["conclusion"] == "success":
                print("\n✅ CI 运行成功！")
            else:
                print("\n❌ CI 运行失败！")
                # 获取失败作业的详细信息
                jobs_url = latest_run["jobs_url"]
                jobs_response = requests.get(jobs_url, headers=headers)
                jobs_data = jobs_response.json()
                
                if "jobs" in jobs_data:
                    for job in jobs_data["jobs"]:
                        if job["conclusion"] == "failure":
                            print("\n失败的步骤：")
                            for step in job["steps"]:
                                if step["conclusion"] == "failure":
                                    print(f"- {step['name']}")
        else:
            print("\n⏳ CI 正在运行中...")
        
        return latest_run
    return None

if __name__ == "__main__":
    get_latest_run() 