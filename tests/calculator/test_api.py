"""
计算器API测试模块。
"""

import pytest
from fastapi.testclient import TestClient
from calculator.api import app

client = TestClient(app)


def test_health_check():
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.parametrize(
    "endpoint,data,expected_result,expected_operation",
    [
        ("/add", {"a": 1, "b": 2}, 3, "addition"),
        ("/subtract", {"a": 5, "b": 3}, 2, "subtraction"),
        ("/multiply", {"a": 4, "b": 3}, 12, "multiplication"),
        ("/divide", {"a": 6, "b": 2}, 3, "division"),
        ("/sqrt", {"value": 16}, 4, "square_root"),
    ],
)
def test_calculation_endpoints(endpoint, data, expected_result, expected_operation):
    """测试计算接口"""
    response = client.post(endpoint, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["result"] == expected_result
    assert result["operation"] == expected_operation


def test_divide_by_zero():
    """测试除零错误处理"""
    response = client.post("/divide", json={"a": 1, "b": 0})
    assert response.status_code == 400
    assert "除数不能为0（当前: 被除数=1.0, 除数=0.0）" in response.json()["detail"]


def test_negative_sqrt():
    """测试负数平方根错误处理"""
    response = client.post("/sqrt", json={"value": -1})
    assert response.status_code == 400
    assert "当前输入值: -1" in response.json()["detail"]


@pytest.mark.parametrize(
    "endpoint,invalid_data",
    [
        ("/add", {"a": "invalid", "b": 2}),
        ("/subtract", {"a": 1, "b": "invalid"}),
        ("/multiply", {"a": None, "b": 3}),
        ("/divide", {"a": 6, "b": "invalid"}),
        ("/sqrt", {"value": "invalid"}),
    ],
)
def test_invalid_input_handling(endpoint, invalid_data):
    """测试无效输入处理"""
    response = client.post(endpoint, json=invalid_data)
    assert response.status_code == 422  # FastAPI的验证错误状态码


@pytest.mark.asyncio
async def test_concurrent_requests():
    """测试并发请求处理"""
    import asyncio
    import httpx

    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        tasks = [ac.post("/add", json={"a": i, "b": i}) for i in range(10)]
        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses):
            assert response.status_code == 200
            result = response.json()
            assert result["result"] == i + i
            assert result["operation"] == "addition"
