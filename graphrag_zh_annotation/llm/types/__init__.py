# 导入模块，这些模块包含了一些特殊的功能
from .llm import LLM                  # 导入LLM类
from .llm_cache import LLMCache       # 导入LLM缓存类
from .llm_callbacks import (         # 导入与LLM相关的回调函数
    ErrorHandlerFn,                 # 错误处理函数
    IsResponseValidFn,              # 检查响应是否有效的函数
    LLMInvocationFn,                # 调用LLM的函数
    OnCacheActionFn,                # 缓存操作时的函数
)
from .llm_config import LLMConfig     # 导入LLM配置类
from .llm_invocation_result import LLMInvocationResult  # 导入调用结果类
from .llm_io import (               # 导入与输入输出相关的类
    LLMInput,                       # LLM的输入类
    LLMOutput,                      # LLM的输出类
)
from .llm_types import (            # 导入不同类型的数据结构
    CompletionInput,                # 完成输入类型
    CompletionLLM,                  # 完成任务的LLM类型
    CompletionOutput,               # 完成输出类型
    EmbeddingInput,                 # 嵌入输入类型
    EmbeddingLLM,                   # 嵌入任务的LLM类型
    EmbeddingOutput,                # 嵌入输出类型
)

# 这一行是版权信息，表示代码由微软公司2024年创建，遵循MIT许可证

# 文档字符串，描述这个文件是用来定义LLM相关类型的
"""LLM Typings."""

# 再次导入相同的模块，确保所有需要的类和函数都在这里列出
from .llm import LLM
from .llm_cache import LLMCache
from .llm_callbacks import (
    ErrorHandlerFn,
    IsResponseValidFn,
    LLMInvocationFn,
    OnCacheActionFn,
)
from .llm_config import LLMConfig
from .llm_invocation_result import LLMInvocationResult
from .llm_io import (
    LLMInput,
    LLMOutput,
)
from .llm_types import (
    CompletionInput,
    CompletionLLM,
    CompletionOutput,
    EmbeddingInput,
    EmbeddingLLM,
    EmbeddingOutput,
)

# 这个列表告诉其他程序，这个模块导出了哪些名字，可以被外部直接使用
__all__ = [
    "LLM",
    "CompletionInput",
    "CompletionLLM",
    "CompletionOutput",
    "EmbeddingInput",
    "EmbeddingLLM",
    "EmbeddingOutput",
    "ErrorHandlerFn",
    "IsResponseValidFn",
    "LLMCache",
    "LLMConfig",
    "LLMInput",
    "LLMInvocationFn",
    "LLMInvocationResult",
    "LLMOutput",
    "OnCacheActionFn",
]

