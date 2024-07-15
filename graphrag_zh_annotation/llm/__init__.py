# 导入基础类
from .base import BaseLLM, CachingLLM, RateLimitingLLM
# 导入错误处理类
from .errors import RetriesExhaustedError
# 导入限流器相关类
from .limiting import (
    CompositeLLMLimiter,  # 复合限流器
    LLMLimiter,           # 基础限流器
    NoopLLMLimiter,       # 无操作限流器
    TpmRpmLLMLimiter,     # TPM/RPM限流器
    create_tpm_rpm_limiters,  # 创建TPM/RPM限流器的方法
)
# 导入模拟器类
from .mock import MockChatLLM, MockCompletionLLM
# 导入OpenAI相关的类和方法
from .openai import (
    OpenAIChatLLM,         # OpenAI聊天逻辑模型
    OpenAIClientTypes,     # OpenAI客户端类型
    OpenAICompletionLLM,   # OpenAI完成逻辑模型
    OpenAIConfiguration,  # OpenAI配置
    OpenAIEmbeddingsLLM,  # OpenAI嵌入式逻辑模型
    create_openai_chat_llm,  # 创建OpenAI聊天逻辑模型的方法
    create_openai_client,  # 创建OpenAI客户端的方法
    create_openai_completion_llm,  # 创建OpenAI完成逻辑模型的方法
    create_openai_embedding_llm,  # 创建OpenAI嵌入式逻辑模型的方法
)
# 导入各种类型定义
from .types import (
    LLM,                  # 逻辑语言模型
    CompletionInput,      # 完成输入
    CompletionLLM,        # 完成逻辑模型
    CompletionOutput,     # 完成输出
    EmbeddingInput,       # 嵌入输入
    EmbeddingLLM,         # 嵌入逻辑模型
    EmbeddingOutput,      # 嵌入输出
    ErrorHandlerFn,       # 错误处理函数类型
    IsResponseValidFn,    # 判断响应是否有效的函数类型
    LLMCache,             # 逻辑语言模型缓存
    LLMConfig,            # 逻辑语言模型配置
    LLMInput,             # 逻辑语言模型输入
    LLMInvocationFn,      # 调用逻辑语言模型的函数类型
    LLMInvocationResult,  # 调用逻辑语言模型的结果
    LLMOutput,            # 逻辑语言模型输出
    OnCacheActionFn,      # 缓存动作处理函数类型
)

# 这段代码是Python写的，用于一个叫做Datashaper OpenAI Utilities的软件包。
# 注释中的(c)表示版权，2024年归Microsoft公司所有。
# 根据MIT许可证，你可以自由使用这个代码。

# 这是一个描述性的字符串，说明这个软件包是关于什么的。
"""The Datashaper OpenAI Utilities package."""

# 导入一些内部模块和类，这些都是这个包中用到的工具。
from .base import BaseLLM, CachingLLM, RateLimitingLLM  # 基础的、缓存的和限速的语言模型
from .errors import RetriesExhaustedError  # 重试次数耗尽错误
from .limiting import (
    CompositeLLMLimiter,  # 复合语言模型限制器
    LLMLimiter,  # 语言模型限制器
    NoopLLMLimiter,  # 无操作限制器
    TpmRpmLLMLimiter,  # TPM/RPM（每分钟事务/请求）限制器
    create_tpm_rpm_limiters,  # 创建TPM/RPM限制器的函数
)
from .mock import MockChatLLM, MockCompletionLLM  # 模拟的聊天和完成语言模型
from .openai import (
    OpenAIChatLLM,  # OpenAI聊天语言模型
    OpenAIClientTypes,  # OpenAI客户端类型
    OpenAICompletionLLM,  # OpenAI完成语言模型
    OpenAIConfiguration,  # OpenAI配置
    OpenAIEmbeddingsLLM,  # OpenAI嵌入式语言模型
    create_openai_chat_llm,  # 创建OpenAI聊天语言模型的函数
    create_openai_client,  # 创建OpenAI客户端的函数
    create_openai_completion_llm,  # 创建OpenAI完成语言模型的函数
    create_openai_embedding_llm,  # 创建OpenAI嵌入式语言模型的函数
)
from .types import (
    LLM,  # 语言模型的基类
    CompletionInput,  # 完成输入
    CompletionLLM,  # 完成语言模型
    CompletionOutput,  # 完成输出
    EmbeddingInput,  # 嵌入输入
    EmbeddingLLM,  # 嵌入语言模型
    EmbeddingOutput,  # 嵌入输出
    ErrorHandlerFn,  # 错误处理函数
    IsResponseValidFn,  # 验证响应是否有效的函数
    LLMCache,  # 语言模型缓存
    LLMConfig,  # 语言模型配置
    LLMInput,  # 语言模型输入
    LLMInvocationFn,  # 调用语言模型的函数
    LLMInvocationResult,  # 调用结果
    LLMOutput,  # 语言模型输出
    OnCacheActionFn,  # 缓存操作回调函数
)

# 这个列表定义了对外公开的所有模块、类和函数，其他程序可以使用这些公开的元素。
__all__ = [
    # 语言模型类型
    "LLM", "BaseLLM", "CachingLLM", "CompletionInput", "CompletionLLM", "CompletionOutput",
    "CompositeLLMLimiter", "EmbeddingInput", "EmbeddingLLM", "EmbeddingOutput",
    # 回调函数
    "ErrorHandlerFn", "IsResponseValidFn",
    # 缓存相关
    "LLMCache", "LLMConfig",
    # 语言模型输入输出类型
    "LLMInput", "LLMInvocationFn", "LLMInvocationResult", "LLMLimiter", "LLMOutput",
    "MockChatLLM",
    # 模拟相关
    "MockCompletionLLM", "NoopLLMLimiter", "OnCacheActionFn",
    "OpenAIChatLLM", "OpenAIClientTypes", "OpenAICompletionLLM",
    # OpenAI相关
    "OpenAIConfiguration", "OpenAIEmbeddingsLLM", "RateLimitingLLM",
    # 错误
    "RetriesExhaustedError", "TpmRpmLLMLimiter",
    # 创建函数
    "create_openai_chat_llm", "create_openai_client", "create_openai_completion_llm",
    "create_openai_embedding_llm",
    # 限制器
    "create_tpm_rpm_limiters",
]

