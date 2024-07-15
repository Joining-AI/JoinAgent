# 导入logging模块，用于记录程序运行时的信息
import logging

# 导入traceback模块，用来处理和打印错误堆栈信息
import traceback

# 从typing模块导入Any类型，表示可以是任何类型的变量
from typing import Any

# 导入networkx库，这是一个用于创建、操作和研究复杂网络结构的库
import networkx as nx

# 从graphrag.index.graph.visualization模块中导入一些图形布局相关的类和函数
from graphrag.index.graph.visualization import (
    GraphLayout,  # 用于定义图的布局方式
    NodePosition,  # 表示节点的位置
    get_zero_positions,  # 获取所有节点初始位置为零的函数
)

# 从graphrag.index.typing模块中导入ErrorHandlerFn，这是错误处理函数的类型定义
from graphrag.index.typing import ErrorHandlerFn

# 这是一个版权声明，表明代码由微软公司拥有，授权使用MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含run和_create_node_position两个方法的定义
# 注：这里的中文注释是为了帮助理解，实际代码中不会出现这些注释

# 为了记录与这个模块相关的信息，创建一个日志器对象
log = logging.getLogger(__name__)

# 定义一个名为run的函数，接收三个参数：一个图（graph）、一个字典（_args）和一个错误处理函数（on_error）
def run(
    graph: nx.Graph,  # 图数据结构
    _args: dict[str, Any],  # 字典，包含各种可能的参数
    on_error: ErrorHandlerFn,  # 错误处理函数
) -> GraphLayout:  # 返回值类型为GraphLayout，表示布局结果

    """这是一个运行方法的定义，用于处理图布局"""
    
    # 初始化两个空列表，用于存储节点所属的群组和节点大小
    node_clusters = []  # 群组列表
    node_sizes = []  # 节点大小列表

    # 获取图中的所有节点
    nodes = list(graph.nodes)

    # 遍历每个节点
    for node_id in nodes:
        # 获取节点信息
        node = graph.nodes[node_id]

        # 尝试获取节点所属的群组，如果不存在则用-1替代
        cluster = node.get("cluster", node.get("community", -1))

        # 将群组添加到群组列表
        node_clusters.append(cluster)

        # 尝试获取节点的度数（连接数量），如果不存在则用0替代
        size = node.get("degree", node.get("size", 0))

        # 将节点大小添加到大小列表
        node_sizes.append(size)

    # 创建一个额外的参数字典，用于传递给其他函数
    additional_args = {}

    # 如果有群组信息，将其作为“node_categories”参数加入字典
    if len(node_clusters) > 0:
        additional_args["node_categories"] = node_clusters

    # 如果有节点大小信息，将其作为“node_sizes”参数加入字典
    if len(node_sizes) > 0:
        additional_args["node_sizes"] = node_sizes

    # 尝试获取节点的初始位置，传入节点标签和额外参数
    try:
        return get_zero_positions(node_labels=nodes, **additional_args)
    # 如果出现异常，记录错误并调用错误处理函数
    except Exception as e:
        log.exception("Error running zero-position")  # 记录错误日志
        on_error(e, traceback.format_exc(), None)  # 调用错误处理函数

        # 如果umap布局失败，可能是输入数据稀疏或内存压力大，返回所有节点在(0, 0)的位置
        result = []
        for i in range(len(nodes)):
            # 如果有群组信息，使用它；否则默认为1
            cluster = node_clusters[i] if len(node_clusters) > 0 else 1
            # 创建一个NodePosition对象，表示节点位置
            result.append(
                NodePosition(x=0, y=0, label=nodes[i], size=0, cluster=str(cluster))
            )
        # 返回节点位置列表
        return result

