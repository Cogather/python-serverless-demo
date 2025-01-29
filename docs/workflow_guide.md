# 工作流程指南

本文档描述了项目的开发、测试和部署工作流程。

## 开发工作流

### 1. 分支管理

- `main`: 主分支，保持稳定可部署状态
- `develop`: 开发分支，用于集成功能
- `feature/*`: 功能分支，用于开发新功能
- `bugfix/*`: 修复分支，用于修复问题
- `release/*`: 发布分支，用于版本发布

### 2. 代码提交规范

提交信息格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- feat: 新功能
- fix: 修复
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建过程或辅助工具的变动

### 3. 开发流程

1. 创建功能分支
```bash
git checkout -b feature/your-feature develop
```

2. 本地开发
```bash
# 启动开发服务器
uvicorn src.calculator.api:app --reload

# 运行测试
pytest

# 代码格式化
black .
flake8
```

3. 提交代码
```bash
git add .
git commit -m "feat(calculator): add new operation"
git push origin feature/your-feature
```

4. 创建Pull Request
- 标题符合提交规范
- 填写完整的描述
- 请求代码审查
- 确保CI检查通过

## 测试流程

### 1. 单元测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_calculator.py

# 生成覆盖率报告
pytest --cov=src
```

### 2. 性能测试

```bash
# 运行基准测试
pytest tests/benchmark --benchmark-only
```

### 3. 集成测试

```bash
# 运行API测试
pytest tests/integration
```

## 部署流程

### 1. 环境配置

- 开发环境（dev）
- 测试环境（staging）
- 生产环境（prod）

### 2. 部署步骤

1. 准备部署
```bash
# 更新依赖
poetry install

# 运行测试
pytest

# 构建Docker镜像
docker build -t python-serverless-demo .
```

2. 部署到AWS
```bash
# 部署到开发环境
./deploy.sh dev

# 部署到测试环境
./deploy.sh staging

# 部署到生产环境
./deploy.sh prod
```

### 3. 部署验证

1. 检查AWS控制台
   - Lambda函数状态
   - API Gateway配置
   - CloudWatch日志

2. 运行健康检查
```bash
curl https://api-endpoint/health
```

## CI/CD流程

### 1. GitHub Actions

- 代码提交触发：
  - 代码质量检查
  - 单元测试
  - 构建检查

- 合并到develop触发：
  - 部署到开发环境
  - 集成测试

- 发布新版本触发：
  - 部署到生产环境
  - 性能测试

### 2. 监控和告警

- CloudWatch指标监控
- 错误率告警
- 性能监控
- 成本监控

## 发布流程

### 1. 版本管理

使用语义化版本：
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 2. 发布步骤

1. 创建发布分支
```bash
git checkout -b release/v1.0.0 develop
```

2. 更新版本号
```bash
poetry version 1.0.0
```

3. 更新CHANGELOG.md

4. 提交更改
```bash
git commit -m "chore(release): v1.0.0"
```

5. 合并到main和develop
```bash
git checkout main
git merge release/v1.0.0
git tag v1.0.0
git push origin main --tags

git checkout develop
git merge release/v1.0.0
git push origin develop
```

## 问题处理流程

### 1. 问题报告

在GitHub Issues中创建问题，包含：
- 问题描述
- 复现步骤
- 期望结果
- 实际结果
- 环境信息

### 2. 问题修复

1. 创建修复分支
```bash
git checkout -b bugfix/issue-number
```

2. 修复并测试

3. 提交修复
```bash
git commit -m "fix(component): issue description (#issue-number)"
```

4. 创建Pull Request

### 3. 紧急修复

1. 从main创建hotfix分支
```bash
git checkout -b hotfix/critical-fix main
```

2. 修复问题

3. 合并到main和develop
```bash
git checkout main
git merge hotfix/critical-fix
git tag v1.0.1

git checkout develop
git merge hotfix/critical-fix
``` 