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

## CI 配置要点

### 工具链配置

1. **Black 代码格式化**
   - 使用默认配置（行长度 88 字符）
   - 在提交前运行格式化检查

2. **Flake8 代码质量检查**
   - 分两步检查：
     1. 严重错误检查：`--select=E9,F63,F7,F82`（语法错误、未定义变量等）
     2. 风格和复杂度检查：`--max-complexity=10 --max-line-length=88`
   - 关键配置：
     - `--ignore=E402`：忽略模块级导入顺序
     - `--exclude=.venv,venv,env`：排除虚拟环境目录
     - `--max-line-length=88`：与 Black 保持一致

3. **Poetry 依赖管理**
   - 使用 `poetry.lock` 确保依赖版本一致
   - 配置虚拟环境在项目目录下：`virtualenvs.in-project true`

### 问题定位思路

1. **环境一致性问题**
   - 本地和 CI 环境的差异（如 flake8 检查范围不同）
   - 使用 `--exclude` 排除不需要检查的目录

2. **工具冲突处理**
   - Black 和 Flake8 的行长度配置保持一致
   - 使用 `ignore` 参数处理特定场景的规则冲突

3. **CI 失败排查**
   - 检查 CI 日志获取详细错误信息
   - 在本地复现 CI 环境的检查命令
   - 使用辅助脚本（如 `.ci/check_job.py`）监控 CI 状态

4. **最佳实践**
   - 将 CI 检查脚本与项目代码分离（放在 `.ci` 目录）
   - 敏感信息（如 token）使用环境变量管理
   - 保持 CI 配置文件的清晰和可维护性 