#!/usr/bin/env python3
"""
测试SSH连接的脚本
"""

import json
import os
import sys
import paramiko
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置文件"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config.local.json"
    )
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("配置文件未找到: %s", config_path)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error("配置文件格式错误: %s", str(e))
        sys.exit(1)


def test_ssh_connection(config):
    """测试SSH连接"""
    host = config["tencent_host"]["host"]
    username = config["tencent_host"]["username"]
    password = config["tencent_host"]["password"]
    
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 尝试连接
        logger.info("正在连接服务器 %s...", host)
        ssh.connect(
            hostname=host,
            username=username,
            password=password,
            timeout=10
        )
        
        # 测试执行命令
        logger.info("执行测试命令...")
        stdin, stdout, stderr = ssh.exec_command("whoami")
        result = stdout.read().decode().strip()
        logger.info("当前用户: %s", result)
        
        # 检查Docker
        logger.info("检查Docker状态...")
        stdin, stdout, stderr = ssh.exec_command("docker --version")
        result = stdout.read().decode().strip()
        logger.info("Docker版本: %s", result)
        
        # 关闭连接
        ssh.close()
        logger.info("连接测试成功!")
        
    except Exception as e:
        logger.error("连接失败: %s", str(e))
        sys.exit(1)


def main():
    """主函数"""
    try:
        config = load_config()
        test_ssh_connection(config)
    except KeyboardInterrupt:
        logger.info("操作已取消")
        sys.exit(0)
    except Exception as e:
        logger.error("程序执行出错: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 