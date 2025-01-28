"""
计算器模块的单元测试。
"""

import pytest
from calculator import add, subtract, multiply, divide, sqrt


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
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_sqrt():
    """测试平方根功能"""
    assert sqrt(4) == 2
    assert sqrt(0) == 0
    assert sqrt(2) == pytest.approx(1.4142135623730951)
    
    # 测试负数的情况
    with pytest.raises(ValueError):
        sqrt(-1) 