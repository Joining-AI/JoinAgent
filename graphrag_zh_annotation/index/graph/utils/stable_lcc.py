# 这段代码是用来找出一个图的最大连通分量，并确保结果是稳定的，即相同的输入图会得到相同的输出最大连通分量。

# 从typing模块导入Any和cast，这两个是类型相关的辅助工具
from typing import Any, cast

# 导入networkx库，这个库用于处理图形数据
import networkx as nx

# 从graspologic.utils模块导入largest_connected_component函数，这个函数用于找到图的最大连通分量
from graspologic.utils import largest_connected_component

# 从当前模块的normalize_node_names导入函数，这个函数用来规范化节点名称
from .normalize_node_names import normalize_node_names

# 以下是一个名为stable_largest_connected_component的函数，它接受一个网络X的图作为输入，并返回一个网络X的图作为输出
def stable_largest_connected_component(graph: nx.Graph) -> nx.Graph:

    # 首先，我们复制输入的图，防止对原图进行修改
    graph = graph.copy()

    # 使用largest_connected_component函数找到并返回图的最大连通分量，然后将结果强制转换回nx.Graph类型
    graph = cast(nx.Graph, largest_connected_component(graph))

    # 接下来，规范化图中的节点名称，以确保稳定性
    graph = normalize_node_names(graph)

    # 最后，调用一个名为_stabilize_graph的内部函数（未显示在此处）来进一步稳定图
    # 注意：_stabilize_graph函数不在这个代码块中，但它是这个过程的一部分
    return _stabilize_graph(graph)

# 定义一个名为_stabilize_graph的函数，它接受一个名为graph的网络图对象作为参数，返回值也是一个网络图对象
def _stabilize_graph(graph: nx.Graph) -> nx.Graph:
    # 确保无论输入的图是无向还是有向，我们总是得到一个稳定表示的图
    # 如果输入的图是有向的，创建一个新的有向图；如果是无向的，创建一个新的无向图
    fixed_graph = nx.DiGraph() if graph.is_directed() else nx.Graph()

    # 获取图中的所有节点及其数据，并按节点名称排序
    sorted_nodes = graph.nodes(data=True)
    sorted_nodes = sorted(sorted_nodes, key=lambda x: x[0])

    # 将排序后的节点添加到新图fixed_graph中
    fixed_graph.add_nodes_from(sorted_nodes)

    # 获取图中的所有边及其数据
    edges = list(graph.edges(data=True))

    # 如果图是无向的，我们需要以稳定的方式创建边
    # 因为在无向图中，A到B和B到A是等价的，但它们的顺序可能影响下游处理
    # 所以我们对边的源节点和目标节点进行排序，确保始终得到相同的顺序
    if not graph.is_directed():
        # 定义一个函数，用于对边的源节点和目标节点进行排序
        def _sort_source_target(edge):
            source, target, edge_data = edge
            if source > target:
                # 交换源节点和目标节点的位置
                temp = source
                source = target
                target = temp
            return source, target, edge_data

        # 对无向图的边列表应用排序函数
        edges = [_sort_source_target(edge) for edge in edges]

    # 定义一个函数，用于生成边的唯一标识字符串
    def _get_edge_key(source: Any, target: Any) -> str:
        return f"{source} -> {target}"

    # 根据边的源节点和目标节点的顺序对边进行排序
    edges = sorted(edges, key=lambda x: _get_edge_key(x[0], x[1]))

    # 将排序后的边添加到新图fixed_graph中
    fixed_graph.add_edges_from(edges)
    
    # 返回处理后的稳定图
    return fixed_graph

