FROM python:3.10-slim

WORKDIR /app

# 安装 poetry
RUN pip install poetry

# 复制项目文件
COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

# 配置 poetry 不创建虚拟环境（在容器中不需要）
RUN poetry config virtualenvs.create false

# 安装依赖（不包含开发依赖）
RUN poetry install --only main --no-root

# 设置 Python 路径
ENV PYTHONPATH=/app/src

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["poetry", "run", "uvicorn", "calculator.api:app", "--host", "0.0.0.0", "--port", "8000"] 