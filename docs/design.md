# Python Serverless Demo 项目设计文档

## 1. 项目概述

### 1.1 项目简介
这是一个基于 FastAPI 的计算器 Demo 项目，提供基本的数学运算 API 服务。

### 1.2 主要功能
- 基本数学运算 API（加、减、乘、除、平方根）
- API 文档（Swagger/OpenAPI）
- 基本的错误处理

## 2. 项目结构
```
python-serverless-demo/
├── src/
│   └── calculator/
│       ├── __init__.py     # 核心计算器功能
│       ├── api.py          # FastAPI应用和路由
│       └── lambda_handler.py # AWS Lambda处理函数
├── tests/                  # 测试代码
└── docs/                   # 项目文档
```

## 3. API 接口

### 3.1 接口列表
| 接口 | 方法 | 描述 |
|------|------|------|
| `/add` | POST | 加法运算 |
| `/subtract` | POST | 减法运算 |
| `/multiply` | POST | 乘法运算 |
| `/divide` | POST | 除法运算 |
| `/sqrt` | POST | 平方根计算 |
| `/health` | GET | 健康检查 |

### 3.2 请求/响应格式

#### 双操作数接口（加、减、乘、除）
请求：
```json
{
    "a": 10.5,
    "b": 5.2
}
```

#### 单操作数接口（平方根）
请求：
```json
{
    "value": 16.0
}
```

#### 响应格式
```json
{
    "result": 15.7,
    "operation": "addition"
}
```

### 3.3 错误码
- 400：请求参数错误
- 422：请求数据验证失败
- 500：服务器内部错误

## 4. 本地开发

### 4.1 环境准备
```bash
# 安装依赖
poetry install

# 运行测试
poetry run pytest

# 启动服务
poetry run uvicorn calculator.api:app --reload
```

### 4.2 API 文档访问
- 启动服务后访问：`http://localhost:8000/docs`
- 可以在线测试所有 API 接口 