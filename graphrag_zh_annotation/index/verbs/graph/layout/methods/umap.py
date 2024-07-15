# 导入logging模块，用于记录程序运行中的信息和错误
import logging

# 导入traceback模块，当程序出错时，它能帮助我们追踪错误来源
import traceback

# 从typing模块导入Any类型，它代表任何类型的值
from typing import Any

# 导入networkx库，这是一个用来创建、操作和研究复杂网络结构的库
import networkx as nx

# 导入numpy库，它是Python中用于科学计算的核心库，处理数组和矩阵
import numpy as np

# 从graphrag的可视化部分导入几个类：GraphLayout（图形布局），NodePosition（节点位置）和compute_umap_positions（计算UMAP位置）
from graphrag.index.graph.visualization import (
    GraphLayout,
    NodePosition,
    compute_umap_positions,
)

# 从graphrag的类型定义部分导入ErrorHandlerFn（错误处理器函数类型）
from graphrag.index.typing import ErrorHandlerFn

# 从graphrag的嵌入部分的类型定义导入NodeEmbeddings（节点嵌入类型）
from graphrag.index.verbs.graph.embed.typing import NodeEmbeddings

# 这段文字是版权信息，说明代码由微软公司拥有，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了run和_create_node_position两个方法的定义
# 注意：这部分是模块的描述，不是实际的代码

# 再次导入logging，创建一个名为__name__的日志器（logger）。这样我们可以记录这个特定模块的日志信息
log = logging.getLogger(__name__)

# 定义一个名为run的函数，它接受四个参数：一个图对象、节点嵌入、字典类型的参数和一个错误处理函数
def run(
    graph: nx.Graph,  # 输入的图对象
    embeddings: NodeEmbeddings,  # 节点的嵌入数据
    args: dict[str, Any],  # 包含额外设置的字典
    on_error: ErrorHandlerFn,  # 错误发生时调用的函数
) -> GraphLayout:  # 函数返回值类型是图布局

    """这是一个运行方法的定义，用于处理图的布局"""
    
    # 初始化两个空列表，分别存储节点的聚类和大小
    node_clusters = []  # 存储每个节点的聚类信息
    node_sizes = []  # 存储每个节点的大小信息

    # 过滤嵌入数据，去除值为None的节点
    embeddings = _filter_raw_embeddings(embeddings)

    # 获取所有节点的ID
    nodes = list(embeddings.keys())
    # 提取节点的嵌入向量
    embedding_vectors = [embeddings[node_id] for node_id in nodes]

    # 遍历所有节点
    for node_id in nodes:
        # 获取节点的详细信息
        node = graph.nodes[node_id]
        # 尝试获取节点的聚类（优先级：cluster > community）
        cluster = node.get("cluster", node.get("community", -1))
        # 将聚类添加到列表
        node_clusters.append(cluster)
        # 尝试获取节点的度或大小（优先级：degree > size）
        size = node.get("degree", node.get("size", 0))
        # 将大小添加到列表
        node_sizes.append(size)

    # 创建一个附加参数字典，根据节点聚类和大小填充
    additional_args = {}
    # 如果有聚类信息，添加到附加参数
    if len(node_clusters) > 0:
        additional_args["node_categories"] = node_clusters
    # 如果有大小信息，添加到附加参数
    if len(node_sizes) > 0:
        additional_args["node_sizes"] = node_sizes

    # 尝试计算UMAP（统一 manifold 投影）位置
    try:
        # 使用计算好的向量、节点标签和附加参数来计算UMAP布局
        return compute_umap_positions(
            embedding_vectors=np.array(embedding_vectors),  # 节点嵌入向量
            node_labels=nodes,  # 节点标签
            **additional_args,  # 附加参数
            min_dist=args.get("min_dist", 0.75),  # 最小距离，默认0.75
            n_neighbors=args.get("n_neighbors", 5),  # 邻居数量，默认5
        )
    # 捕获并处理异常
    except Exception as e:
        # 记录错误日志
        log.exception("Error running UMAP")
        # 调用错误处理函数
        on_error(e, traceback.format_exc(), None)
        # 当UMAP计算失败时，返回所有节点位于(0,0)的布局
        result = []
        for i in range(len(nodes)):
            # 如果有聚类信息，使用它；否则默认为1
            cluster = node_clusters[i] if len(node_clusters) > 0 else 1
            # 创建NodePosition对象，位置在(0,0)，大小为0，标签为节点ID，聚类信息为str(cluster)
            result.append(
                NodePosition(x=0, y=0, label=nodes[i], size=0, cluster=str(cluster))
            )
        # 返回失败情况下的布局结果
        return result

# 定义一个辅助函数，用于过滤掉嵌入数据中值为None的节点
def _filter_raw_embeddings(embeddings: NodeEmbeddings) -> NodeEmbeddings:
    # 创建一个新的字典，只包含值不为None的节点及其嵌入数据
    return {
        node_id: embedding
        for node_id, embedding in embeddings.items()  # 遍历原字典的键值对
        if embedding is not None  # 只保留值不为None的项
    }

