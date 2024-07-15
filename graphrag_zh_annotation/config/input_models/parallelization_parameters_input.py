# 导入一个叫做NotRequired和TypedDict的工具，它们来自typing_extensions库
from typing_extensions import NotRequired, TypedDict

# 这一段是代码的版权信息，表示这个代码是微软公司2024年的，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这里写了一个文档字符串，简单说明了下面的代码是关于LLM（可能是指语言模型）参数的模型
"""LLM Parameters model."""

# 使用TypDict创建一个新的类，叫做ParallelizationParametersInput
class ParallelizationParametersInput(TypedDict):
    # 这个类也是一个字典，用来存储特定的参数
    # 这里定义了一个键名为'stager'的参数，它的值可以是浮点数、字符串或者None，但不是必须提供的
    stagger: NotRequired[float | str | None]
    # 定义了另一个键名为'num_threads'的参数，它的值可以是整数、字符串或者None，同样不是必须提供的
    num_threads: NotRequired[int | str | None]

