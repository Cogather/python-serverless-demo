#!/usr/bin/env python3
"""
创建 GitHub Pull Request 的辅助脚本。
"""

import json
import os
import sys
from datetime import datetime

import requests


def load_config():
    """加载本地配置文件"""
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


def get_current_branch():
    """获取当前分支名称"""
    try:
        with open(".git/HEAD", "r") as f:
            ref = f.read().strip()
            if ref.startswith("ref: refs/heads/"):
                return ref[16:]
            raise ValueError("无效的HEAD引用格式")
    except (IOError, OSError) as e:
        print("错误: 无法读取.git/HEAD文件: %s", str(e))
        sys.exit(1)
    except ValueError as e:
        print("错误: %s", str(e))
        sys.exit(1)


def create_pull_request(config):
    """创建Pull Request"""
    token = config["github"]["token"]
    repo = config["github"]["repository"]
    api_url = f"https://api.github.com/repos/{repo}/pulls"

    current_branch = get_current_branch()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {
        "title": "代码重构: 优化项目结构 (%s)" % current_time,
        "body": """
## 更新内容

1. 重构项目目录结构，采用标准的Python项目布局
   - 源代码移至 `src/calculator/` 目录
   - 测试文件移至 `tests/calculator/` 目录
   - CI脚本移至 `scripts/` 目录

2. 优化代码组织
   - 将核心功能移至独立模块
   - 更新导入路径
   - 优化测试文件组织

3. 改进配置文件
   - 优化 `.gitignore` 配置
   - 更新 CI 工作流配置
   - 添加本地配置文件支持

4. 完善文档
   - 更新 README.md
   - 更新项目状态文档
   - 添加详细的API文档

## 测试状态
- [x] 所有测试通过
- [x] 代码风格检查通过
- [x] 文档已更新
""",
        "head": current_branch,
        "base": "main",
        "maintainer_can_modify": True,
    }

    print("当前分支: %s", current_branch)
    print("API URL: %s", api_url)
    print("请求头: %s", json.dumps(headers, indent=2))
    print("请求数据: %s", json.dumps(data, indent=2))

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        pr_data = response.json()
        print("Pull Request 创建成功！")
        print("URL: %s", pr_data["html_url"])
    except requests.exceptions.RequestException as e:
        print("错误: 创建Pull Request失败")
        print("详细信息: %s", str(e))
        if hasattr(e, "response") and e.response is not None:
            print("状态码: %d", e.response.status_code)
            print("响应头: %s", json.dumps(dict(e.response.headers), indent=2))
            try:
                print(
                    "响应内容: %s",
                    json.dumps(e.response.json(), indent=2)
                )
            except json.JSONDecodeError:
                print("响应内容: %s", e.response.text)
        sys.exit(1)


if __name__ == "__main__":
    config = load_config()
    create_pull_request(config)
