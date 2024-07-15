# 这段代码是创建一个用于聊天的语言模型。让我们一行一行地理解它：

# 导入一些特殊类型的定义，帮助我们更好地了解代码中的变量类型
from typing_extensions import Unpack
# 导入特定的类型定义，这些定义与语言模型有关
from graphrag.llm.types import (
    LLM,  # 一个通用的语言模型接口
    CompletionInput,  # 完成输入的数据结构
    CompletionLLM,  # 特定类型的完成语言模型
    CompletionOutput,  # 完成输出的数据结构
    LLMInput,  # 语言模型的一般输入数据结构
    LLMOutput,  # 语言模型的一般输出数据结构
)

# 代码版权信息，说明这是微软公司的作品，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个聊天式语言模型的描述
"""The Chat-based language model."""

# 再次导入Unpack，确保在后续代码中可以使用
from typing_extensions import Unpack

# 继续从graphrag.llm.types导入类型定义
from graphrag.llm.types import ...

# 定义一个名为OpenAIHistoryTrackingLLM的类，它是一个特殊的语言模型，能跟踪对话历史
class OpenAIHistoryTrackingLLM(LLM[CompletionInput, CompletionOutput]):
    # 这个类内部会用到一个名为Delegate的完成语言模型
    _delegate: CompletionLLM

    # 初始化方法，当我们创建这个类的对象时会调用
    def __init__(self, delegate: CompletionLLM):
        # 把传入的完成语言模型赋值给内部的_delegate属性
        self._delegate = delegate

    # 这个方法是调用语言模型的核心部分
    async def __call__(
        self,
        input: CompletionInput,  # 输入数据
        **kwargs: Unpack[LLMInput],  # 其他可能的参数，以关键字参数形式传递
    ) -> LLMOutput[CompletionOutput]:
        # 描述：调用语言模型
        """Call the LLM."""
        
        # 从kwargs中获取历史记录，如果没有就用空列表代替
        history = kwargs.get("history") or []

        # 使用_delegate（即我们传入的完成语言模型）处理输入数据
        output = await self._delegate(input, **kwargs)

        # 创建一个新的输出数据结构，包含原始输出、JSON数据和新的系统响应（即模型的输出）
        return LLMOutput(
            output=output.output,
            json=output.json,
            history=[*history, {"role": "system", "content": output.output}],
        )

