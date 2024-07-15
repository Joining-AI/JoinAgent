# 导入一些有用的工具包，让我们的代码能执行特殊任务
from collections.abc import Awaitable, Callable  # 引入可以等待的任务和可调用对象的定义
from dataclasses import dataclass  # 引入数据类的定义，用于创建简单的类
from typing import Any  # 引入类型注释中的“任何”类型

from datashaper import VerbCallbacks  # 引入数据操作的回调函数
from graphrag.index.cache import PipelineCache  # 引入缓存管道的类

# 这是微软公司的版权信息，表示代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含两个模型：'ResolvedEntity' 和 'EntityResolutionResult'

# 再次导入一些相同的工具包，确保它们在代码中可用
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

# 定义一个字典，键是字符串，值可以是任何类型
StrategyConfig = dict[str, Any]

# 使用数据类创建一个类，用来保存实体摘要的结果
@dataclass
class SummarizedDescriptionResult:
    """这是一个描述实体摘要结果的类。"""

    # 类中的属性，可以是单个字符串或字符串元组
    items: str | tuple[str, str]
    # 描述实体的字符串
    description: str

# 定义一个函数类型，这个函数会获取一些输入并返回一个等待的任务，该任务的结果是SummarizedDescriptionResult类型的
SummarizationStrategy = Callable[
    # 函数的参数列表：
    [
        str | tuple[str, str],  # 输入的项目，可以是字符串或字符串对
        list[str],  # 一个字符串列表
        VerbCallbacks,  # 数据操作的回调函数
        PipelineCache,  # 缓存管道对象
        StrategyConfig,  # 战略配置字典
    ],
    # 函数返回值是一个等待的任务，任务结果是SummarizedDescriptionResult
    Awaitable[SummarizedDescriptionResult],
]

