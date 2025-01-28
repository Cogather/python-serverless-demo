"""
计算器模块的单元测试。
"""

import sys
import pytest
from calculator import add, subtract, multiply, divide, sqrt


# 基本功能测试
def test_add():
    """测试加法功能"""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0


def test_subtract():
    """测试减法功能"""
    assert subtract(3, 2) == 1
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5
    assert subtract(2.5, 1.5) == 1.0


def test_multiply():
    """测试乘法功能"""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0
    assert multiply(2.5, 2) == 5.0


def test_divide():
    """测试除法功能"""
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    assert divide(0, 5) == 0
    assert divide(-6, 2) == -3

    # 测试除以0的情况
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide(1, 0)
    assert "被除数=1, 除数=0" in str(exc_info.value)


def test_sqrt():
    """测试平方根功能"""
    assert sqrt(4) == 2
    assert sqrt(0) == 0
    assert sqrt(2) == pytest.approx(1.4142135623730951)

    # 测试负数的情况
    with pytest.raises(ValueError) as exc_info:
        sqrt(-1)
    assert "当前输入值: -1" in str(exc_info.value)


# 边界值测试
def test_boundary_values():
    """测试边界值情况"""
    # 测试最大浮点数
    max_float = sys.float_info.max
    assert add(max_float, 0) == max_float
    assert subtract(max_float, 0) == max_float
    assert multiply(max_float, 1) == max_float
    assert divide(max_float, 1) == max_float

    # 测试最小浮点数
    min_float = sys.float_info.min
    assert add(min_float, 0) == min_float
    assert subtract(min_float, 0) == min_float
    assert multiply(min_float, 1) == min_float
    assert divide(min_float, 1) == min_float

    # 测试接近于0的值
    epsilon = sys.float_info.epsilon
    assert sqrt(epsilon) == pytest.approx(pow(epsilon, 0.5))


# 参数类型测试
@pytest.mark.parametrize(
    "value",
    [
        1,  # 整数
        1.0,  # 浮点数
        int(1),  # 显式整数
        float(1.0),  # 显式浮点数
        1.1234567890,  # 高精度浮点数
    ],
)
def test_type_handling(value):
    """测试不同数值类型的处理"""
    assert add(value, 0) == value
    assert subtract(value, 0) == value
    assert multiply(value, 1) == value
    assert divide(value, 1) == value
    if value >= 0:
        assert sqrt(value * value) == pytest.approx(value)


# 性能测试
@pytest.mark.benchmark(
    group="calculator",
    min_rounds=100,
    disable_gc=True,
    warmup=True
)
def test_performance_sqrt(benchmark):
    """测试平方根计算的性能"""

    def run_sqrt():
        for i in range(1000):
            sqrt(i)

    benchmark(run_sqrt)


@pytest.mark.benchmark(
    group="calculator",
    min_rounds=100,
    disable_gc=True,
    warmup=True
)
def test_performance_operations(benchmark):
    """测试基本运算的性能"""

    def run_operations():
        for i in range(1000):
            add(i, i)
            subtract(i, i)
            multiply(i, i)
            if i != 0:
                divide(i, i)

    # 执行基准测试
    benchmark(run_operations)
