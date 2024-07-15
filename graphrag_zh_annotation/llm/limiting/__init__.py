# 导入一些工具模块，让程序能用到特别的功能
from .composite_limiter import CompositeLLMLimiter  # 引入复合限制器
from .create_limiters import create_tpm_rpm_limiters  # 引入创建限制器的函数
from .llm_limiter import LLMLimiter  # 引入基本的限制器
from .noop_llm_limiter import NoopLLMLimiter  # 引入无操作限制器（不做任何限制）
from .tpm_rpm_limiter import TpmRpmLLMLimiter  # 引入TPM/RPM限制器

# 这是微软公司的版权信息，表示这个代码由他们编写
# 并且遵循MIT许可证，允许他人自由使用和修改

# 这个模块关于限制器的文档注释
"""LLM限制器模块。"""

# 再次导入上面的模块，确保它们在模块中可见
from .composite_limiter import CompositeLLMLimiter
from .create_limiters import create_tpm_rpm_limiters
from .llm_limiter import LLMLimiter
from .noop_llm_limiter import NoopLLMLimiter
from .tpm_rpm_limiter import TpmRpmLLMLimiter

# 这个列表告诉别人这个模块里有哪些东西可以使用
# 这些都是上面导入的类和函数
__all__ = [
    "CompositeLLMLimiter",  # 复合限制器
    "LLMLimiter",  # 基本限制器
    "NoopLLMLimiter",  # 无操作限制器
    "TpmRpmLLMLimiter",  # TPM/RPM限制器
    "create_tpm_rpm_limiters",  # 创建限制器的函数
]

