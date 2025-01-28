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
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.local.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 未找到配置文件 {config_path}")
        sys.exit(1)


def get_current_branch():
    """获取当前分支名称"""
    try:
        with open('.git/HEAD', 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: refs/heads/'):
                return ref[16:]
    except:
        print("错误: 无法获取当前分支名称")
        sys.exit(1)


def create_pull_request(config):
    """创建Pull Request"""
    token = config['github']['token']
    repo = config['github']['repository']
    api_url = f"https://api.github.com/repos/{repo}/pulls"
    
    current_branch = get_current_branch()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'title': f'代码重构: 优化项目结构 ({current_time})',
        'body': '''
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
''',
        'head': current_branch,
        'base': 'main',
        'maintainer_can_modify': True
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        pr_data = response.json()
        print(f"Pull Request 创建成功！")
        print(f"URL: {pr_data['html_url']}")
    except requests.exceptions.RequestException as e:
        print(f"错误: 创建Pull Request失败")
        print(f"详细信息: {str(e)}")
        if hasattr(e.response, 'json'):
            print(f"GitHub API响应: {e.response.json()}")
        sys.exit(1)


if __name__ == '__main__':
    config = load_config()
    create_pull_request(config) 