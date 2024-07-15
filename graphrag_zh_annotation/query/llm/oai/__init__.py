# 导入基础模块
from .base import BaseOpenAILLM, OpenAILLMImpl, OpenAITextEmbeddingImpl
# 这些是不同类型的类，帮助处理OpenAI的文本和聊天功能

from .chat_openai import ChatOpenAI
# 导入ChatOpenAI类，用于与OpenAI进行聊天交互

from .embedding import OpenAIEmbedding
# 导入OpenAIEmbedding类，处理文本嵌入（将文本转化为数字表示）

from .openai import OpenAI
# 导入OpenAI类，它是与OpenAI API交互的主要接口

from .typing import OPENAI_RETRY_ERROR_TYPES, OpenaiApiType
# 导入两个常量，一个是错误重试类型列表，另一个是OpenAI API的类型枚举

# 版权声明
# 2024年微软公司的代码
# 根据MIT许可证授权

# 这段文字描述了这个代码的作用
"""GraphRAG Orchestration OpenAI Wrappers."""

# 将以下这些名字公开给其他文件使用
__all__ = [
    # 错误重试的类型
    "OPENAI_RETRY_ERROR_TYPES",
    # 基础的OpenAI语言模型类
    "BaseOpenAILLM",
    # 聊天用的OpenAI类
    "ChatOpenAI",
    # 主要的OpenAI接口类
    "OpenAI",
    # 处理文本嵌入的类
    "OpenAIEmbedding",
    # OpenAI语言模型的实现类
    "OpenAILLMImpl",
    # 文本嵌入的OpenAI实现类
    "OpenAITextEmbeddingImpl",
    # OpenAI API的类型
    "OpenaiApiType",
]

