# 开发环境设置指南

## 环境要求

- Python >= 3.8.1
- Poetry >= 1.7.0
- Docker (可选，用于本地测试)
- AWS CLI (已配置凭证)

## 快速开始

1. 克隆项目
```bash
git clone https://github.com/yourusername/python-serverless-demo.git
cd python-serverless-demo
```

2. 安装依赖
```bash
poetry install
```

3. 激活虚拟环境
```bash
poetry shell
```

## 主要依赖版本

- FastAPI: 0.109.0
- AWS Lambda Powertools: 2.0
- Boto3: 1.34
- Pydantic: 2.5.3
- Mangum: 0.17.0

## 本地开发

1. 运行本地开发服务器
```bash
uvicorn src.calculator.api:app --reload
```

2. 访问API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

运行单元测试：
```bash
pytest
```

运行性能测试：
```bash
pytest tests/benchmark --benchmark-only
```

## 代码质量

1. 格式化代码
```bash
black .
```

2. 运行代码检查
```bash
flake8
```

## Docker支持

构建Docker镜像：
```bash
docker build -t python-serverless-demo .
```

运行容器：
```bash
docker run -p 8000:8000 python-serverless-demo
```

## 部署

1. 确保AWS凭证已配置
2. 运行部署命令：
```bash
./deploy.sh
```

## 常见问题

1. Poetry安装问题
   - 确保使用最新版本的poetry
   - 如遇到依赖冲突，尝试删除poetry.lock后重新安装

2. 本地测试问题
   - 确保所有环境变量都已正确设置
   - 检查config.local.json配置是否正确

3. 部署问题
   - 确保AWS凭证配置正确
   - 检查IAM权限是否充足

## 更新日志

- 2024-01-28: 初始版本创建 