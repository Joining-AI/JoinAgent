# 导入所需的不同工具包，它们帮助处理图和数据
from typing import Any    # 用于类型注解的库
import networkx as nx      # 用于处理图的库
from graphrag.index.graph.embedding import embed_nod2vec  # 图嵌入算法node2vec
from graphrag.index.graph.utils import stable_largest_connected_component  # 找到最大的稳定连接组件
from graphrag.index.verbs.graph.embed.typing import NodeEmbeddings  # 定义节点嵌入的类型

# 这段代码的版权信息，由微软公司拥有，遵循MIT许可证

# 这是一个包含run方法定义的模块
from typing import Any

import networkx as nx

from graphrag.index.graph.embedding import embed_nod2vec
from graphrag.index.graph.utils import stable_largest_connected_component
from graphrag.index.verbs.graph.embed.typing import NodeEmbeddings


# 定义一个名为run的函数，输入是网络x图和字典参数，返回节点嵌入
def run(graph: nx.Graph, args: dict[str, Any]) -> NodeEmbeddings:
    """这个函数用来执行一些操作"""
    
    # 如果参数中设置使用最大连通分量（默认为True），则找到并使用它
    if args.get("use_lcc", True):
        graph = stable_largest_connected_component(graph)

    # 使用node2vec算法创建图的嵌入
    # 这些参数是从输入的字典中获取的，默认值如下：
    dimensions = args.get("dimensions", 1536)  # 嵌入的维度
    num_walks = args.get("num_walks", 10)     # 每个节点行走次数
    walk_length = args.get("walk_length", 40)   # 每次行走的长度
    window_size = args.get("window_size", 2)   # 词窗口大小
    iterations = args.get("iterations", 3)     # 算法迭代次数
    random_seed = args.get("random_seed", 86)   # 随机种子

    embeddings = embed_nod2vec(
        graph=graph,
        dimensions=dimensions,
        num_walks=num_walks,
        walk_length=walk_length,
        window_size=window_size,
        iterations=iterations,
        random_seed=random_seed,
    )

    # 将节点、对应的嵌入向量和严格比较标志打包成元组
    pairs = zip(embeddings.nodes, embeddings.embeddings.tolist(), strict=True)

    # 按节点名称排序这些元组
    sorted_pairs = sorted(pairs, key=lambda x: x[0])

    # 将排序后的元组转换成字典并返回
    return dict(sorted_pairs)

