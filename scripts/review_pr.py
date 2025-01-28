#!/usr/bin/env python3
"""
GitHub Pull Request 代码审查脚本。
用于获取 PR 信息并提交代码审查意见。
"""

import json
import os
import sys
import re
from typing import List, Dict, Any

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


def get_pr_files(config: Dict[str, Any], pr_number: int) -> List[Dict[str, Any]]:
    """获取 PR 中的文件变更"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = (
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("错误: 获取文件变更失败 - %s", str(e))
        sys.exit(1)


def parse_patch(patch: str) -> List[Dict[str, Any]]:
    """解析补丁内容，返回变更的行号信息"""
    changes = []
    current_section = None

    for line in patch.split("\n"):
        # 解析变更区块头
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+),?\d* \+(\d+),?\d* @@", line)
            if match:
                old_start = int(match.group(1))
                new_start = int(match.group(2))
                current_section = {
                    "old_start": old_start,
                    "new_start": new_start,
                    "lines": [],
                }
                changes.append(current_section)
        # 记录变更的行
        elif current_section is not None:
            if line.startswith("+"):
                added_lines = len([
                    line_info
                    for line_info in current_section["lines"]
                    if line_info["type"] in ("add", "context")
                ])
                current_section["lines"].append({
                    "type": "add",
                    "content": line[1:],
                    "line_number": current_section["new_start"] + added_lines,
                })
            elif line.startswith("-"):
                removed_lines = len([
                    line_info
                    for line_info in current_section["lines"]
                    if line_info["type"] in ("remove", "context")
                ])
                current_section["lines"].append({
                    "type": "remove",
                    "content": line[1:],
                    "line_number": (
                        current_section["old_start"] + removed_lines
                    ),
                })
            else:
                context_lines = len([
                    line_info
                    for line_info in current_section["lines"]
                    if line_info["type"] in ("add", "context")
                ])
                current_section["lines"].append({
                    "type": "context",
                    "content": line,
                    "line_number": (
                        current_section["new_start"] + context_lines
                    ),
                })

    return changes


def get_existing_reviews(
    config: Dict[str, Any], pr_number: int
) -> List[Dict[str, Any]]:
    """获取PR已有的检视意见"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = (
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        reviews = response.json()

        # 收集所有已有的检视意见
        existing_comments = []
        for review in reviews:
            if review.get("state") != "DISMISSED":  # 忽略已被驳回的检视意见
                comments_url = (
                    f"https://api.github.com/repos/{repo}/pulls/"
                    f"{pr_number}/reviews/{review['id']}/comments"
                )
                comments_response = requests.get(
                    comments_url, headers=headers
                )
                comments_response.raise_for_status()
                existing_comments.extend(comments_response.json())

        return existing_comments
    except requests.exceptions.RequestException as e:
        print("警告: 获取现有检视意见失败 - %s", str(e))
        return []


def is_similar_comment(
    new_comment: Dict[str, Any], existing_comment: Dict[str, Any]
) -> bool:
    """检查两个检视意见是否相似"""
    # 检查文件路径是否相同
    if new_comment["path"] != existing_comment.get("path"):
        return False

    # 检查行号是否相近（允许5行的误差）
    if abs(new_comment["line"] - existing_comment.get("line", 0)) > 5:
        return False

    # 检查内容是否相似（使用简单的文本匹配）
    new_body = new_comment["body"].lower()
    existing_body = existing_comment.get("body", "").lower()

    # 定义一些关键词组来判断评论是否属于同一类型
    comment_types = [
        {"logging", "print", "日志"},
        {"error", "exception", "错误", "异常"},
        {"type", "hint", "类型"},
        {"test", "case", "测试"},
        {"boundary", "value", "边界"},
        {"performance", "benchmark", "性能"},
    ]

    for keywords in comment_types:
        if any(word in new_body for word in keywords) and any(
            word in existing_body for word in keywords
        ):
            return True

    return False


