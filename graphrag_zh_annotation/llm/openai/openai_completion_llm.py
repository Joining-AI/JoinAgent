# 导入logging模块，它用于记录程序运行时的日志信息
import logging

# 从typing_extensions库中导入Unpack，这是一个类型注解工具，帮助我们处理元组解包
from typing_extensions import Unpack

# 从graphrag.llm.base导入BaseLLM类，这是基础的LLM（语言模型）类
from graphrag.llm.base import BaseLLM

# 从graphrag.llm.types导入一些数据类型，用于表示输入和输出
from graphrag.llm.types import CompletionInput, CompletionOutput, LLMInput

# 从当前模块的子目录.openai_configuration导入OpenAIConfiguration类，这可能与OpenAI API配置有关
from .openai_configuration import OpenAIConfiguration

# 从当前模块的子目录.types导入OpenAIClientTypes，这可能是OpenAI客户端的特定数据类型
from .types import OpenAIClientTypes

# 从当前模块的子目录.utils导入get_completion_llm_args函数，它用于获取完成LLM所需的一些参数
from .utils import get_completion_llm_args

# 这是版权信息，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个基于文本完成的LLM（语言模型）
class OpenAICompletionLLM(BaseLLM[CompletionInput, CompletionOutput]):

    # 初始化成员变量，包括OpenAI客户端和配置
    _client: OpenAIClientTypes
    _configuration: OpenAIConfiguration

    # 构造函数，用于创建OpenAICompletionLLM实例，传入OpenAI客户端和配置
    def __init__(self, client: OpenAIClientTypes, configuration: OpenAIConfiguration):
        self.client = client
        self.configuration = configuration

    # 异步方法，执行LLM任务，输入是CompletionInput，其他参数用**kwargs接收
    async def _execute_llm(
        self,
        input: CompletionInput,
        **kwargs: Unpack[LLMInput],
    ) -> CompletionOutput | None:

        # 获取完成LLM所需的参数，使用kwargs中的model_parameters和配置
        args = get_completion_llm_args(
            kwargs.get("model_parameters"), self.configuration
        )

        # 使用OpenAI客户端的completions.create方法，完成输入文本
        completion = self.client.completions.create(prompt=input, **args)

        # 返回完成后的第一个选择的文本内容
        return completion.choices[0].text

