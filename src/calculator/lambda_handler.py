"""
AWS Lambda处理函数模块。
"""

import json
from typing import Dict, Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from .api import handler

# 配置日志
logger = Logger()


@logger.inject_lambda_context
def lambda_handler(
    event: Dict[str, Any], context: LambdaContext
) -> Dict[str, Any]:
    """
    AWS Lambda处理函数，用于处理API Gateway的请求。
    
    Args:
        event: API Gateway事件
        context: Lambda上下文
        
    Returns:
        API响应
    """
    try:
        # 使用Mangum处理API Gateway事件
        response = handler(event, context)
        return response
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
