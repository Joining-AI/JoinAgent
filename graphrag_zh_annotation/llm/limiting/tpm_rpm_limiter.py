# 导入了一个叫做AsyncLimiter的模块，它用于限制操作的速度
from aiolimiter import AsyncLimiter

# 导入了另一个叫做LLMLimiter的类，这个类可能也是用来限制速度的
from .llm_limiter import LLMLimiter

# 这是版权声明，告诉我们这段代码是微软公司2024年的作品，使用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# TPM RPM Limiter模块的文档字符串，简单描述了这个模块的作用
"""TPM RPM Limiter模块。"""

# 再次导入AsyncLimiter，这可能是为了保持代码的整洁
from aiolimiter import AsyncLimiter

# 再次导入LLMLimiter，同上
from .llm_limiter import LLMLimiter

# 定义了一个新的类TpmRpmLLMLimiter，它是LLMLimiter的子类，专门用于限制TPM和RPM
class TpmRpmLLMLimiter(LLMLimiter):
    # 这两个变量可能存储了两种不同类型的限制器，它们可以是AsyncLimiter对象，也可以是None
    _tpm_limiter: AsyncLimiter | None
    _rpm_limiter: AsyncLimiter | None

    # 构造函数，当创建这个类的实例时会调用
    def __init__(self, tpm_limiter: AsyncLimiter | None, rpm_limiter: AsyncLimiter | None):
        # 把传入的限制器对象分别保存到对应的成员变量中
        self._tpm_limiter = tpm_limiter
        self._rpm_limiter = rpm_limiter

    # 这个方法检查是否需要传递令牌数量
    def needs_token_count(self) -> bool:
        # 如果_tpm_limiter不是None，说明需要令牌数量，返回True
        return self._tpm_limiter is not None

    # 异步获取方法，用于限制操作
    async def acquire(self, num_tokens: int = 1) -> None:
        # 如果_tpm_limiter存在，就尝试获取num_tokens个令牌
        if self._tpm_limiter is not None:
            await self._tpm_limiter.acquire(num_tokens)
        # 如果_rpm_limiter存在，就尝试获取一个令牌（默认值）
        if self._rpm_limiter is not None:
            await self._rpm_limiter.acquire()

