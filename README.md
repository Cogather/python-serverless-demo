# Python 无服务器演示项目

这是一个基于 Python 的无服务器演示项目，用于展示基本的数学计算功能，同时演示 GitHub Actions 和 CI/CD 的使用。

## 功能特性

- 基本数学运算（加、减、乘、除）
- 平方根计算
- 完整的单元测试
- CI/CD 流程
- 代码质量控制

## 快速开始

### 环境要求

- Python 3.8+
- Poetry

### 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/python-serverless-demo.git
cd python-serverless-demo
```

2. 安装依赖：

```bash
poetry install
```

### 使用示例

```python
from calculator import add, subtract, multiply, divide, sqrt

# 基本运算
result = add(1, 2)      # 3
result = subtract(5, 3)  # 2
result = multiply(4, 2)  # 8
result = divide(6, 2)    # 3
result = sqrt(16)        # 4
```

## 开发

### 运行测试

```bash
poetry run pytest
```

### 代码格式化

```bash
poetry run black .
```

### 代码检查

```bash
poetry run flake8
```

## 项目结构

```
.
├── src/                    # 源代码目录
│   └── calculator/         # 计算器模块
│       ├── __init__.py    # 模块接口
│       └── core.py        # 核心实现
├── tests/                  # 测试目录
│   └── calculator/        # 计算器模块测试
│       └── test_core.py   # 核心功能测试
├── docs/                   # 文档目录
├── scripts/               # 脚本目录
└── .github/workflows/     # GitHub Actions 配置
```

## 文档

详细的项目文档请参见 [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)。

## CI/CD

项目使用 GitHub Actions 进行持续集成和部署。每次提交都会自动运行以下检查：

- 代码风格检查（Black）
- 代码质量检查（Flake8）
- 单元测试（Pytest）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 