# Python Serverless 项目工作流程指南

本文档旨在指导开发者（包括 AI 助手）如何在本项目中进行代码开发、检查、提交、检视等工作。

## 1. 代码开发流程

### 1.1 分支管理
- 从 `main` 分支创建新的功能分支
- 分支命名规范：
  - 功能分支：`feature/功能名称`
  - 修复分支：`fix/问题描述`
  - 优化分支：`optimize/优化内容`

### 1.2 代码规范
- 使用 Black 进行代码格式化
- 遵循 PEP 8 编码规范
- 代码行长度限制：88 字符
- 必须添加类型注解
- 必须添加文档字符串（docstring）

## 2. 代码检查流程

### 2.1 本地代码检查
使用以下命令进行代码检查：

```bash
# 格式化检查
poetry run black src --check

# 代码风格检查
poetry run flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
poetry run flake8 src --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# 运行测试
poetry run pytest -v
```

### 2.2 自动修复格式问题
如果发现格式问题，使用以下命令自动修复：

```bash
poetry run black src
```

## 3. 代码提交流程

### 3.1 提交前检查
1. 确保所有测试通过
2. 确保代码格式正确
3. 确保文档已更新

### 3.2 提交代码
使用规范的提交信息格式：

```bash
# 格式：<type>: <description>
# type 可以是：feat, fix, docs, style, refactor, test, chore

# 示例：
git add .
git commit -m "feat: 添加新功能 - 详细描述"
git push origin feature/分支名
```

## 4. 创建和管理 Pull Request

### 4.1 创建 PR
使用 `scripts/create_pr.py` 脚本创建 PR：

```bash
python scripts/create_pr.py
```

脚本会自动：
- 获取当前分支信息
- 创建格式化的 PR 描述
- 提交 PR 到 GitHub

### 4.2 检查 CI 状态
使用 `scripts/check_ci.py` 脚本检查 CI 状态：

```bash
python scripts/check_ci.py
```

### 4.3 查看现有检视意见
使用 `scripts/get_reviews.py` 脚本查看检视意见：

```bash
python scripts/get_reviews.py
```

## 5. 代码检视流程

### 5.1 进行代码检视
使用 `scripts/review_pr.py` 脚本进行代码检视：

```bash
python scripts/review_pr.py
```

脚本会：
- 自动检查 src 目录下的代码变更
- 根据预设规则提供检视意见
- 将检视意见提交到 GitHub

### 5.2 检视重点关注
1. 代码质量
   - 代码可读性
   - 错误处理
   - 性能问题
   - 安全问题

2. API 设计
   - 接口定义
   - 参数验证
   - 错误响应
   - 安全控制

3. 测试覆盖
   - 单元测试
   - 集成测试
   - 边界测试
   - 性能测试

## 6. 自动化脚本说明

### 6.1 可用脚本
- `scripts/check_ci.py`: 检查 CI 运行状态
- `scripts/check_job.py`: 检查特定任务状态
- `scripts/create_pr.py`: 创建 Pull Request
- `scripts/get_reviews.py`: 获取检视意见
- `scripts/review_pr.py`: 提交代码检视意见

### 6.2 配置要求
所有脚本都需要 `config.local.json` 配置文件，包含：
```json
{
    "github": {
        "token": "你的GitHub令牌",
        "repository": "用户名/仓库名",
        "base_url": "https://github.com"
    }
}
```

## 7. 注意事项

### 7.1 安全性
- 不要在代码中硬编码敏感信息
- 使用环境变量或配置文件管理密钥
- 注意 API 的访问控制和限制

### 7.2 性能
- 注意代码的时间和空间复杂度
- 避免不必要的 API 调用
- 合理使用缓存机制

### 7.3 文档维护
- 及时更新 API 文档
- 保持 README 文件的最新状态
- 记录重要的设计决策和变更 