# 导入logging模块，它用于记录程序运行时的信息
import logging

# 导入JSONDecodeError，当尝试解析无效的JSON数据时会抛出这个错误
from json import JSONDecodeError

# 从typing_extensions导入Unpack，这是一个类型注解工具，用于元组解包
from typing_extensions import Unpack

# 从graphrag.llm.base导入BaseLLM，这是基本的语言模型类
from graphrag.llm.base import BaseLLM

# 从graphrag.llm.types导入一些数据类型定义
from graphrag.llm.types import (
    CompletionInput,  # 完成输入的数据类型
    CompletionOutput,  # 完成输出的数据类型
    LLMInput,  # 语言模型输入的数据类型
    LLMOutput,  # 语言模型输出的数据类型
)

# 从本模块的_json子模块导入clean_up_json函数，用来清理和格式化JSON数据
from ._json import clean_up_json

# 从本模块的_prompts子模块导入JSON_CHECK_PROMPT，可能是一个用于检查JSON的提示
from ._prompts import JSON_CHECK_PROMPT

# 从.openai_configuration导入OpenAIConfiguration，可能与OpenAI API配置有关
from .openai_configuration import OpenAIConfiguration

# 从.types模块导入OpenAIClientTypes，这可能是OpenAI客户端的一些特定类型
from .types import OpenAIClientTypes

# 从.utils模块导入一些辅助函数
from .utils import (
    get_completion_llm_args,  # 获取完成语言模型所需参数的函数
    try_parse_json_object,  # 尝试解析JSON对象的函数
)

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个基于聊天的语言模型
"""The Chat-based language model."""

# 初始化日志记录器，名为__name__（当前模块的名字）
log = logging.getLogger(__name__)

# 设置最大生成重试次数为3次
_MAX_GENERATION_RETRIES = 3

# 定义一个错误信息字符串，当无法生成有效的JSON输出时使用
FAILED_TO_CREATE_JSON_ERROR = "Failed to generate valid JSON output"

# 这个代码定义了一个名为OpenAIChatLLM的类，它用于与OpenAI的语言模型进行对话。
class OpenAIChatLLM(BaseLLM[CompletionInput, CompletionOutput]):
    # 类的注释说明这是一个基于聊天的LLM（Language Model）。
    """A Chat-based LLM."""

    # 这两个变量是类的成员，用来存储OpenAI的客户端和配置信息。
    _client: OpenAIClientTypes
    _configuration: OpenAIConfiguration

    # 这是类的初始化方法，当创建一个新的OpenAIChatLLM对象时会调用它。
    def __init__(self, client: OpenAIClientTypes, configuration: OpenAIConfiguration):
        # 设置客户端和配置信息
        self.client = client
        self.configuration = configuration

    # 这个异步方法用于执行语言模型的对话任务。
    async def _execute_llm(
        self, input: CompletionInput, **kwargs: Unpack[LLMInput]
    ) -> CompletionOutput | None:
        # 准备参数
        args = get_completion_llm_args(
            kwargs.get("model_parameters"), self.configuration
        )
        # 获取历史对话记录
        history = kwargs.get("history") or []
        # 添加当前用户输入到对话历史中
        messages = [
            *history,
            {"role": "user", "content": input},
        ]
        # 使用OpenAI客户端发送对话请求
        completion = await self.client.chat.completions.create(
            messages=messages, **args
        )
        # 返回模型的回复内容
        return completion.choices[0].message.content

    # 这个异步方法用于生成JSON格式的输出。
    async def _invoke_json(
        self,
        input: CompletionInput,
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[CompletionOutput]:
        # 获取函数名和验证响应是否有效的函数
        name = kwargs.get("name") or "unknown"
        is_response_valid = kwargs.get("is_response_valid") or (lambda _x: True)

        # 定义一个内部异步函数，用于生成JSON输出
        async def generate(
            attempt: int | None = None,
        ) -> LLMOutput[CompletionOutput]:
            # ...
            pass  # 省略了具体实现，因为比较复杂

        # 检查并尝试生成有效JSON，如果尝试多次仍无效则抛出错误
        # ...
        pass  # 省略了具体实现，因为比较复杂

    # 这个异步方法使用模型内置的JSON输出支持来生成JSON。
    async def _native_json(
        self, input: CompletionInput, **kwargs: Unpack[LLMInput]
    ) -> LLMOutput[CompletionOutput]:
        # ...
        pass  # 省略了具体实现，因为比较复杂

    # 如果模型不支持内置JSON输出，这个异步方法尝试手动清理输出并解析为JSON。
    async def _manual_json(
        self, input: CompletionInput, **kwargs: Unpack[LLMInput]
    ) -> LLMOutput[CompletionOutput]:
        # ...
        pass  # 省略了具体实现，因为比较复杂

    # 当手动清理JSON失败时，这个异步方法尝试使用LLM重新格式化输出。
    async def _try_clean_json_with_llm(
        self, output: str, **kwargs: Unpack[LLMInput]
    ) -> LLMOutput[CompletionOutput]:
        # ...
        pass  # 省略了具体实现，因为比较复杂

