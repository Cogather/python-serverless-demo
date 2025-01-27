# Python Serverless Demo

这是一个演示GitHub Actions和CI/CD功能的Python项目。

## 功能特点

- 使用GitHub Actions进行自动化测试
- 代码质量检查 (flake8)
- 代码格式化 (black)
- 自动化测试 (pytest)

## 项目设置

1. 克隆项目
```bash
git clone https://github.com/YOUR_USERNAME/python-serverless-demo.git
cd python-serverless-demo
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 开发指南

- 运行测试：`pytest`
- 代码格式化：`black .`
- 代码检查：`flake8`

## CI/CD 流程

本项目使用GitHub Actions进行CI/CD，包括：
- 代码质量检查
- 自动化测试
- 代码格式验证 