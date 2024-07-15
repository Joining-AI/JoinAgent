# 导入异步操作库，用于处理需要等待的任务
import asyncio

# 导入日志模块，帮助记录程序运行情况
import logging

# 导入枚举类库，用于定义固定选项的类
from enum import Enum

# 导入类型提示库，帮助编写更清晰的代码
from typing import Any, NamedTuple, cast

# 导入网络图库，用于处理图形数据
import networkx as nx

# 导入数据分析库，用于处理表格数据
import pandas as pd

# 导入datashaper库中的相关组件，用于数据处理和进度显示
from datashaper import (
    ProgressTicker,  # 进度指示器
    TableContainer,  # 表格容器
    VerbCallbacks,  # 命令回调
    VerbInput,  # 命令输入
    progress_ticker,  # 进度条函数
    verb,  # 定义命令函数的装饰器
)

# 导入缓存库，用于存储中间结果
from graphrag.index.cache import PipelineCache

# 导入加载图形数据的辅助函数
from graphrag.index.utils import load_graph

# 导入自定义策略的类型
from .strategies.typing import SummarizationStrategy

# 版权声明和许可信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含“summarize_descriptions”命令

# 设置日志记录器，用于输出程序运行日志
log = logging.getLogger(__name__)

# 定义一个元组类，用于存储描述总结的数据
class DescriptionSummarizeRow(NamedTuple):
    graph: Any  # 图形数据


# 定义一个枚举类，用于选择总结策略
class SummarizeStrategyType(str, Enum):
    graph_intelligence = "graph_intelligence"  # 使用图形智能策略

    # 返回枚举值的字符串表示
    def __repr__(self):
        return f'"{self.value}"'


# 使用verb装饰器定义一个名为"summarize_descriptions"的命令函数
@verb(name="summarize_descriptions")

# 这个函数用来从实体图中总结实体和关系的描述
async def summarize_descriptions(
    输入: VerbInput,  # 输入数据
    缓存: PipelineCache,  # 管道缓存
    回调: VerbCallbacks,  # 回调函数
    列: str,  # 提取描述的列名
    输出到: str,  # 存放总结后描述的列名
    策略: dict[str, Any] | None = None,  # 可选的总结策略配置
    **kwargs,  # 其他任意参数
) -> TableContainer:  # 返回处理后的表格容器

    # 在日志中记录策略类型
    log.debug("summarize_descriptions 策略=%s", 策略)
    
    # 获取输入数据的DataFrame
    输出数据 = 输入.get_input()

    # 如果没有提供策略，则使用默认值
    策略 = 策略 or {}

    # 加载指定类型的策略执行器
    策略执行器 = load_strategy(
        策略.get("type", SummarizeStrategyType.graph_intelligence)
    )

    # 复制策略配置
    策略配置 = {**策略}

    # 定义一个异步函数，用于获取处理后的实体
    async def 获取解析实体(row, 信号量: asyncio.Semaphore):
        # 加载图数据
        图: nx.Graph = 加载图(getattr(row, 列))

        # 计算节点和边的数量
        进度条长度 = len(图.nodes) + len(图.edges)

        # 创建进度条
        进度条 = 进度条回调(callbacks.progress, 进度条长度)

        # 创建异步任务列表，用于总结每个节点和边的描述
        任务列表 = [
            做总结描述(
                节点或边,
                排序后的描述列表,
                进度条,
                信号量,
            )
            for 节点或边 in 图.nodes()
        ]
        任务列表 += [
            做总结描述(
                边,
                排序后的描述列表,
                进度条,
                信号量,
            )
            for 边 in 图.edges()
        ]

        # 并行执行任务并获取结果
        结果列表 = await asyncio.gather(*任务列表)

        # 更新图中的描述
        for 结果 in 结果列表:
            图项 = 结果.items
            if 图项是节点名称并且在图的节点中：
                图.nodes[图项]["description"] = 结果.description
            elif 图项是边并且在图的边中：
                图.edges[图项]["description"] = 结果.description

        # 返回处理后的图数据
        return DescriptionSummarizeRow(
            图="\n".join(nx.generate_graphml(图)),
        )

    # 定义一个异步函数，用于对单个节点或边进行描述的总结
    async def 做总结描述(
        图项: str | tuple[str, str],
        描述: list[str],
        进度条: ProgressTicker,
        信号量: asyncio.Semaphore,
    ):
        # 使用信号量控制并发
        async with 信号量:
            # 执行策略
            结果 = await 策略执行器(
                图项,
                描述,
                回调,
                缓存,
                策略配置,
            )
            # 更新进度条
            进度条(1)
        # 返回结果
        return 结果

    # 创建信号量，用于限制并发数量
    信号量 = asyncio.Semaphore(kwargs.get("num_threads", 4))

    # 对每一行数据并行处理
    结果列表 = [
        await 获取解析实体(row, 信号量) for row in 输出数据.itertuples()
    ]

    # 初始化输出到的列
    输出到结果 = []

    # 将处理结果添加到新列
    for 结果 in 结果列表:
        if 结果:
            输出到结果.append(结果.graph)
        else:
            输出到结果.append(None)

    # 将总结后的描述添加到输出数据的新列
    输出数据[输出到] = 输出到结果

    # 返回包含处理后数据的表格容器
    return TableContainer(table=输出数据)

# 定义一个函数，叫load_strategy，它接受一个类型为SummarizeStrategyType的参数（策略类型），并返回一个SummarizationStrategy类型的值
def load_strategy(strategy_type: SummarizeStrategyType) -> SummarizationStrategy:
    # 这个函数的目的是加载不同的策略方法
    """Load strategy method definition."""
    
    # 使用Python的match-case结构来根据strategy_type的值执行不同的代码块
    match strategy_type:
        # 如果strategy_type是SummarizeStrategyType.graph_intelligence类型
        case SummarizeStrategyType.graph_intelligence:
            # 从当前目录下的.strategies.graph_intelligence模块导入run函数，然后用别名run_gi
            from .strategies.graph_intelligence import run as run_gi
            
            # 返回run_gi这个函数
            return run_gi
        # 如果strategy_type不是上面的情况，也就是其他任何情况
        case _:
            # 创建一个消息字符串，内容为“未知的策略：”，后面跟着strategy_type的具体值
            msg = f"Unknown strategy: {strategy_type}"
            
            # 抛出一个ValueError，附带刚才创建的消息，告诉用户策略类型不被识别
            raise ValueError(msg)

