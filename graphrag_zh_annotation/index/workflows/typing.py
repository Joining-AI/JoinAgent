# 导入Callable模块，它定义了可调用对象的接口，就像函数一样
from collections.abc import Callable

# 导入dataclass装饰器，用于简化数据类的创建
from dataclasses import dataclass as dc_dataclass

# 导入Any类型，表示任何类型的变量
from typing import Any

# 导入TableContainer和Workflow，它们是数据处理相关的类
from datashaper import TableContainer, Workflow

# 这是一个版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，里面包含'WorkflowToRun'模型
# "A module containing 'WorkflowToRun' model."

# 定义一个字典类型StepDefinition，键是字符串，值可以是任何类型
StepDefinition = dict[str, Any]

# 定义一个字典类型VerbDefinitions，键是字符串（动词名称），值是可调用对象，返回TableContainer
VerbDefinitions = dict[str, Callable[..., TableContainer]]

# 定义一个字典类型WorkflowConfig，键是字符串，值可以是任何类型
WorkflowConfig = dict[str, Any]

# 定义一个字典类型WorkflowDefinitions，键是工作流名称，值是接受配置并返回步骤定义列表的函数
WorkflowDefinitions = dict[str, Callable[[WorkflowConfig], list[StepDefinition]]]

# 定义一个字典类型VerbTiming，键是字符串（动词ID），值是浮点数（执行时间）
VerbTiming = dict[str, float]


# 使用dataclass装饰器创建一个类WorkflowToRun
@dc_dataclass
class WorkflowToRun:
    # 类的定义，包含两个属性：workflow（一个Workflow对象）和config（一个键为字符串的字典）
    workflow: Workflow  # 工作流对象
    config: dict[str, Any]  # 工作流配置

