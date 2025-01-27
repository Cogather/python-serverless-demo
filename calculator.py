"""简单的计算器模块"""


def add(a: float, b: float) -> float:
    """加法函数"""
    return a + b


def subtract(a: float, b: float) -> float:
    """减法函数"""
    return a - b


def multiply(a: float, b: float) -> float:
    """乘法函数"""
    return a * b


def divide(a: float, b: float) -> float:
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b


def sqrt(x: float) -> float:
    """计算平方根
    
    Args:
        x: 要计算平方根的数
        
    Returns:
        平方根结果
        
    Raises:
        ValueError: 当输入为负数时抛出异常
    """
    if x < 0:
        raise ValueError("不能计算负数的平方根")
    return x ** 0.5