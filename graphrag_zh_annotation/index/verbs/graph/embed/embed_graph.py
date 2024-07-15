# 导入Enum模块，用于创建枚举类型
from enum import Enum

# 导入typing模块，用于类型注解
from typing import Any, cast

# 导入networkx库，用于处理图数据
import networkx as nx

# 导入pandas库，用于数据处理和分析
import pandas as pd

# 导入datashaper库中的几个类，用于数据操作
from datashaper import TableContainer, VerbCallbacks, VerbInput, derive_from_rows, verb

# 导入graphrag.index.utils模块中的load_graph函数
from graphrag.index.utils import load_graph

# 导入自定义的NodeEmbeddings类型
from .typing import NodeEmbeddings

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了embed_graph和run_embeddings方法的定义

# 定义一个枚举类 EmbedGraphStrategyType，表示图嵌入策略类型
class EmbedGraphStrategyType(str, Enum):
    # 枚举值：node2vec，表示使用node2vec算法进行图嵌入
    node2vec = "node2vec"

    # 当打印或显示枚举实例时，返回一个字符串表示
    def __repr__(self):
        # 返回带引号的枚举值字符串
        return f'"{self.value}"'

# 使用verb装饰器定义一个名为"embed_graph"的操作
@verb(name="embed_graph")

# 这是一个Python函数，用于将图嵌入到一个向量空间中。图应该是graphml格式的。
# 函数会创建一个新的列，其中包含节点ID和它们对应的向量映射。

# 定义一个异步函数（async function），名字叫embed_graph，接收多个参数：
# - input：输入的数据
# - callbacks：回调函数，用于处理函数运行过程中的事件
# - strategy：一个字典，定义了嵌入图的方法
# - column：包含图数据的列的名字
# - to：新生成的包含嵌入向量的列的名字
# - **kwargs：其他任意数量的键值对参数

async def embed_graph(
    input: VerbInput,
    callbacks: VerbCallbacks,
    strategy: dict[str, Any],
    column: str,
    to: str,
    **kwargs,
) -> TableContainer:
    """
    # 这个函数的用途是把图变成向量。
    
    在YAML格式的配置文件里这样用：

# 定义一个名为run_embeddings的函数，它接受三个参数：策略（strategy），可以是图的描述或图本身（graphml_or_graph），以及一个字典（args）
def run_embeddings(
    strategy: EmbedGraphStrategyType,  # 策略类型，用于决定如何处理图
    graphml_or_graph: str | nx.Graph,  # 图的数据，可能是字符串（可能是图的文件路径）或网络x库的图对象
    args: dict[str, Any],  # 一个包含额外参数的字典
) -> NodeEmbeddings:  # 函数返回值类型，表示节点嵌入的结果

    # 加载输入的图数据
    graph = load_graph(graphml_or_graph)

    # 使用Python的匹配语句，根据strategy的值执行不同的操作
    match strategy:
        # 如果strategy的值等于'node2vec'（节点到向量的策略）
        case EmbedGraphStrategyType.node2vec:
            # 从.strategies.node_2_vec模块导入run函数
            from .strategies.node_2_vec import run as run_node_2_vec

            # 调用run_node_2_vec函数，传入图和参数字典，然后返回结果
            return run_node_2_vec(graph, args)

        # 如果strategy的值不是已知的'node2vec'
        case _:  # 这里代表所有其他情况
            # 构造一个错误消息，包含未知策略的名称
            msg = f"Unknown strategy {strategy}"
            # 抛出一个ValueError，附带错误消息
            raise ValueError(msg)

