# 导入两个抽象基类和一个类型提示模块
from abc import ABC, abstractmethod  # ABC是抽象基类，abstractmethod用于定义抽象方法
from typing import Any  # Any表示可以是任何类型的变量

# 这是一个版权信息，表示代码归微软公司所有
# Licensed under the MIT License 表示代码遵循MIT许可证

# 定义一个基础类，用于LLM（可能是“语言模型”）回调函数
class BaseLLMCallback:
    # 初始化函数，创建一个空列表来存储响应
    def __init__(self):
        self.response = []

    # 当生成新的令牌（可能是单词或短语）时调用的方法
    def on_llm_new_token(self, token: str):
        # 将新生成的令牌添加到响应列表中
        self.response.append(token)

# 定义一个抽象基类，用于LLM的基础实现
class BaseLLM(ABC):
    # 一个抽象方法，用于生成响应，需要在子类中实现
    @abstractmethod
    def generate(
        self,
        messages: str | list[Any],  # 输入可以是字符串或任何类型的列表
        streaming: bool = True,  # 默认开启流式处理
        callbacks: list[BaseLLMCallback] | None = None,  # 可选的回调函数列表
        **kwargs: Any,  # 其他任意参数
    ) -> str:
        # 返回生成的响应
        pass

    # 另一个抽象方法，异步生成响应，也需要在子类中实现
    @abstractmethod
    async def agenerate(
        self,
        messages: str | list[Any],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        # 异步返回生成的响应
        pass


# 定义一个文本嵌入的抽象基类
class BaseTextEmbedding(ABC):
    # 一个抽象方法，用于将文本转换成向量，需要在子类中实现
    @abstractmethod
    def embed(self, text: str, **kwargs: Any) -> list[float]:  # 输入是字符串，返回浮点数列表
        # 返回文本的嵌入向量
        pass

    # 另一个抽象方法，异步将文本转换成向量
    @abstractmethod
    async def aembed(self, text: str, **kwargs: Any) -> list[float]:
        # 异步返回文本的嵌入向量
        pass

