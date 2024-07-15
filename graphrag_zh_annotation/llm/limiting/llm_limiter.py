# 导入抽象基类和抽象方法模块
from abc import ABC, abstractmethod

# 这是一个版权声明，告诉我们这段代码的版权属于微软公司，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个代码的作用，是关于限制类型的
"""Limiting types."""

# 定义一个抽象基类（Abstract Base Class），叫做LLMLimiter
class LLMLimiter(ABC):
    # 这个类是一个接口，用于限制某些操作
    """LLM Limiter Interface."""

    # 定义一个属性，它是抽象方法，意味着子类必须实现它
    @property
    @abstractmethod
    def needs_token_count(self) -> bool:
        # 这个方法检查是否需要传递令牌计数
        """Whether this limiter needs the token count to be passed in."""

    # 定义一个异步抽象方法，子类也需要实现
    @abstractmethod
    async def acquire(self, num_tokens: int = 1) -> None:
        # 这个方法用于获取通过限制器的权限，可以传入令牌数量，默认为1
        """Acquire a pass through the limiter."""

