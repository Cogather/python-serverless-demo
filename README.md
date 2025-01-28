# Python Serverless Demo

这是一个基于 FastAPI 的计算器 Demo 项目，提供基本的数学运算 API 服务。项目采用无服务器架构，可部署在 AWS Lambda 上运行。

## 项目状态

当前版本：v0.3.0 (2024-01-28)

主要更新：
- 代码质量改进：优化错误处理、统一日志格式、增强类型提示
- CI/CD改进：完善CI检查、优化PR流程
- 测试改进：增加边界测试、性能基准测试

详细的版本历史和计划请查看 [项目状态文档](docs/PROJECT_STATUS.md)。

## 功能特性

- RESTful API 接口
  - 基本数学运算（加、减、乘、除）
  - 平方根计算
  - 健康检查接口
- Swagger/OpenAPI 文档
- AWS Lambda 集成
- 完整的测试覆盖
- CI/CD 自动化流程

## 快速开始

### 环境要求

详细的环境配置请参考 [开发环境配置指南](docs/development_setup.md)

- Windows 10 64位（专业版、企业版或教育版）
- Python 3.8.1+
- Poetry 1.4.0+
- Docker Desktop for Windows

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/python-serverless-demo.git
cd python-serverless-demo
```

2. 安装依赖：
```bash
poetry install
```

3. 启动开发服务器：
```bash
poetry run uvicorn calculator.api:app --reload
```

### API 使用示例

访问 API 文档：http://localhost:8000/docs

示例请求：
```bash
# 加法运算
curl -X POST "http://localhost:8000/add" -H "Content-Type: application/json" -d '{"a": 10.5, "b": 5.2}'

# 平方根计算
curl -X POST "http://localhost:8000/sqrt" -H "Content-Type: application/json" -d '{"value": 16.0}'
```

## 项目结构

```
python-serverless-demo/
├── src/
│   └── calculator/
│       ├── __init__.py     # 核心计算器功能
│       ├── api.py          # FastAPI应用和路由
│       └── lambda_handler.py # AWS Lambda处理函数
├── tests/                  # 测试代码
├── docs/                   # 项目文档
│   ├── design.md          # 设计文档
│   ├── development_setup.md # 环境配置指南
│   ├── workflow_guide.md   # 工作流程指南
│   └── PROJECT_STATUS.md   # 项目状态记录
└── scripts/               # 自动化脚本
```

## 开发工作流

详细的开发流程请参考 [工作流程指南](docs/workflow_guide.md)

### 代码检查
```bash
# 格式化检查
poetry run black . --check

# 代码风格检查
poetry run flake8

# 运行测试
poetry run pytest -v
```

### 分支管理
- 功能分支：`feature/功能名称`
- 修复分支：`fix/问题描述`
- 优化分支：`optimize/优化内容`

## CI/CD

项目使用 GitHub Actions 进行自动化流程：
- 代码风格检查（Black）
- 代码质量检查（Flake8）
- 单元测试（Pytest）
- 自动化部署（AWS Lambda）

## 文档

- [项目设计文档](docs/design.md)：API 设计和技术架构
- [开发环境配置](docs/development_setup.md)：环境搭建指南
- [工作流程指南](docs/workflow_guide.md)：开发流程和规范
- [项目状态](docs/PROJECT_STATUS.md)：版本历史和计划

## 贡献指南

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

详细的开发规范和流程请参考 [工作流程指南](docs/workflow_guide.md)。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 