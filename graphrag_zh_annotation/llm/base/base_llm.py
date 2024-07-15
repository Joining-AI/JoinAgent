# 导入一些工具，帮助我们创建和管理类和类型
import traceback  # 用于捕获和打印错误信息
from abc import ABC, abstractmethod  # 创建抽象基类的工具
from typing import Generic, TypeVar  # 处理泛型类型的工具
from typing_extensions import Unpack  # 帮助解包字典参数

# 导入自定义的类型定义
from graphrag.llm.types import (
    LLM,
    ErrorHandlerFn,
    LLMInput,
    LLMOutput,
)

# 版本控制信息，表示这个代码的版权和许可
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义基类 LLM 的文档字符串
"""基础的 LLM 类定义。"""

# 定义两个类型变量，代表输入和输出的任意类型
TIn = TypeVar("TIn")
TOut = TypeVar("TOut")

# 创建一个抽象基类 BaseLLM，它同时继承了 ABC（抽象基类）和 LLM
# 并且是泛型类，可以处理 TIn 和 TOut 类型
class BaseLLM(ABC, LLM[TIn, TOut], Generic[TIn, TOut]):
    # 错误处理器函数的存储变量，可能为 None
    _on_error: ErrorHandlerFn | None

    # 设置错误处理器函数的方法
    def on_error(self, on_error: ErrorHandlerFn | None) -> None:
        # 将传入的错误处理器函数赋值给 _on_error
        self._on_error = on_error

    # 一个必须在子类中实现的抽象方法，执行 LLM 的核心逻辑
    @abstractmethod
    async def _execute_llm(
        self,
        input: TIn,
        **kwargs: Unpack[LLMInput],
    ) -> TOut | None:
        # 子类需要在这里实现具体的 LLM 执行逻辑
        pass

    # 调用 LLM 的主要方法
    async def __call__(
        self,
        input: TIn,
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[TOut]:
        # 判断是否需要 JSON 格式的输出
        is_json = kwargs.get("json") or False
        # 如果需要 JSON 格式，调用 _invoke_json 方法
        if is_json:
            return await self._invoke_json(input, **kwargs)
        # 否则，调用 _invoke 方法
        return await self._invoke(input, **kwargs)

    # 实现 LLM 的普通调用逻辑
    async def _invoke(self, input: TIn, **kwargs: Unpack[LLMInput]) -> LLMOutput[TOut]:
        try:
            # 执行 LLM 的核心逻辑，并获取输出
            output = await self._execute_llm(input, **kwargs)
            # 包装输出结果为 LLMOutput 对象返回
            return LLMOutput(output=output)
        except Exception as e:
            # 捕获并打印异常的堆栈跟踪信息
            stack_trace = traceback.format_exc()
            # 如果设置了错误处理器，调用它处理异常
            if self._on_error:
                self._on_error(e, stack_trace, {"input": input})
            # 抛出异常，中断程序
            raise

    # 实现 LLM 的 JSON 输出逻辑，但这里抛出一个错误，因为这个 LLM 不支持 JSON 输出
    async def _invoke_json(
        self, input: TIn, **kwargs: Unpack[LLMInput]
    ) -> LLMOutput[TOut]:
        msg = "JSON output not supported by this LLM"
        raise NotImplementedError(msg)

