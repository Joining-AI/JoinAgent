# 导入一个叫做 LLMLimiter 的东西，它来自当前模块的子路径 .llm_limiter
from .llm_limiter import LLMLimiter

# 这是微软公司的版权信息，告诉我们代码的使用权
# 它遵循 MIT 许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块里有一个关于“复合限制器”（Composite Limiter）的定义
# "A module containing Composite Limiter class definition."

# 再次导入 LLMLimiter，可能是为了方便使用
from .llm_limiter import LLMLimiter

# 定义一个叫 CompositeLLMLimiter 的类，它是 LLMLimiter 类的子类
class CompositeLLMLimiter(LLMLimiter):
    # 这个类用来组合多个 LLMLimiter 实例
    """Composite Limiter class definition."""

    # 这个类有一个属性，叫 _limiters，它是一个包含 LLMLimiter 对象的列表
    _limiters: list[LLMLimiter]

    # 构造函数，当我们创建这个类的实例时会用到
    def __init__(self, limiters: list[LLMLimiter]):
        # 把传入的 limiters 列表赋值给 _limiters
        self._limiters = limiters

    # 这个方法告诉我们这个限制器是否需要知道令牌的数量
    @property
    def needs_token_count(self) -> bool:
        # 如果列表中的任何限制器需要令牌数量，就返回 True
        return any(limiter.needs_token_count for limiter in self._limiters)

    # 这个方法用于获取令牌，可以设置获取的数量，默认是 1
    async def acquire(self, num_tokens: int = 1) -> None:
        # 遍历 _limiters 列表中的每个限制器
        for limiter in self._limiters:
            # 对每个限制器调用它的 acquire 方法，传入令牌数量
            await limiter.acquire(num_tokens)

