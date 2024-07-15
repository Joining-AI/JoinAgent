# 导入一个叫做 LLMLimiter 的东西，它来自 .llm_limiter 模块
from .llm_limiter import LLMLimiter

# 这里是微软公司2024年的版权信息，用的是 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# TPM RPM Limiter 模块的说明
"""TPM RPM Limiter 模块."""

# 再次导入 LLMLimiter，这样我们可以在下面的类中使用它
from .llm_limiter import LLMLimiter

# 定义一个叫做 NoopLLMLimiter 的新类，它继承自 LLMLimiter 类
class NoopLLMLimiter(LLMLimiter):
    # NoopLLMLimiter 类的描述
    """TPM RPM Limiter 的类定义."""

    # 这个方法告诉我们这个限制器是否需要令牌数量
    # 如果返回 False，表示不需要
    @property
    def needs_token_count(self) -> bool:
        """是否需要传递令牌数量进来。"""
        return False

    # 这是一个异步方法，用于获取（获取的意思是使用）令牌
    # 参数 num_tokens 默认为 1
    async def acquire(self, num_tokens: int = 1) -> None:
        """调用方法的定义。"""
        # 这个方法什么也不做，只是空过
        # 所以叫 "Noop"，意思是“无操作”

