#!/usr/bin/env python3
"""
检查GitHub Actions工作流错误的脚本
"""

import json
import os
import sys
import logging
from typing import Dict, Any, List
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config.local.json"
    )
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("配置文件未找到: %s", config_path)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error("配置文件格式错误: %s", str(e))
        sys.exit(1)


def get_workflow_runs(config: Dict[str, Any], per_page: int = 5) -> List[Dict[str, Any]]:
    """获取最近的工作流运行记录"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/actions/runs"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    params = {
        "per_page": per_page,
        "branch": "main"
    }

    try:
        # 禁用代理
        session = requests.Session()
        session.trust_env = False
        response = session.get(api_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()["workflow_runs"]
    except Exception as e:
        logger.error("获取工作流运行记录失败: %s", str(e))
        sys.exit(1)


def get_workflow_logs(config: Dict[str, Any], run_id: int) -> Dict[str, Any]:
    """获取工作流运行的日志"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        # 禁用代理
        session = requests.Session()
        session.trust_env = False
        response = session.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error("获取工作流日志失败: %s", str(e))
        return None


def get_run_details(config: Dict[str, Any], run_id: int) -> Dict[str, Any]:
    """获取工作流运行的详细信息"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        session = requests.Session()
        session.trust_env = False
        response = session.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error("获取运行详情失败: %s", str(e))
        return None


def get_job_logs(config: Dict[str, Any], job_id: int) -> str:
    """获取作业的详细日志"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/actions/jobs/{job_id}/logs"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        session = requests.Session()
        session.trust_env = False
        response = session.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error("获取作业日志失败: %s", str(e))
        return None


def print_workflow_status(run: Dict[str, Any], logs: Dict[str, Any] = None) -> None:
    """打印工作流状态和错误信息"""
    print("\n" + "=" * 80)
    print(f"工作流: {run['name']}")
    print(f"提交: {run['head_commit']['message']}")
    print(f"分支: {run['head_branch']}")
    print(f"状态: {run['status']}")
    print(f"结论: {run['conclusion'] or '进行中'}")
    print(f"触发事件: {run['event']}")
    print(f"创建时间: {run['created_at']}")
    print(f"详情链接: {run['html_url']}")
    
    if logs and "jobs" in logs:
        print("\n作业详情:")
        for job in logs["jobs"]:
            print(f"\n作业名称: {job['name']}")
            print(f"状态: {job['status']}")
            print(f"结论: {job['conclusion'] or '进行中'}")
            
            print("\n步骤:")
            for step in job["steps"]:
                status_icon = "✅" if step["conclusion"] == "success" else "❌" if step["conclusion"] == "failure" else "⏳"
                print(f"{status_icon} {step['name']}: {step['conclusion'] or '进行中'}")
                
                # 如果步骤失败，显示错误信息
                if step.get("conclusion") == "failure":
                    print(f"   错误信息: {step.get('error_message', '未知错误')}")
    
    print("=" * 80 + "\n")


def main():
    """主函数"""
    try:
        config = load_config()
        runs = get_workflow_runs(config)
        
        if not runs:
            logger.error("没有找到任何工作流运行记录")
            return
        
        # 只获取最新的一次运行
        latest_run = runs[0]
        print(f"\n最新的工作流运行:")
        print(f"提交: {latest_run['head_commit']['message']}")
        print(f"状态: {latest_run['status']}")
        print(f"结论: {latest_run['conclusion']}")
        
        # 获取作业信息
        jobs = get_workflow_logs(config, latest_run["id"])
        if jobs and "jobs" in jobs:
            for job in jobs["jobs"]:
                print(f"\n作业: {job['name']}")
                print(f"状态: {job['status']}")
                print(f"结论: {job['conclusion']}")
                
                # 如果作业失败了，获取详细日志
                if job['conclusion'] == 'failure':
                    print("\n详细日志:")
                    logs = get_job_logs(config, job['id'])
                    if logs:
                        print(logs)
                    
    except KeyboardInterrupt:
        logger.info("操作已取消")
        sys.exit(0)
    except Exception as e:
        logger.error("程序执行出错: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 
