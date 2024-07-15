# 导入一个叫做AsyncType的特殊类型，它用于处理异步操作
from datashaper import AsyncType

# 从typing_extensions库导入NotRequired，它表示某个参数是可选的，不一定需要提供
from typing_extensions import NotRequired, TypedDict

# 从当前目录下的llm_parameters_input模块导入LLMParametersInput类
from .llm_parameters_input import LLMParametersInput

# 从当前目录下的parallelization_parameters_input模块导入ParallelizationParametersInput类
from .parallelization_parameters_input import ParallelizationParametersInput

# 这一段是版权信息，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为LLMConfigInput的类，它继承自TypedDict
# TypedDict是一个特殊的字典，可以指定每个键的类型
class LLMConfigInput(TypedDict):
    # 这里定义了LLMConfigInput类中可以有的键和对应的类型
    # 'llm'键的类型是NotRequired[LLMParametersInput | None]，表示可以不提供，或者提供一个LLMParametersInput对象或None
    llm: NotRequired[LLMParametersInput | None]
    # 'parallelization'键的类型是NotRequired[ParallelizationParametersInput | None]，同理，也可以不提供，或者提供一个ParallelizationParametersInput对象或None
    parallelization: NotRequired[ParallelizationParametersInput | None]
    # 'async_mode'键的类型是NotRequired[AsyncType | str | None]，表示可以不提供，或者提供一个AsyncType、字符串或None
    async_mode: NotRequired[AsyncType | str | None]

