# 导入一些特殊的Python库，它们帮助我们定义类型
from typing_extensions import Unpack
from graphrag.llm.base import BaseLLM
from graphrag.llm.types import (
    CompletionInput,  # 用于表示对话输入的数据结构
    CompletionOutput,  # 用于表示对话输出的数据结构
    LLMInput,  # 通用的LLM（语言模型）输入数据结构
    LLMOutput,  # 通用的LLM输出数据结构
)

# 这是微软公司的版权信息，它告诉我们代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模拟聊天LLM（语言模型），它会返回预先设定的回答

# 再次导入Unpack，确保类型正确
from typing_extensions import Unpack

# 从graphrag.llm.base导入基础的LLM类
from graphrag.llm.base import BaseLLM
# 从graphrag.llm.types导入需要的数据结构

# 创建一个名为MockChatLLM的类，它继承自BaseLLM
class MockChatLLM(
    BaseLLM[  # 告诉Python这个类是基于特定输入和输出类型的BaseLLM
        CompletionInput,  # 输入类型
        CompletionOutput,  # 输出类型
    ]
):
    # 这个模拟的LLM会返回预设的回答
    # 类的属性：存储回答列表
    responses: list[str]
    # 类的属性：记录当前返回到哪个回答了
    i: int = 0

    # 初始化方法，当我们创建MockChatLLM对象时调用
    def __init__(self, responses: list[str]):
        # 设置初始索引为0
        self.i = 0
        # 把传入的回答列表保存起来
        self.responses = responses

    # 创建输出的方法，根据输入和额外参数生成LLMOutput
    def _create_output(
        self,
        output: CompletionOutput | None,  # 可能有的输出结果
        **kwargs: Unpack[LLMInput],  # 其他任意键值对参数，类型为LLMInput
    ) -> LLMOutput[CompletionOutput]:
        # 获取历史记录（对话历史）
        history = kwargs.get("history") or []
        # 创建新的LLMOutput，包含输出结果和更新的历史记录
        return LLMOutput[CompletionOutput](
            output=output, history=[*history, {"content": output}]
        )

    # 模拟执行LLM的方法，接收输入并返回输出
    async def _execute_llm(
        self,
        input: CompletionInput,  # 输入数据
        **kwargs: Unpack[LLMInput],  # 其他任意键值对参数，类型为LLMInput
    ) -> CompletionOutput:
        # 检查是否还有剩余的回答
        if self.i >= len(self.responses):
            # 如果没有了，抛出一个错误
            msg = f"No more responses, requested {self.i} but only have {len(self.responses)}"
            raise ValueError(msg)
        # 获取下一个回答
        response = self.responses[self.i]
        # 更新回答索引
        self.i += 1
        # 返回回答
        return response

