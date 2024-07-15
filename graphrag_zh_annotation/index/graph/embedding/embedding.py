# 导入必要的库，这些库帮助我们处理数据和图形
from dataclasses import dataclass  # 用于创建类的数据结构
import graspologic as gc  # 图论和图嵌入的库
import networkx as nx  # 处理图形的库
import numpy as np  # 数值计算的库

# 这是微软公司的版权信息，意味着代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一些有用的辅助函数，用于生成图的嵌入

# 使用dataclass创建一个类，存储节点和它们的嵌入
@dataclass
class NodeEmbeddings:
    nodes: list[str]  # 节点名称列表
    embeddings: np.ndarray  # 节点的嵌入向量数组


# 这个函数使用Node2Vec算法生成节点的嵌入
def embed_nod2vec(
    graph: nx.Graph | nx.DiGraph,  # 输入的图，可以是无向或有向的
    dimensions: int = 1536,  # 嵌入向量的维度，默认是1536
    num_walks: int = 10,  # 每个节点要进行的随机游走次数，默认是10
    walk_length: int = 40,  # 每次随机游走的步数，默认是40
    window_size: int = 2,  # 对于上下文窗口大小，默认是2
    iterations: int = 3,  # 训练迭代次数，默认是3
    random_seed: int = 86,  # 随机数种子，确保结果可复现，默认是86
) -> NodeEmbeddings:
    # 使用graspologic库中的node2vec方法生成嵌入
    lcc_tensors = gc.embed.node2vec_embed(  # 忽略类型检查警告
        graph=graph,
        dimensions=dimensions,
        window_size=window_size,
        iterations=iterations,
        num_walks=num_walks,
        walk_length=walk_length,
        random_seed=random_seed,
    )

    # 将生成的嵌入和节点列表返回
    return NodeEmbeddings(embeddings=lcc_tensors[0], nodes=lcc_tensors[1])

