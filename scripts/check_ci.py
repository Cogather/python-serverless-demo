#!/usr/bin/env python3
"""
检查GitHub CI状态的脚本。
"""

import json
import os
import sys
import logging
from datetime import datetime, timezone
from typing import Dict, Any

import requests
from requests.exceptions import (
    RequestException,
    HTTPError,
    ConnectionError,
    Timeout,
)

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
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
    logger.debug("尝试加载配置文件: %s", config_path)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.debug("成功加载配置: %s", config)
            return config
    except FileNotFoundError:
        logger.error("配置文件未找到: %s", config_path)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error("配置文件格式错误: %s", str(e))
        sys.exit(1)


def get_latest_workflow_run(config: Dict[str, Any]) -> int:
    """获取最新的工作流运行"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    # 添加branch参数来过滤main分支的运行记录
    api_url = f"https://api.github.com/repos/{repo}/actions/runs?branch=main"
    
    logger.debug("请求GitHub API: %s", api_url)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        logger.debug("API响应状态码: %d", response.status_code)
        response.raise_for_status()
        runs = response.json()
        
        logger.debug("获取到工作流运行数据: %s", runs)

        if not runs["workflow_runs"]:
            logger.error("没有找到main分支的工作流运行记录")
            sys.exit(1)

        latest_run = runs["workflow_runs"][0]
        logger.info("最新工作流运行ID: %d", latest_run["id"])
        logger.info(f"分支: {latest_run['head_branch']}")
        logger.info(f"提交: {latest_run['head_sha'][:7]}")
        return latest_run["id"]

    except Timeout:
        logger.error("请求超时，请检查网络连接")
        sys.exit(1)
    except ConnectionError:
        logger.error("网络连接错误，请检查网络状态")
        sys.exit(1)
    except HTTPError as e:
        logger.error("HTTP请求失败 (状态码: %d)", e.response.status_code)
        logger.debug("响应内容: %s", e.response.text)
        sys.exit(1)
    except RequestException as e:
        logger.error("请求异常: %s", str(e))
        sys.exit(1)
    except Exception as e:
        logger.error("未预期的错误: %s", str(e))
        sys.exit(1)


def get_workflow_jobs(config: Dict[str, Any], run_id: int) -> Dict[str, Any]:
    """获取工作流作业的详细信息"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = (
        f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    except Timeout:
        logger.error("请求超时，请检查网络连接")
        sys.exit(1)
    except ConnectionError:
        logger.error("网络连接错误，请检查网络状态")
        sys.exit(1)
    except HTTPError as e:
        logger.error("HTTP请求失败 (状态码: %d)", e.response.status_code)
        logger.debug("响应内容: %s", e.response.text)
        sys.exit(1)
    except RequestException as e:
        logger.error("请求异常: %s", str(e))
        sys.exit(1)
    except Exception as e:
        logger.error("未预期的错误: %s", str(e))
        sys.exit(1)


def format_time(time_str: str) -> str:
    """格式化时间字符串"""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone()
        return local_dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.warning("时间格式化失败: %s", str(e))
        return time_str


def print_job_info(jobs_data: Dict[str, Any]) -> None:
    """打印作业信息"""
    logger.info("最新的 CI 运行状态:")
    print("=" * 80)

    for job in jobs_data["jobs"]:
        print(f"作业名称: {job['name']}")
        print(f"状态: {job['status']}")
        print(f"结果: {job['conclusion']}")
        print(f"开始时间: {format_time(job['started_at'])}")
        print(f"完成时间: {format_time(job['completed_at'])}")
        print(f"详情链接: {job['html_url']}")
        print("\n步骤详情:")

        for step in job["steps"]:
            status_icon = (
                "✅"
                if step["conclusion"] == "success"
                else "❌"
                if step["conclusion"] == "failure"
                else "⏭️"
                if step["conclusion"] == "skipped"
                else "⚪"
            )
            print(f"{status_icon} {step['name']}: {step['conclusion']}")

        print("=" * 80)


if __name__ == "__main__":
    print("开始检查CI状态...")
    try:
        print("正在加载配置...")
        config = load_config()
        print("配置加载成功:", config)
        
        print("正在获取最新工作流运行...")
        run_id = get_latest_workflow_run(config)
        print(f"获取到运行ID: {run_id}")
        
        print("正在获取作业详情...")
        jobs_data = get_workflow_jobs(config, run_id)
        print("正在打印作业信息...")
        print_job_info(jobs_data)
    except KeyboardInterrupt:
        print("操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print("错误详情:", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
