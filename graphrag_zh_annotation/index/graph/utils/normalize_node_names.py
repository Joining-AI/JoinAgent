# 导入一个叫做html的模块，它帮助我们处理HTML文本
import html

# 导入一个叫做networkx的模块，这个模块用来创建和操作图（图形数据结构）
import networkx as nx

# 这里是微软公司的版权声明，告诉我们这个代码是2024年微软公司的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个模块的描述，里面有一个方法叫做normalize_node_names
"""这是一个包含normalize_node_names方法定义的模块。"""

# 再次导入html和networkx模块，这样我们可以在函数内部使用它们
import html
import networkx as nx


# 定义一个名为normalize_node_names的函数，它接受一个图（可以是无向或有向的）作为参数
def normalize_node_names(graph: nx.Graph | nx.DiGraph) -> nx.Graph | nx.DiGraph:
    """这个函数用来规范化图中节点的名字"""
    
    # 创建一个字典，键是图中的每个节点，值是经过处理的节点名
    # html.unescape() 将HTML特殊字符转为普通字符，upper() 把名字变成大写，strip() 去掉两边的空白
    node_mapping = {node: html.unescape(node.upper().strip()) for node in graph.nodes()}  # type: ignore

    # 使用relabel_nodes函数，用新的节点名替换旧的节点名，返回一个新的图
    # 返回的图类型与输入图相同，可以是无向图或有向图
    return nx.relabel_nodes(graph, node_mapping)

