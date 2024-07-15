# 导入logging模块，它用来记录程序运行时的信息
import logging

# 导入Enum类，这是一个用于创建枚举类型的类
from enum import Enum

# 导入Random类，用于生成随机数
from random import Random

# 导入Any和cast类型提示，它们是Python的类型检查工具
from typing import Any, cast

# 导入networkx库，它用于创建、操作和研究复杂网络的结构、动态和功能
import networkx as nx

# 导入pandas库，它用于数据处理和分析
import pandas as pd

# 导入datashaper库中的几个组件，用于数据操作
from datashaper import TableContainer, VerbCallbacks, VerbInput, progress_iterable, verb

# 从graphrag.index.utils导入两个函数，gen_uuid生成唯一标识符，load_graph加载图形数据
from graphrag.index.utils import gen_uuid, load_graph

# 从当前模块的typing子模块导入Communities类型定义
from .typing import Communities

# 这一行是版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含了cluster_graph、apply_clustering和run_layout方法的定义
"""

# 创建一个日志器，用于记录程序运行过程中的信息
log = logging.getLogger(__name__)

# 使用装饰器@verb，定义一个名为"cluster_graph"的方法（函数）
@verb(name="cluster_graph")

# 定义一个函数叫做cluster_graph，它接受几个参数
def cluster_graph(
    input: VerbInput,  # 输入的数据，类型是VerbInput
    callbacks: VerbCallbacks,  # 回调函数，用于显示进度条
    strategy: dict[str, Any],  # 策略字典，定义如何分组图形
    column: str,  # 图形数据所在的列名
    to: str,  # 输出分组后图形的新列名
    level_to: str | None = None,  # 输出层次信息的列名，默认为None
    **_kwargs,  # 其他任意关键字参数，这里不使用
) -> TableContainer:  # 函数返回一个TableContainer对象

    """
    这个函数用来对图形进行层次聚类。输入的图应该是graphml格式的。函数会生成新的列，包含分组后的图和图的层次信息。

    使用示例：

# 待办事项：这个函数应该支持字符串或nx.Graph作为graphml参数
def apply_clustering(
    graphml: str, communities: Communities, level=0, seed=0xF001
) -> nx.Graph:
    """将聚类应用到一个图的graphml字符串上."""
    # 创建一个随机数生成器，用给定的种子初始化（S311忽略）
    random = Random(seed)  # noqa S311
    # 解析graphml字符串，得到图
    graph = nx.parse_graphml(graphml)

    # 遍历社区信息（层次、社区ID和节点列表）
    for community_level, community_id, nodes in communities:
        # 如果当前层次等于要处理的层次
        if level == community_level:
            # 给属于该层次社区的每个节点分配社区ID和层次信息
            for node in nodes:
                graph.nodes[node]["cluster"] = community_id
                graph.nodes[node]["level"] = level

    # 添加节点度数信息
    for node_degree in graph.degree:
        # 将节点的度数转换为整数并保存
        graph.nodes[str(node_degree[0])]["degree"] = int(node_degree[1])

    # 为每个节点添加唯一的人类可读ID（用于报告中的引用）和UUID
    for index, node in enumerate(graph.nodes()):
        graph.nodes[node]["human_readable_id"] = index
        graph.nodes[node]["id"] = str(gen_uuid(random))  # 生成UUID字符串

    # 为每条边添加ID，人类可读ID和层次信息
    for index, edge in enumerate(graph.edges()):
        graph.edges[edge]["id"] = str(gen_uuid(random))  # 生成UUID字符串
        graph.edges[edge]["human_readable_id"] = index
        graph.edges[edge]["level"] = level

    # 返回处理后的图
    return graph


# 定义一个枚举类，表示图社区策略类型
class GraphCommunityStrategyType(str, Enum):
    """GraphCommunityStrategyType类定义."""

    leiden = "leiden"  # 例如，Leiden算法

    def __repr__(self):
        """返回字符串表示形式."""
        # 返回带引号的枚举值
        return f'"{self.value}"'

# 定义一个名为run_layout的函数，接收两个参数：一个字典strategy和一个字符串或网络图graphml_or_graph
def run_layout(
    strategy: dict[str, Any], graphml_or_graph: str | nx.Graph
) -> Communities:
    """这个函数用来运行布局方法。"""

    # 加载输入的图数据，可以是graphml格式的字符串或直接是网络图对象
    graph = load_graph(graphml_or_graph)

    # 检查图中是否有节点，如果没有，打印警告信息并返回空列表
    if len(graph.nodes) == 0:
        log.warning("图中没有节点")
        return []

    # 初始化一个空字典，用于存储聚类结果
    clusters: dict[int, dict[str, list[str]]] = {}

    # 获取策略类型，默认为leiden
    strategy_type = strategy.get("type", GraphCommunityStrategyType.leiden)

    # 根据策略类型执行不同的聚类方法
    match strategy_type:
        case GraphCommunityStrategyType.leiden:  # 如果策略是leiden
            # 从.strategies.leiden模块导入run_leiden函数
            from .strategies.leiden import run as run_leiden

            # 运行leiden算法并把结果存入clusters字典
            clusters = run_leiden(graph, strategy)
        case _:  # 其他未知策略
            # 构造错误信息，因为策略类型未知
            msg = f"未知的聚类策略 {strategy_type}"
            # 抛出一个值错误
            raise ValueError(msg)

    # 初始化一个空列表，用于存储最终的聚类结果
    results: Communities = []

    # 遍历clusters字典中的每个级别（level）
    for level in clusters:
        # 再遍历该级别下的每个聚类（cluster_id）及其包含的节点（nodes）
        for cluster_id, nodes in clusters[level].items():
            # 将级别、聚类ID和节点列表打包成一个元组，并添加到结果列表中
            results.append((level, cluster_id, nodes))

    # 返回所有的聚类结果
    return results

