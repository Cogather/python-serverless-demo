#!/usr/bin/env python3
"""
关闭GitHub Pull Request的脚本。
"""

import json
import os
import sys
from typing import Dict, Any

import requests


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config.local.json"
    )
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 未找到配置文件 {config_path}")
        sys.exit(1)


def get_pr_info(config: Dict[str, Any]) -> Dict[str, Any]:
    """获取当前分支的 PR 信息"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/pulls"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        prs = response.json()

        # 获取当前分支名
        with open(".git/HEAD", "r") as f:
            current_branch = f.read().strip()
            if current_branch.startswith("ref: refs/heads/"):
                current_branch = current_branch[16:]

        # 查找当前分支的 PR
        for pr in prs:
            if pr["head"]["ref"] == current_branch:
                return pr

        print(f"错误: 未找到分支 {current_branch} 的 PR")
        sys.exit(1)

    except Exception as e:
        print(f"错误: 获取 PR 信息失败 - {str(e)}")
        sys.exit(1)


def close_pr(config: Dict[str, Any], pr_number: int) -> None:
    """关闭指定的PR"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {"state": "closed"}

    try:
        response = requests.patch(api_url, headers=headers, json=data)
        response.raise_for_status()
        print(f"成功关闭 PR #{pr_number}！")
    except Exception as e:
        print(f"错误: 关闭 PR 失败 - {str(e)}")
        if hasattr(e, "response") and e.response is not None:
            print(f"响应内容: {e.response.text}")
        sys.exit(1)


def main():
    """主函数"""
    config = load_config()
    pr_data = get_pr_info(config)

    if not pr_data:
        print("未找到活动的Pull Request")
        return

    pr_number = pr_data["number"]
    print(f"\n准备关闭 PR #{pr_number}")
    print(f"标题: {pr_data['title']}")
    print(f"URL: {pr_data['html_url']}")

    # 关闭PR
    close_pr(config, pr_number)


if __name__ == "__main__":
    main()
