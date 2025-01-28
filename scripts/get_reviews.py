#!/usr/bin/env python3
"""
获取GitHub Pull Request的检视意见。
"""

import json
import os
import sys
from typing import Dict, Any, List
from datetime import datetime

import requests


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
        print("错误: 未找到配置文件 %s", config_path)
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

        print("错误: 未找到分支 %s 的 PR", current_branch)
        sys.exit(1)

    except (IOError, OSError) as e:
        print("错误: 无法读取.git/HEAD文件 - %s", str(e))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print("错误: 获取 PR 信息失败 - %s", str(e))
        sys.exit(1)


def get_pr_reviews(
    config: Dict[str, Any], pr_number: int
) -> List[Dict[str, Any]]:
    """获取PR的所有检视意见"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = (
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return [
            {"state": "COMMENTED", "detailed_comments": [comment]}
            for comment in response.json()
        ]

    except requests.exceptions.RequestException as e:
        print("错误: 获取检视意见失败 - %s", str(e))
        if hasattr(e, "response") and e.response is not None:
            print("响应内容: %s", e.response.text)
        sys.exit(1)


def format_review_comments(
    reviews: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """将检视意见按文件分组"""
    comments_by_file = {}

    for review in reviews:
        for comment in review.get("detailed_comments", []):
            file_path = comment["path"]
            if file_path not in comments_by_file:
                comments_by_file[file_path] = []

            comments_by_file[file_path].append(
                {
                    "line": comment.get("position", comment.get("line", 1)),
                    "body": comment["body"],
                    "reviewer": comment["user"]["login"],
                    "time": datetime.strptime(
                        comment["created_at"], "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "url": comment["html_url"],
                }
            )

    return comments_by_file


def print_review_comments(comments_by_file: Dict[str, List[Dict[str, Any]]]):
    """打印检视意见"""
    if not comments_by_file:
        print("\n没有找到任何检视意见。")
        return

    print("\n检视意见汇总:")
    print("=" * 80)

    for file_path, comments in comments_by_file.items():
        print("\n文件: %s", file_path)
        print("-" * 40)

        for comment in comments:
            print("行号: %d", comment["line"])
            print("检视者: %s", comment["reviewer"])
            print("时间: %s", comment["time"])
            print("意见: %s", comment["body"])
            print("链接: %s", comment["url"])
            print()


def main():
    """主函数"""
    config = load_config()
    pr_data = get_pr_info(config)

    if not pr_data:
        print("未找到活动的Pull Request")
        return

    pr_number = pr_data["number"]
    print("\nPull Request 信息:")
    print("=" * 80)
    print("标题: %s", pr_data["title"])
    print("编号: #%d", pr_number)
    print("状态: %s", pr_data["state"])
    print("URL: %s", pr_data["html_url"])

    # 获取并显示检视意见
    reviews = get_pr_reviews(config, pr_number)
    comments_by_file = format_review_comments(reviews)
    print_review_comments(comments_by_file)

    # 保存检视意见到文件，供其他脚本使用
    output_file = os.path.join(
        os.path.dirname(__file__),
        "review_comments.json"
    )
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comments_by_file, f, ensure_ascii=False, indent=2)
    print("\n检视意见已保存到: %s", output_file)


if __name__ == "__main__":
    main()
