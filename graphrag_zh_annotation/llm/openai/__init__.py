# 导入一个名为`create_openai_client`的函数，它来自当前文件夹中的另一个模块.create_openai_client
from .create_openai_client import create_openai_client

# 从.factories模块导入三个创建不同OpenAI模型的函数
from .factories import (
    create_openai_chat_llm,  # 创建用于聊天的OpenAI模型
    create_openai_completion_llm,  # 创建用于文本完成的OpenAI模型
    create_openai_embedding_llm,  # 创建用于生成文本嵌入的OpenAI模型
)

# 导入OpenAIChatLLM类，这是用于聊天的特定OpenAI模型
from .openai_chat_llm import OpenAIChatLLM

# 导入OpenAICompletionLLM类，这是用于文本完成的OpenAI模型
from .openai_completion_llm import OpenAICompletionLLM

# 导入OpenAIConfiguration类，用于设置和管理OpenAI API的配置信息
from .openai_configuration import OpenAIConfiguration

# 导入OpenAIEmbeddingsLLM类，用于处理文本嵌入的OpenAI模型
from .openai_embeddings_llm import OpenAIEmbeddingsLLM

# 导入OpenAIClientTypes，这是一个枚举类型，可能包含了OpenAI客户端的不同类型
from .types import OpenAIClientTypes

# 这是版权声明，表示这段代码由微软公司所有，遵循MIT许可证

# 这个模块公开的（可以被其他模块直接使用的）内容列表
__all__ = [
    "OpenAIChatLLM",  # 聊天模型类
    "OpenAIClientTypes",  # 客户端类型枚举
    "OpenAICompletionLLM",  # 文本完成模型类
    "OpenAIConfiguration",  # 配置类
    "OpenAIEmbeddingsLLM",  # 嵌入模型类
    "create_openai_chat_llm",  # 创建聊天模型的函数
    "create_openai_client",  # 创建OpenAI客户端的函数
    "create_openai_completion_llm",  # 创建文本完成模型的函数
    "create_openai_embedding_llm",  # 创建嵌入模型的函数
]

