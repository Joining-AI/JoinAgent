# 导入logging模块，它用于在程序中记录信息和错误
import logging

# 导入Enum类，它是Python内置的枚举类型，用于创建枚举对象
from enum import Enum

# 导入typing模块中的Any和cast，它们帮助我们更好地定义和理解函数参数的类型
from typing import Any, cast

# 导入pandas库，它用于处理表格数据
import pandas as pd

# 导入datashaper库的一些组件，用于数据操作
from datashaper import (
    AsyncType,  # 异步类型
    TableContainer,  # 表格容器
    VerbCallbacks,  # 用于处理命令的回调函数
    VerbInput,  # 命令输入
    derive_from_rows,  # 从行数据派生新数据
    verb,  # 定义命令的装饰器
)

# 导入graphrag库的索引初始化和缓存部分
from graphrag.index.bootstrap import bootstrap
from graphrag.index.cache import PipelineCache

# 导入本项目的策略类型定义
from .strategies.typing import Document, EntityExtractStrategy

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了提取实体的方法
"""

# 初始化日志记录器，用于记录程序运行时的信息
log = logging.getLogger(__name__)

# 定义一个枚举类，表示不同的实体提取策略
class ExtractEntityStrategyType(str, Enum):
    # 枚举成员，表示使用图智能进行提取
    graph_intelligence = "graph_intelligence"
    # 使用图智能的JSON格式进行提取
    graph_intelligence_json = "graph_intelligence_json"
    # 使用nltk库进行提取
    nltk = "nltk"

    # 自定义字符串表示方法
    def __repr__(self):
        # 返回带有引号的策略类型值
        return f'"{self.value}"'

# 默认的实体类型列表
DEFAULT_ENTITY_TYPES = ["organization", "person", "geo", "event"]

# 使用verb装饰器定义一个名为"entity_extract"的命令
@verb(name="entity_extract")

# 定义一个异步函数，叫做entity_extract，它需要一些参数
async def entity_extract(
    # 输入的数据，类型是VerbInput
    input: VerbInput,
    # 管道缓存，类型是PipelineCache
    cache: PipelineCache,
    # 回调函数集合，类型是VerbCallbacks
    callbacks: VerbCallbacks,
    # 要从中提取实体的列名
    column: str,
    # 表中每一行的唯一ID列名
    id_column: str,
    # 输出实体到的列名
    to: str,
    # 提取策略，可以是字典或None
    strategy: dict[str, Any] | None,
    # 输出图到的列名，可选，可能是None
    graph_to: str | None = None,
    # 异步模式，默认使用AsyncIO
    async_mode: AsyncType = AsyncType.AsyncIO,
    # 要提取的实体类型，默认是一些预定义类型
    entity_types=DEFAULT_ENTITY_TYPES,
    **kwargs,  # 其他可能的参数
) -> TableContainer:
    """
    这个函数从文本中提取实体。

    使用方法：
    JSON格式示例：
    YAML格式示例：

    提取策略：
    1. graph_intelligence：使用特定库和LLM（大型语言模型）来提取。
    2. nltk：使用nltk库来提取。

    """
    # 打印调试信息，显示使用的策略
    log.debug("entity_extract strategy=%s", strategy)
    
    # 如果没有指定实体类型，就用默认值
    if entity_types is None:
        entity_types = DEFAULT_ENTITY_TYPES

    # 获取输入数据并转换成DataFrame
    output = cast(pd.DataFrame, input.get_input())

    # 策略可能是None，这里处理一下
    strategy = strategy or {}
    # 加载指定类型的提取策略
    strategy_exec = _load_strategy(
        strategy.get("type", ExtractEntityStrategyType.graph_intelligence)
    )
    # 复制策略配置
    strategy_config = {**strategy}

    # 记录开始运行的数量
    num_started = 0

    # 定义一个异步函数，用于运行策略
    async def run_strategy(row):
        nonlocal num_started  # 更新外部变量
        # 获取当前行的文本和ID
        text = row[column]
        id = row[id_column]
        # 使用策略执行函数处理数据
        result = await strategy_exec(
            [Document(text=text, id=id)],
            entity_types,
            callbacks,
            cache,
            strategy_config,
        )
        # 增加已开始计数
        num_started += 1
        # 返回结果中的实体和图
        return [result.entities, result.graphml_graph]

    # 对DataFrame的每一行运行run_strategy函数
    results = await derive_from_rows(
        output,
        run_strategy,
        callbacks,
        # 指定异步模式
        scheduling_type=async_mode,
        # 指定并发线程数量
        num_threads=kwargs.get("num_threads", 4),
    )

    # 初始化结果列表
    to_result = []
    graph_to_result = []

    # 将结果放入对应列表
    for result in results:
        if result:
            to_result.append(result[0])
            graph_to_result.append(result[1])
        else:
            to_result.append(None)
            graph_to_result.append(None)

    # 将提取的实体添加到output DataFrame的'to'列
    output[to] = to_result
    # 如果有graph_to，将图添加到对应的列
    if graph_to is not None:
        output[graph_to] = graph_to_result

    # 返回一个新的TableContainer对象
    return TableContainer(table=output.reset_index(drop=True))

# 定义一个函数，名为_load_strategy，它接受一个参数：strategy_type，类型是ExtractEntityStrategyType
def _load_strategy(strategy_type: ExtractEntityStrategyType) -> EntityExtractStrategy:
    """这个函数用来加载策略方法的定义。"""
    
    # 使用Python的match-case结构，根据strategy_type的值来执行不同的代码块
    match strategy_type:
        # 如果strategy_type等于ExtractEntityStrategyType.graph_intelligence
        case ExtractEntityStrategyType.graph_intelligence:
            # 从.strategies.graph_intelligence模块导入run_gi函数
            from .strategies.graph_intelligence import run_gi
            
            # 返回run_gi函数
            return run_gi
            
        # 如果strategy_type等于ExtractEntityStrategyType.nltk
        case ExtractEntityStrategyType.nltk:
            # 首先调用bootstrap()函数（可能用于初始化）
            bootstrap()
            
            # 动态导入nltk策略模块，避免如果没有使用就引入依赖
            from .strategies.nltk import run as run_nltk
            
            # 返回run_nltk函数
            return run_nltk
            
        # 如果以上都不匹配，即strategy_type是其他未知值
        case _:
            # 创建一个错误信息，包含未知的strategy_type
            msg = f"未知的策略：{strategy_type}"
            
            # 抛出一个ValueError，附带错误信息
            raise ValueError(msg)

