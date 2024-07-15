# 导入基础类和方法
from abc import ABC, abstractmethod  # 引入抽象基类和抽象方法
from dataclasses import dataclass  # 引入数据类，用于创建结构化数据
from typing import Any  # 引入Any类型，表示可以是任何类型

# 导入特定库
import tiktoken  # 引入处理token的库
from graphrag.query.context_builder.builders import (  # 引入构建上下文的类
    GlobalContextBuilder,  # 全局上下文构建器
    LocalContextBuilder,  # 局部上下文构建器
)
from graphrag.query.llm.base import BaseLLM  # 引入基础语言模型类

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.  # 微软公司2024年的版权
# Licensed under the MIT License  # 使用MIT许可证授权

# 定义问题结果的数据类
@dataclass
class QuestionResult:
    response: list[str]  # 生成的问题列表
    context_data: str | dict[str, Any]  # 上下文数据，可能是字符串或字典
    completion_time: float  # 完成时间（以秒为单位）
    llm_calls: int  # 调用语言模型的次数
    prompt_tokens: int  # 提示令牌的数量

# 定义问题生成器的抽象基类
class BaseQuestionGen(ABC):
    # 初始化方法
    def __init__(
        self,
        llm: BaseLLM,  # 语言模型对象
        context_builder: GlobalContextBuilder | LocalContextBuilder,  # 上下文构建器对象
        token_encoder: tiktoken.Encoding | None = None,  # 令牌编码器，可能为空
        llm_params: dict[str, Any] | None = None,  # 语言模型参数，可能为空
        context_builder_params: dict[str, Any] | None = None,  # 上下文构建器参数，可能为空
    ):
        self.llm = llm  # 保存语言模型
        self.context_builder = context_builder  # 保存上下文构建器
        self.token_encoder = token_encoder  # 保存令牌编码器
        self.llm_params = llm_params or {}  # 保存语言模型参数，如果为空则设为{}
        self.context_builder_params = context_builder_params or {}  # 保存上下文构建器参数，如果为空则设为{}

    # 抽象方法：同步生成问题
    @abstractmethod
    def generate(
        self,
        question_history: list[str],  # 之前的问题历史
        context_data: str | None,  # 上下文数据，可能为空
        question_count: int,  # 需要生成的问题数量
        **kwargs,  # 其他任意参数
    ) -> QuestionResult:
        """根据问题历史和上下文生成问题"""
        
    # 抽象方法：异步生成问题
    @abstractmethod
    async def agenerate(
        self,
        question_history: list[str],
        context_data: str | None,
        question_count: int,
        **kwargs,
    ) -> QuestionResult:
        """异步方式根据问题历史和上下文生成问题"""

