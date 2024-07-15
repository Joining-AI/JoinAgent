# 导入一个叫做 networkx 的库，它帮助我们处理图形数据
import networkx as nx

# 这是微软公司2024年的版权声明，用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个关于 networkx 库加载图形工具的定义
"""Networkx load_graph 实用工具的定义。"""

# 再次导入 networkx，这里是为了确保代码清晰，虽然之前已经导入过
import networkx as nx

# 定义一个名为 load_graph 的函数，它接受一个参数
# 参数可以是一个字符串或者一个 networkx 图形
def load_graph(graphml: str | nx.Graph) -> nx.Graph:
    # 如果参数是字符串类型
    if isinstance(graphml, str):
        # 那么就从这个字符串表示的 graphml 文件中解析并返回一个 networkx 图形
        return nx.parse_graphml(graphml)
    # 如果参数已经是 networkx 图形
    else:
        # 直接返回这个图形
        return graphml

