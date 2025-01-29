#!/usr/bin/env python3
"""
在远程服务器上安装Docker的脚本
"""

import json
import os
import sys
import time
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


def execute_command(ssh, command, check_error=True):
    """执行命令并返回结果"""
    logger.info("执行命令: %s", command)
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    
    if output:
        logger.info("输出: %s", output)
    if error:
        logger.warning("错误: %s", error)
    
    if check_error and exit_status != 0:
        raise Exception(f"命令执行失败: {error}")
    
    return output, error, exit_status


def install_docker(config):
    """在远程服务器上安装Docker"""
    host = config["tencent_host"]["host"]
    username = config["tencent_host"]["username"]
    password = config["tencent_host"]["password"]
    
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接服务器
        logger.info("正在连接服务器 %s...", host)
        ssh.connect(
            hostname=host,
            username=username,
            password=password,
            timeout=10
        )
        
        # 检查是否已安装Docker
        _, _, exit_status = execute_command(ssh, "docker --version", check_error=False)
        if exit_status == 0:
            logger.info("Docker已安装，跳过安装步骤")
            return
        
        # 更新包索引
        logger.info("更新包索引...")
        execute_command(ssh, "sudo apt-get update")
        
        # 安装必要的依赖
        logger.info("安装依赖包...")
        execute_command(ssh, """
            sudo apt-get install -y \\
                apt-transport-https \\
                ca-certificates \\
                curl \\
                gnupg \\
                lsb-release
        """)
        
        # 使用腾讯云镜像源安装Docker
        logger.info("安装Docker...")
        execute_command(ssh, """
            curl -fsSL https://mirrors.cloud.tencent.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
        """)
        
        # 添加Docker软件源
        logger.info("添加Docker软件源...")
        execute_command(ssh, """
            sudo add-apt-repository "deb [arch=amd64] https://mirrors.cloud.tencent.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
        """)
        
        # 再次更新包索引
        logger.info("更新包索引...")
        execute_command(ssh, "sudo apt-get update")
        
        # 安装Docker
        logger.info("安装Docker...")
        execute_command(ssh, "sudo apt-get install -y docker-ce docker-ce-cli containerd.io")
        
        # 将当前用户添加到docker组
        logger.info("将当前用户添加到docker组...")
        execute_command(ssh, "sudo usermod -aG docker $USER")
        
        # 启动Docker服务
        logger.info("启动Docker服务...")
        execute_command(ssh, "sudo systemctl start docker")
        execute_command(ssh, "sudo systemctl enable docker")
        
        # 配置Docker镜像加速
        logger.info("配置Docker镜像加速...")
        execute_command(ssh, """
            sudo mkdir -p /etc/docker
            sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://mirror.ccs.tencentyun.com"]
}
EOF
        """)
        
        # 重启Docker服务
        logger.info("重启Docker服务...")
        execute_command(ssh, "sudo systemctl daemon-reload")
        execute_command(ssh, "sudo systemctl restart docker")
        
        # 验证安装
        logger.info("验证Docker安装...")
        output, _, _ = execute_command(ssh, "docker --version")
        logger.info("Docker安装成功: %s", output)
        
        # 测试Docker运行
        logger.info("测试Docker运行...")
        execute_command(ssh, "sudo docker run hello-world")
        
        # 关闭连接
        ssh.close()
        logger.info("Docker安装和配置完成!")
        
    except Exception as e:
        logger.error("安装失败: %s", str(e))
        sys.exit(1)


def main():
    """主函数"""
    try:
        config = load_config()
        install_docker(config)
    except KeyboardInterrupt:
        logger.info("操作已取消")
        sys.exit(0)
    except Exception as e:
        logger.error("程序执行出错: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 