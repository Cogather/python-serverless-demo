"""
计算器API模块，提供RESTful API接口。
"""

from typing import Dict, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mangum import Mangum

from . import add, subtract, multiply, divide, sqrt

app = FastAPI(
    title="Calculator API",
    description="一个基于FastAPI的无服务器计算器API",
    version="1.0.0",
)


class CalculationRequest(BaseModel):
    """计算请求模型"""

    a: float = Field(..., description="第一个操作数")
    b: float = Field(..., description="第二个操作数")


class SingleValueRequest(BaseModel):
    """单值请求模型"""

    value: float = Field(..., description="输入值")


class CalculationResponse(BaseModel):
    """计算响应模型"""

    result: float = Field(..., description="计算结果")
    operation: str = Field(..., description="执行的操作")


@app.post("/add", response_model=CalculationResponse)
async def api_add(
    request: CalculationRequest,
) -> Dict[str, Union[float, str]]:
    """加法API"""
    try:
        result = add(request.a, request.b)
        return {"result": result, "operation": "addition"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/subtract", response_model=CalculationResponse)
async def api_subtract(
    request: CalculationRequest,
) -> Dict[str, Union[float, str]]:
    """减法API"""
    try:
        result = subtract(request.a, request.b)
        return {"result": result, "operation": "subtraction"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/multiply", response_model=CalculationResponse)
async def api_multiply(
    request: CalculationRequest,
) -> Dict[str, Union[float, str]]:
    """乘法API"""
    try:
        result = multiply(request.a, request.b)
        return {"result": result, "operation": "multiplication"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/divide", response_model=CalculationResponse)
async def api_divide(
    request: CalculationRequest,
) -> Dict[str, Union[float, str]]:
    """除法API"""
    try:
        result = divide(request.a, request.b)
        return {"result": result, "operation": "division"}
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sqrt", response_model=CalculationResponse)
async def api_sqrt(
    request: SingleValueRequest,
) -> Dict[str, Union[float, str]]:
    """平方根API"""
    try:
        result = sqrt(request.value)
        return {"result": result, "operation": "square_root"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查接口"""
    return {"status": "healthy"}


# AWS Lambda处理器
handler = Mangum(app)

# 测试CI触发
