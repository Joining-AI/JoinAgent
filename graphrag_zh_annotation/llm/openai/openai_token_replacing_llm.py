# 导入一些特殊类型的定义，让Python知道数据的结构
from typing_extensions import Unpack
# 导入特定的类和类型定义，这些是关于语言模型的
from graphrag.llm.types import LLM, CompletionInput, CompletionLLM, CompletionOutput, LLMInput, LLMOutput
# 导入一个辅助函数，用于替换变量
from .utils import perform_variable_replacements

# 这个是微软公司的版权信息，表示代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation. Licensed under the MIT License

# 定义一个聊天式语言模型的类
class OpenAITokenReplacingLLM(LLM[CompletionInput, CompletionOutput]):
    # 类里有一个内部变量，它是一个CompletionLLM类型的对象
    _delegate: CompletionLLM

    # 初始化方法，当创建这个类的对象时会调用
    def __init__(self, delegate: CompletionLLM):
        # 把传入的CompletionLLM对象赋值给内部变量
        self._delegate = delegate

    # 这个方法是调用语言模型的核心功能
    async def __call__(
        self,
        # 输入数据是CompletionInput类型
        input: CompletionInput,
        # 其他参数可以是任意类型，用Unpack标记来展开它们
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[CompletionOutput]:
        # 获取kwargs中的"variables"和"history"，如果没有"history"就设为空列表
        variables = kwargs.get("variables")
        history = kwargs.get("history") or []
        # 使用辅助函数替换输入数据中的变量
        input = perform_variable_replacements(input, history, variables)
        # 调用内部的CompletionLLM对象来处理输入数据，并返回结果
        return await self._delegate(input, **kwargs)