def review_code(
    config: Dict[str, Any],
    pr_data: Dict[str, Any],
    files: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """执行代码审查"""
    comments = []
    existing_comments = get_existing_reviews(config, pr_data["number"])

    for file in files:
        filename = file["filename"]

        # 检查 check_job.py
        if filename == "scripts/check_job.py":
            changes = parse_patch(file["patch"])
            for section in changes:
                for line in section["lines"]:
                    # 检查错误处理
                    if (
                        "except" in line["content"]
                        and "Exception" in line["content"]
                    ):
                        new_comment = {
                            "path": filename,
                            "line": line["line_number"],
                            "body": (
                                "建议将异常处理分得更细致，分别处理 "
                                "`requests.exceptions.RequestException` "
                                "和其他可能的异常。"
                            ),
                        }
                        if not any(
                            is_similar_comment(new_comment, existing)
                            for existing in existing_comments
                        ):
                            comments.append(new_comment)

                    # 检查日志格式
                    if "print(" in line["content"] and (
                        "错误" in line["content"] or "Error" in line["content"]
                    ):
                        new_comment = {
                            "path": filename,
                            "line": line["line_number"],
                            "body": "建议使用日志模块（logging）来替代 print 输出错误信息，这样可以更好地控制日志级别和格式。",
                        }
                        if not any(
                            is_similar_comment(new_comment, existing)
                            for existing in existing_comments
                        ):
                            comments.append(new_comment)

        # 检查 calculator/core.py
        elif filename == "src/calculator/core.py":
            changes = parse_patch(file["patch"])
            for section in changes:
                for line in section["lines"]:
                    # 检查错误消息
                    if "raise ValueError" in line["content"]:
                        new_comment = {
                            "path": filename,
                            "line": line["line_number"],
                            "body": "建议在错误消息中添加更多上下文信息，例如当前的输入值。",
                        }
                        if not any(
                            is_similar_comment(new_comment, existing)
                            for existing in existing_comments
                        ):
                            comments.append(new_comment)

                    # 检查类型提示
                    if "def" in line["content"] and "->" in line["content"]:
                        if "float" not in line["content"]:
                            new_comment = {
                                "path": filename,
                                "line": line["line_number"],
                                "body": "建议为所有数值参数添加类型提示，使用 float 或 Union[int, float]。",
                            }
                            if not any(
                                is_similar_comment(new_comment, existing)
                                for existing in existing_comments
                            ):
                                comments.append(new_comment)

        # 检查测试文件
        elif filename == "tests/calculator/test_core.py":
            new_comment = {
                "path": filename,
                "line": 1,
                "body": """建议添加以下测试用例：
1. 边界值测试（例如：最大浮点数、最小浮点数）
2. 性能测试（使用 @pytest.mark.benchmark）
3. 参数类型测试（确保函数能正确处理不同类型的数值输入）""",
            }
            if not any(
                is_similar_comment(new_comment, existing)
                for existing in existing_comments
            ):
                comments.append(new_comment)

    return comments


def submit_review(
    config: Dict[str, Any],
    pr_number: int,
    pr_data: Dict[str, Any],
    comments: List[Dict[str, Any]],
) -> int:
    """提交代码审查意见"""
    if not comments:
        print("没有发现需要审查的问题。")
        return

    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {
        "commit_id": pr_data["head"]["sha"],
        "body": "## 代码审查意见\n\n以下是一些改进建议：",
        "event": "COMMENT",
        "comments": comments,
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        review_id = response.json()["id"]
        print("代码审查意见已提交成功！")
        return review_id
    except Exception as e:
        print(f"错误: 提交代码审查意见失败 - {str(e)}")
        sys.exit(1)


def mark_files_as_viewed(
    config: Dict[str, Any], pr_number: int, review_id: int
) -> None:
    """标记PR中的所有文件为已审查"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews/{review_id}/files"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.put(api_url, headers=headers)
        response.raise_for_status()
        print("成功标记所有文件为已审查！")
    except requests.exceptions.RequestException as e:
        print(f"警告: 标记文件为已审查失败 - {str(e)}")
        if hasattr(e, "response") and e.response is not None:
            print(f"响应内容: {e.response.text}")


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
    print(f"标题: {pr_data['title']}")
    print(f"编号: #{pr_number}")
    print(f"状态: {pr_data['state']}")
    print(f"创建者: {pr_data['user']['login']}")
    print(f"创建时间: {pr_data['created_at']}")
    print(f"更新时间: {pr_data['updated_at']}")
    print(f"URL: {pr_data['html_url']}\n")

    print("文件变更:")
    print("=" * 80)

    files = get_pr_files(config, pr_number)
    for file in files:
        print(f"\n文件: {file['filename']}")
        print(f"状态: {file['status']}")
        print(f"增加: +{file['additions']} 行")
        print(f"删除: -{file['deletions']} 行")
        print(f"变更: {file['changes']} 行\n")

        if file.get("patch"):
            print("代码变更:")
            print("-" * 40)
            print(file["patch"])

    comments = review_code(config, pr_data, files)
    if comments:
        review_id = submit_review(config, pr_number, pr_data, comments)
        mark_files_as_viewed(config, pr_number, review_id)
    else:
        print("没有新的检视意见需要提交。")


if __name__ == "__main__":
    main()
