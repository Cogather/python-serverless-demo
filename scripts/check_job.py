#!/usr/bin/env python3
"""
检查 GitHub Actions CI 作业的状态。
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

import requests


def load_config():
    """加载本地配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.local.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 未找到配置文件 {config_path}")
        sys.exit(1)


def get_latest_workflow_run(config):
    """获取最新的工作流运行"""
    token = config['github']['token']
    repo = config['github']['repository']
    api_url = f"https://api.github.com/repos/{repo}/actions/runs"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        runs = response.json()
        
        if not runs['workflow_runs']:
            print("没有找到任何工作流运行记录")
            sys.exit(1)
            
        latest_run = runs['workflow_runs'][0]
        return latest_run['id']
        
    except requests.exceptions.RequestException as e:
        print(f"错误: 获取工作流运行失败")
        print(f"详细信息: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"状态码: {e.response.status_code}")
            try:
                print(f"响应内容: {json.dumps(e.response.json(), indent=2, ensure_ascii=False)}")
            except:
                print(f"响应内容: {e.response.text}")
        sys.exit(1)


def get_workflow_jobs(config, run_id):
    """获取工作流作业的详细信息"""
    token = config['github']['token']
    repo = config['github']['repository']
    api_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"错误: 获取作业详情失败")
        print(f"详细信息: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"状态码: {e.response.status_code}")
            try:
                print(f"响应内容: {json.dumps(e.response.json(), indent=2, ensure_ascii=False)}")
            except:
                print(f"响应内容: {e.response.text}")
        sys.exit(1)


def format_time(time_str):
    """格式化时间字符串"""
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    dt = dt.replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone()
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")


def print_job_info(jobs_data):
    """打印作业信息"""
    print("\n最新的 CI 运行状态:")
    print("=" * 80)
    
    for job in jobs_data['jobs']:
        print(f"作业名称: {job['name']}")
        print(f"状态: {job['status']}")
        print(f"结果: {job['conclusion']}")
        print(f"开始时间: {format_time(job['started_at'])}")
        print(f"完成时间: {format_time(job['completed_at'])}")
        print(f"详情链接: {job['html_url']}")
        print("\n步骤详情:")
        
        for step in job['steps']:
            status_icon = "✅" if step['conclusion'] == 'success' else "❌" if step['conclusion'] == 'failure' else "⏭️" if step['conclusion'] == 'skipped' else "⚪"
            print(f"{status_icon} {step['name']}: {step['conclusion']}")
        
        print("=" * 80)


if __name__ == '__main__':
    config = load_config()
    run_id = get_latest_workflow_run(config)
    jobs_data = get_workflow_jobs(config, run_id)
    print_job_info(jobs_data)
