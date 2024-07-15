# 这段代码是用来创建搜索算法的基础类的。
# 它使用了一些Python库来帮助处理数据和逻辑。

# 首先，它从abc模块导入了ABC和abstractmethod，这两个是用于创建抽象基类的工具。
from abc import ABC, abstractmethod

# 接着，它导入了dataclasses模块，这个模块用来创建带有默认值的数据类。
from dataclasses import dataclass

# 从typing模块导入Any类型，这是一个可以代表任何类型的占位符。
from typing import Any

# 导入pandas库，这个库用于处理表格数据，比如电子表格。
import pandas as pd

# 导入tiktoken库，这个库可能是一个特定的、与搜索或查询相关的库，但具体功能未知。
import tiktoken

# 从graphrag.query.context_builder.builders导入两个类：GlobalContextBuilder和LocalContextBuilder。
# 这些类可能用于构建搜索上下文。
from graphrag.query.context_builder.builders import (
    GlobalContextBuilder,
    LocalContextBuilder,
)

# 从graphrag.query.context_builder.conversation_history导入ConversationHistory类。
# 这个类可能记录了之前的对话历史，对搜索有帮助。
from graphrag.query.context_builder.conversation_history import (
    ConversationHistory,
)

# 从graphrag.query.llm.base导入BaseLLM类，这个可能是基础的语言模型类。
from graphrag.query.llm.base import BaseLLM

# 下面这段版权信息表示代码归微软公司所有，并遵循MIT许可证。
# 注释部分可以忽略，不影响代码运行。

# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为SearchResult的数据类。
@dataclass
class SearchResult:
    # response字段存储搜索结果，可以是字符串、字典或列表。
    response: str | dict[str, Any] | list[dict[str, Any]]
    # context_data存储搜索上下文的数据，可以是字符串、DataFrame列表或字典。
    context_data: str | list[pd.DataFrame] | dict[str, pd.DataFrame]
    # context_text字段存储上下文窗口中的实际文本，可以是字符串、字符串列表或字典。
    context_text: str | list[str] | dict[str, str]
    # completion_time存储完成搜索的时间（以秒为单位）。
    completion_time: float
    # llm_calls记录调用语言模型的次数。
    llm_calls: int
    # prompt_tokens记录用于查询的提示令牌数量。
    prompt_tokens: int

# 定义一个名为BaseSearch的类，它继承自一个叫ABC的抽象基类
class BaseSearch(ABC):
    """这是一个基础的搜索实现类。"""

    # 初始化方法，当创建BaseSearch对象时会执行这个方法
    def __init__(
        self,
        llm: BaseLLM,          # 接收一个类型为BaseLLM的对象，作为语言模型
        context_builder: GlobalContextBuilder | LocalContextBuilder,  # 接收一个全局或局部上下文构建器对象
        token_encoder: tiktoken.Encoding | None = None,  # 可选的，接收一个tiktoken编码器对象，如果没有则为None
        llm_params: dict[str, Any] | None = None,  # 可选的，接收一个字典，包含语言模型的参数，如果没有则为空字典
        context_builder_params: dict[str, Any] | None = None,  # 可选的，接收一个字典，包含上下文构建器的参数，如果没有则为空字典
    ):
        # 将传入的参数赋值给对象的属性
        self.llm = llm
        self.context_builder = context_builder
        self.token_encoder = token_encoder
        self.llm_params = llm_params or {}  # 如果llm_params是None，则用空字典替代
        self.context_builder_params = context_builder_params or {}  # 如果context_builder_params是None，则用空字典替代

    # 标记为抽象方法的search方法，必须在子类中实现
    @abstractmethod
    def search(
        self,
        query: str,  # 接收一个字符串作为查询内容
        conversation_history: ConversationHistory | None = None,  # 可选的，接收一个对话历史对象，如果没有则为None
        **kwargs,  # 其他任意键值对参数
    ) -> SearchResult:  # 返回一个SearchResult对象
        """根据给定的查询进行搜索。"""

    # 同样标记为抽象方法的异步search方法，也必须在子类中实现
    @abstractmethod
    async def asearch(
        self,
        query: str,  # 同上，接收一个字符串作为查询内容
        conversation_history: ConversationHistory | None = None,  # 同上，可选的对话历史对象
        **kwargs,  # 其他任意键值对参数
    ) -> SearchResult:  # 返回一个SearchResult对象
        """异步地根据给定的查询进行搜索。"""

