# 导入一些特殊的工具
from typing_extensions import Unpack  # 这个是用来帮助我们理解函数参数类型的
from graphrag.llm.base import BaseLLM  # 引入一个基础的类，用于处理语言模型
from graphrag.llm.types import (  # 引入一些数据类型定义
    EmbeddingInput,  # 输入是关于嵌入（词向量）的信息
    EmbeddingOutput,  # 输出也是关于嵌入的信息
    LLMInput,  # 语言模型的一般输入信息
)
from .openai_configuration import OpenAIConfiguration  # 引入OpenAI的配置类
from .types import OpenAIClientTypes  # 引入OpenAI客户端的数据类型

# 这是版权信息，表示这个代码由微软公司所有，遵循MIT许可证

# 下面定义了一个类，叫做OpenAIEmbeddingsLLM
class OpenAIEmbeddingsLLM(BaseLLM[EmbeddingInput, EmbeddingOutput]):
    # 这个类是从BaseLLM继承的，专门用来生成文本嵌入（词向量）的语言模型

    # 这里有两个成员变量，一个是客户端对象，另一个是配置对象
    _client: OpenAIClientTypes
    _configuration: OpenAIConfiguration

    # 类的初始化方法，当我们创建一个实例时会调用
    def __init__(self, client: OpenAIClientTypes, configuration: OpenAIConfiguration):
        # 把传入的客户端和配置对象分别赋值给类的成员
        self.client = client
        self.configuration = configuration

    # 这是一个异步方法，用于执行语言模型任务
    async def _execute_llm(
        self, input: EmbeddingInput, **kwargs: Unpack[LLMInput]
    ) -> EmbeddingOutput | None:
        # 准备要传递给模型的参数，包括模型名称和可能的其他模型参数
        args = {
            "model": self.configuration.model,  # 使用配置中的模型名
            **(kwargs.get("model_parameters") or {}),  # 可能有的额外模型参数
        }

        # 调用客户端的embeddings.create方法，传入输入和参数
        embedding = await self.client.embeddings.create(
            input=input,
            **args,
        )

        # 提取每个数据点的嵌入向量并返回，如果没数据则返回None
        return [d.embedding for d in embedding.data]

