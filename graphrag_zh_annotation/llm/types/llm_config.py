# 导入一个叫做 Protocol 的工具，它帮助我们定义一种特殊类型的类
from typing import Protocol

# 这是一个版权声明，告诉我们这段代码由微软公司编写，并遵循 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了接下来我们要定义的协议（Protocol）是关于什么的
"""LLM 配置协议定义。"""

# 使用 Protocol 创建一个名为 LLMConfig 的类，这个类描述了一些方法（功能）
class LLMConfig(Protocol):
    # 这个类是用来定义 LLM（可能是“语言学习模型”或类似的东西）的配置标准

    # 定义一个方法，用于获取最大重试次数，返回值可以是整数或者 None
    @property
    def max_retries(self) -> int | None:
        """获取允许的最大重试次数。"""
        # 这里用 "..." 表示这个方法的具体实现不在这里，会在其他地方完成

    # 定义一个方法，用于获取最大重试等待时间，返回值可以是浮点数或者 None
    @property
    def max_retry_wait(self) -> float | None:
        """获取最大重试等待的时间。"""
        # 同上，这个方法的具体实现需要在其他地方查看

    # 定义一个方法，用于获取是否应根据速率限制建议暂停，返回值可以是布尔值或者 None
    @property
    def sleep_on_rate_limit_recommendation(self) -> bool | None:
        """获取是否在遇到速率限制时暂停。"""
        # 这个方法也没有具体实现

    # 定义一个方法，用于获取每分钟可用的令牌数量，返回值可以是整数或者 None
    @property
    def tokens_per_minute(self) -> int | None:
        """获取每分钟可用的令牌数量。"""
        # 同样，没有具体的实现细节

    # 定义一个方法，用于获取每分钟允许的请求数量，返回值可以是整数或者 None
    @property
    def requests_per_minute(self) -> int | None:
        """获取每分钟允许的请求数量。"""
        # 这个方法也是需要在其他地方查看实现的

