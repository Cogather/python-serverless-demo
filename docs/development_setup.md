# 开发环境配置指南

本文档介绍了在本地设置开发环境所需的所有依赖和配置步骤。

## 系统要求

- Windows 10 64位（专业版、企业版或教育版，Build 19044或更高版本）
- 最小 8GB RAM 推荐
- 至少 20GB 可用磁盘空间

## 必需软件

### 1. Python 环境

- Python 版本: 3.8.1 或更高版本（小于 4.0.0）
- 推荐使用 [pyenv](https://github.com/pyenv-win/pyenv-win) 管理 Python 版本

安装步骤：
```powershell
# 使用 pyenv 安装 Python
pyenv install 3.8.1
pyenv global 3.8.1
```

### 2. Poetry 包管理工具

Poetry 用于管理项目依赖，版本 1.4.0 或更高版本。

安装步骤：
```powershell
# Windows PowerShell 安装命令
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# 验证安装
poetry --version
```

### 3. Docker 环境

需要安装 Docker Desktop for Windows。

前置条件：
- 启用 Windows 的 Hyper-V 功能
- 启用 WSL 2（Windows Subsystem for Linux 2）

安装步骤：
1. 启用 WSL 2：
   ```powershell
   wsl --install
   ```

2. 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - 运行安装程序
   - 选择 "Use WSL 2 instead of Hyper-V" 选项
   - 完成安装后重启电脑

3. 验证 Docker 安装：
   ```powershell
   docker --version
   docker-compose --version
   ```

## 项目依赖

项目使用 Poetry 管理依赖，主要依赖包括：

### 核心依赖
- aws-lambda-powertools: ^2.0
- boto3: ^1.34
- fastapi: ^0.109.0
- mangum: ^0.17.0
- uvicorn: ^0.27.0
- pydantic: ^2.5.3

### 开发依赖
- pytest: ^7.4
- black: ^23.12
- flake8: ^6.1
- pytest-benchmark: ^4.0.0
- httpx: ^0.26.0
- pytest-asyncio: ^0.23.3

## 项目设置

1. 克隆项目：
   ```bash
   git clone [项目地址]
   cd python-serverless-demo
   ```

2. 安装依赖：
   ```bash
   poetry install
   ```

3. 激活虚拟环境：
   ```bash
   poetry shell
   ```

## 开发工具推荐

- VSCode 或 PyCharm Professional
- Git 版本控制
- Windows Terminal（提供更好的命令行体验）

## 验证开发环境

运行以下命令验证环境配置：

```bash
# 运行测试
poetry run pytest

# 代码格式化检查
poetry run black . --check
poetry run flake8

# 验证 Docker
docker ps
```

## 常见问题

1. 如果安装 Docker 时遇到 WSL 2 相关错误：
   - 确保在 BIOS 中启用了虚拟化功能
   - 确保 Windows 功能中启用了 "Hyper-V" 和 "Windows Subsystem for Linux"

2. 如果 Poetry 安装依赖失败：
   - 确保使用的是兼容的 Python 版本
   - 尝试清除 Poetry 缓存：`poetry cache clear . --all`

## 更新日志

- 2024-01-28: 初始版本创建 