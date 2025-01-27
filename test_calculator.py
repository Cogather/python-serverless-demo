"""计算器模块的测试用例"""
import pytest
from calculator import add, subtract, multiply, divide, sqrt


def test_add():
    """测试加法函数"""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2


def test_subtract():
    """测试减法函数"""
    assert subtract(3, 2) == 1
    assert subtract(1, 1) == 0
    assert subtract(-1, -1) == 0


def test_multiply():
    """测试乘法函数"""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(-2, -3) == 6


def test_divide():
    """测试除法函数"""
    assert divide(6, 2) == 3
    assert divide(-6, 2) == -3
    assert divide(-6, -2) == 3


def test_divide_by_zero():
    """测试除以零的情况"""
    with pytest.raises(ValueError):
        divide(1, 0)


def test_sqrt():
    """测试平方根函数"""
    assert sqrt(4) == 2
    assert sqrt(0) == 0
    assert sqrt(2) == 2**0.5


def test_sqrt_negative():
    """测试计算负数平方根的情况"""
    with pytest.raises(ValueError):
        sqrt(-1)
