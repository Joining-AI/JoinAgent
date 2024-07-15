# 导入一些必要的库，让程序能处理不同类型的数据和任务
from collections.abc import Awaitable, Callable  # 引入可以等待的异步操作和可调用对象的抽象基类
from dataclasses import dataclass  # 引入数据类，用于创建简单的类
from typing import Any  # 引入 Any 类型，表示可以是任何类型

from datashaper import VerbCallbacks  # 引入数据操作的回调函数
from graphrag.index.cache import PipelineCache  # 引入缓存管道的类

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了 'Document' 和 'EntityExtractionResult' 两个模型的定义

# 定义一个字典，键是字符串，值可以是任何类型
ExtractedEntity = dict[str, Any]
# 定义一个字典，键是字符串，值也是任意类型
StrategyConfig = dict[str, Any]
# 定义一个字符串列表
EntityTypes = list[str]

# 使用数据类定义一个名为 'Document' 的类，它有两个属性：文本（text）和唯一标识符（id）
@dataclass
class Document:
    """文档类的定义，包含文本和ID。"""
    text: str  # 文档的文本内容
    id: str  # 文档的唯一标识

# 使用数据类定义一个名为 'EntityExtractionResult' 的类，它有两个属性：实体列表（entities）和可能的图ML图形（graphml_graph）
@dataclass
class EntityExtractionResult:
    """实体提取结果类的定义，包含提取出的实体列表和可能的图形数据。"""
    entities: list[ExtractedEntity]  # 提取出的实体，每个实体是一个字典
    graphml_graph: str | None  # 图ML格式的图形数据，或者可能是None

# 定义一个函数类型，这个函数接受多个参数，返回一个可以等待的结果（EntityExtractionResult）
EntityExtractStrategy = Callable[
    [
        list[Document],  # 文档列表
        EntityTypes,  # 实体类型列表
        VerbCallbacks,  # 数据操作的回调函数
        PipelineCache,  # 缓存管道
        StrategyConfig,  # 策略配置
    ],
    Awaitable[EntityExtractionResult],  # 返回的结果是一个可以等待的实体提取结果
]

