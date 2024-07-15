# 导入必要的库，它们帮助我们处理不同类型的数据和图
from typing import Any, cast  # 定义数据类型的工具
import networkx as nx  # 用于创建和操作图形的库
import pandas as pd  # 处理表格数据的库
from datashaper import TableContainer, VerbCallbacks, VerbInput, progress_iterable, verb  # 数据操作和进度显示的工具
from graphrag.index.utils import load_graph  # 加载图形的函数，来自graphrag库的一个模块

# 这个是版权声明，表示代码由微软公司所有，并遵循MIT许可证

# 定义一个模块，里面有一些方法（函数）关于如何处理图形数据
"""A module containing unpack_graph, _run_unpack, _unpack_nodes and _unpack_edges methods definition."""

# 以下是一些默认要复制的属性名
default_copy = ["level"]

# 定义一个名为"unpack_graph"的函数（verb是datashaper中的一个装饰器，用于标记特殊功能的函数）
@verb(name="unpack_graph")

# 定义一个函数 unpack_graph，接收一些参数
def unpack_graph(
    input: VerbInput,  # 输入的数据，类型是 VerbInput
    callbacks: VerbCallbacks,  # 回调函数，用于进度显示
    column: str,  # 指定包含图信息的列名
    type: str,  # 图数据类型，可以是 'node' 或 'edge'
    copy: list[str] | None = None,  # 要复制到结果中的原数据列名，默认为 None
    embeddings_column: str = "embeddings",  # 嵌入向量列名，默认为 'embeddings'
    **kwargs,  # 其他任意参数
) -> TableContainer:  # 返回一个 TableContainer 对象

    """
    这个函数的作用是从 graphml 格式的图中，解包出节点或边，变成节点或边的列表。
    它会为每个节点或边的属性创建一列。

    使用示例：

# 定义一个函数_run_unpack，接收四个参数：可能是图文件或图对象的graphml_or_graph，类型选择unpack_type，节点嵌入信息embeddings，以及一个包含各种参数的字典args
def _run_unpack(
    graphml_or_graph: str | nx.Graph,  # 可以是字符串（图文件）或网络图对象
    unpack_type: str,  # 选择解包的类型，可能是"nodes"或"edges"
    embeddings: dict[str, list[float]],  # 字典，键是节点标签，值是节点的浮点数列表
    args: dict[str, Any],  # 包含任意类型的参数字典
) -> list[dict[str, Any]]:  # 返回值是一个包含字典的列表

    # 加载图数据
    graph = load_graph(graphml_or_graph)

    # 如果unpack_type是"nodes"，调用_unpack_nodes函数处理节点
    if unpack_type == "nodes":
        return _unpack_nodes(graph, embeddings, args)

    # 如果unpack_type是"edges"，调用_unpack_edges函数处理边
    if unpack_type == "edges":
        return _unpack_edges(graph, args)

    # 如果unpack_type既不是"nodes"也不是"edges"，生成错误消息并抛出异常
    msg = f"未知类型 {unpack_type}"
    raise ValueError(msg)  # 抛出一个值错误，因为类型未定义


# 定义一个内部函数_unpack_nodes，用于处理节点
def _unpack_nodes(
    graph: nx.Graph,  # 网络图对象
    embeddings: dict[str, list[float]],  # 节点嵌入信息字典
    _args: dict[str, Any],  # 参数字典，这里未使用
) -> list[dict[str, Any]]:  # 返回值是一个包含字典的列表

    # 遍历图中的每个节点及其数据，创建一个字典列表
    return [
        {
            "label": label,  # 节点的标签
            **(node_data or {}),  # 节点的数据，如果为空则为{}
            "graph_embedding": embeddings.get(label),  # 节点的嵌入信息，从embeddings字典中获取
        }  # 创建一个新字典
        for label, node_data in graph.nodes(data=True)  # 获取图的所有节点和其数据
    ]


# 定义另一个内部函数_unpack_edges，用于处理边
def _unpack_edges(graph: nx.Graph, _args: dict[str, Any]) -> list[dict[str, Any]]:
    # 遍历图中的每条边及其数据，创建一个字典列表
    return [
        {
            "source": source_id,  # 边的源节点ID
            "target": target_id,  # 边的目标节点ID
            **(edge_data or {}),  # 边的数据，如果为空则为{}
        }  # 创建一个新字典
        for source_id, target_id, edge_data in graph.edges(data=True)  # 获取图的所有边和其数据
    ]

