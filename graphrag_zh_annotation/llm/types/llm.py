# 导入一些编程工具，让我们的代码更规范
from typing import Generic, Protocol, TypeVar  # 引入类型定义的工具
from typing_extensions import Unpack  # 引入一个特殊类型的工具，用于解包

# 从我们项目的某个部分导入两个类
from .llm_io import LLMInput, LLMOutput  # 导入与输入和输出相关的类

# 这是微软公司的版权信息，表示代码的归属
# Copyright (c) 2024 Microsoft Corporation.  # 版权属于微软公司
# Licensed under the MIT License  # 使用MIT许可证授权

# 这个模块是关于LLM（可能是“语言逻辑模型”）的类型定义
"""LLM Types."""


# 定义两个类型变量，TIn和TOut，它们代表输入和输出的类型
TIn = TypeVar("TIn", contravariant=True)  # TIn是一个可逆变的输入类型
TOut = TypeVar("TOut")  # TOut是一个输出类型


# 定义一个协议类（Protocol），它像一个接口，规定了其他类需要实现的方法
class LLM(Protocol, Generic[TIn, TOut]):  # LLM协议，包含输入和输出类型
    """LLM Protocol definition."""
    # 这个类定义了一个方法，模拟调用一个函数
    async def __call__(  # 当你使用"()"来调用一个对象时，Python会执行这个方法
        self,  # 指向当前对象的引用
        input: TIn,  # 方法的输入参数，类型为TIn
        **kwargs: Unpack[LLMInput],  # 其他任意关键字参数，类型为LLMInput的解包形式
    ) -> LLMOutput[TOut]:  # 返回值类型为包含TOut的LLMOutput
        """Invoke the LLM, treating the LLM as a function."""
        # 这里省略了方法的具体实现，用"..."来表示
        ...

