"""
计算器模块的核心功能实现。
提供基本的数学运算功能。
"""

import math


def add(a: float, b: float) -> float:
    """
    执行加法运算。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两个数的和
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    执行减法运算。

    Args:
        a: 被减数
        b: 减数

    Returns:
        两个数的差
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    执行乘法运算。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两个数的积
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    执行除法运算。

    Args:
        a: 被除数
        b: 除数

    Returns:
        两个数的商

    Raises:
        ZeroDivisionError: 当除数为0时抛出
    """
    if b == 0:
        raise ZeroDivisionError(f"除数不能为0（当前: 被除数={a}, 除数={b}）")
    return a / b


def sqrt(x: float) -> float:
    """
    计算平方根。

    Args:
        x: 要计算平方根的数

    Returns:
        x的平方根

    Raises:
        ValueError: 当x为负数时抛出
    """
    if x < 0:
        raise ValueError(f"不能计算负数的平方根（当前输入值: {x}）")
    return math.sqrt(x)
