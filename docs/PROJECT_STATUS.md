# 项目状态文档

## 项目概述

这是一个基于 Python 的无服务器演示项目，用于展示 GitHub Actions 和 CI/CD 功能。

### 当前分支
- 主分支：`main`
- 开发分支：`feature/add-sqrt-function`（添加平方根计算功能）

### 项目结构
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
│   └── PROJECT_STATUS.md  # 项目状态文档
├── scripts/               # 脚本目录
│   ├── check_ci.py       # 检查 CI 运行状态
│   └── check_job.py      # 获取 CI 作业详细信息
├── .github/workflows/     # GitHub Actions 配置
│   └── python-ci.yml     # CI 工作流配置
├── pyproject.toml        # Poetry 项目配置
└── poetry.lock          # 依赖版本锁定
```

## API 文档

### 计算器模块 (calculator.core)
- `add(a: float, b: float) -> float`: 加法运算
- `subtract(a: float, b: float) -> float`: 减法运算
- `multiply(a: float, b: float) -> float`: 乘法运算
- `divide(a: float, b: float) -> float`: 除法运算
- `sqrt(x: float) -> float`: 平方根计算

### CI 检查脚本
1. **check_ci.py**
   - 功能：监控 GitHub Actions CI 运行状态
   - 环境变量：`GITHUB_TOKEN`（必需）
   - 用法：`poetry run python scripts/check_ci.py`

2. **check_job.py**
   - 功能：获取 CI 作业的详细日志
   - 环境变量：`GITHUB_TOKEN`（必需）
   - 用法：`poetry run python scripts/check_job.py`

## GitHub API 使用
- Actions Runs API: `GET /repos/{owner}/{repo}/actions/runs`
- Jobs API: `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`
- 认证：使用 Bearer Token（Personal Access Token）

## 开发环境
- Python 3.10
- Poetry 依赖管理
- 代码质量工具：
  - Black（格式化）
  - Flake8（代码检查）
  - Pytest（测试框架）

## CI/CD 状态
- [x] 基础功能实现
- [x] 单元测试覆盖
- [x] CI 工作流配置
- [x] 代码质量检查
- [x] 自动化测试
- [ ] CD 部署流程（待实现）

## 注意事项
1. CI 脚本需要设置 `GITHUB_TOKEN` 环境变量
2. 运行 flake8 时需要排除虚拟环境目录
3. Black 和 Flake8 的行长度配置保持一致（88 字符）

## 最近更新
1. 重构项目目录结构，采用标准的Python项目布局
2. 将核心功能移至独立模块
3. 优化测试文件组织
4. 更新文档以反映新的结构

## 待办事项
- [ ] 实现持续部署流程
- [ ] 添加更多数学函数
- [ ] 完善错误处理
- [ ] 添加 API 文档生成 