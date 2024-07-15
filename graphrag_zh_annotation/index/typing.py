# 导入Callable模块，这是一个Python接口，表示可调用的对象
from collections.abc import Callable

# 导入dataclass模块，它是Python的一个装饰器，用来简化创建具有默认值的数据类
from dataclasses import dataclass

# 导入pandas库，它用于数据处理和分析
import pandas as pd

# 这是版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含'PipelineRunResult'模型的代码
"""A module containing the 'PipelineRunResult' model."""

# 定义一个类型别名，ErrorHandlerFn，表示一个函数，接收可能的异常、字符串和字典作为参数，不返回任何值
ErrorHandlerFn = Callable[[BaseException | None, str | None, dict | None], None]

# 使用dataclass装饰器定义一个名为PipelineRunResult的类
@dataclass
class PipelineRunResult:
    # 类的初始化方法，定义了三个属性
    # workflow：存储工作流的名称，类型为字符串
    workflow: str
    
    # result：存储结果数据，类型可以是pandas的DataFrame或None
    result: pd.DataFrame | None
    
    # errors：存储在运行过程中遇到的异常列表，类型可以是BaseException类型的列表或None
    errors: list[BaseException] | None

