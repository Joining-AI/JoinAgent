# 导入logging模块，用于记录程序运行时的信息
import logging

# 导入os模块，它包含与操作系统交互的函数
import os

# 使用pathlib模块，它提供了处理文件路径的类和方法
from pathlib import Path

# 导入dotenv模块，它能读取.env文件中的键值对
from dotenv import dotenv_values

# 这是微软公司的版权声明，表示代码由微软编写
# 并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块的作用
"""一个模块，包含了读取.env文件的工具函数。"""

# 初始化日志记录器，用于打印程序运行信息
log = logging.getLogger(__name__)

# 定义一个名为read_dotenv的函数，接收一个参数root，表示根目录路径
def read_dotenv(root: str) -> None:
    # 创建一个.pathlib.Path对象，表示.env文件的路径
    env_path = Path(root) / ".env"

    # 检查.env文件是否存在
    if env_path.exists():
        # 如果存在，打印信息并读取文件内容
        log.info("加载pipeline的.env文件")
        # 使用dotenv_values函数读取.env文件的内容
        env_config = dotenv_values(f"{env_path}")
        
        # 遍历.env文件中所有的键值对
        for key, value in env_config.items():
            # 如果键不在当前环境变量中
            if key not in os.environ:
                # 将键值对添加到环境变量中，如果值为空，则设置为空字符串
                os.environ[key] = value or ""
    else:
        # 如果.env文件不存在，打印一条信息
        log.info("在%s未找到.env文件", root)

