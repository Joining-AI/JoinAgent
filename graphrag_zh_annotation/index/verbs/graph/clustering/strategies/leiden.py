# 导入logging模块，用于输出日志信息
import logging

# 导入typing模块，提供类型提示功能
from typing import Any

# 导入networkx库，用于处理图数据
import networkx as nx

# 导入hierarchical_leiden函数，用于社区划分
from graspologic.partition import hierarchical_leiden

# 导入稳定最大连通分量函数，用于处理图的连通性
from graphrag.index.graph.utils import stable_largest_connected_component

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含run和_compute_leiden_communities方法的定义

# 获取当前模块的日志记录器
log = logging.getLogger(__name__)

# 定义run方法
def run(graph: nx.Graph, args: dict[str, Any]) -> dict[int, dict[str, list[str]]]:
    # 从参数字典中获取最大社区大小，默认值为10
    max_cluster_size = args.get("max_cluster_size", 10)
    # 获取是否使用最大连通分量，默认值为True
    use_lcc = args.get("use_lcc", True)
    
    # 如果设置为输出详细信息，打印当前的参数设置
    if args.get("verbose", False):
        log.info("正在运行leiden算法，最大社区大小=%s，使用LCC=%s", max_cluster_size, use_lcc)

    # 计算节点到社区的映射
    node_id_to_community_map = _compute_leiden_communities(
        graph=graph,
        max_cluster_size=max_cluster_size,
        use_lcc=use_lcc,
        seed=args.get("seed", 0xDEADBEEF),  # 设置随机种子，默认值为0xDEADBEEF
    )

    # 获取指定的层级列表，如果没有指定则使用所有层级
    levels = args.get("levels")
    if levels is None:
        levels = sorted(node_id_to_community_map.keys())  # 如果未指定，排序并使用所有层级

    # 初始化结果字典，以层级为键，社区信息为值
    results_by_level: dict[int, dict[str, list[str]]] = {}
    for level in levels:
        # 初始化当前层级的结果字典
        result = {}
        results_by_level[level] = result
        # 遍历当前层级的节点和社区
        for node_id, raw_community_id in node_id_to_community_map[level].items():
            # 将原始社区ID转换为字符串
            community_id = str(raw_community_id)
            # 如果当前社区不在结果中，创建一个新的空列表
            if community_id not in result:
                result[community_id] = []
            # 将节点ID添加到对应社区的列表中
            result[community_id].append(node_id)

    # 返回结果字典
    return results_by_level

# 定义一个名为_compute_leiden_communities的函数，它接受四个参数：
# graph：一个图（可以是无向或有向的），用nx.Graph或nx.DiGraph表示
# max_cluster_size：最大的聚类大小
# use_lcc：一个布尔值，决定是否使用最大的稳定连通分量
# seed：随机数种子，用于可重复性，默认值为0xDEADBEEF（一个常用于示例的十六进制数）

# 如果use_lcc为真（True），则找到图中的最大稳定连通分量，并将图替换为此分量
def _compute_leiden_communities(
    graph: nx.Graph | nx.DiGraph,
    max_cluster_size: int,
    use_lcc: bool,
    seed=0xDEADBEEF,
) -> dict[int, dict[str, int]]:
    if use_lcc:
        # stable_largest_connected_component函数会返回一个只包含最大连通部分的图
        graph = stable_largest_connected_component(graph)

    # 使用hierarchical_leiden函数对图进行分层Leiden聚类，设置最大聚类大小和随机种子
    community_mapping = hierarchical_leiden(
        graph, max_cluster_size=max_cluster_size, random_seed=seed
    )

    # 初始化一个空字典，用于存储结果
    results: dict[int, dict[str, int]] = {}

    # 遍历每个聚类（partition）
    for partition in community_mapping:
        # 每个聚类都有一个级别（level）和一些节点（node）
        # 将聚类级别作为键，如果该级别不存在则创建一个新的字典
        results[partition.level] = results.get(partition.level, {})

        # 节点的名称作为键，聚类编号作为值，存入对应级别的字典中
        results[partition.level][partition.node] = partition.cluster

    # 返回结果字典
    return results

