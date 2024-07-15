# 导入一个叫做TopologicalSorter的工具，它帮助我们排列图中节点的顺序
from graphlib import TopologicalSorter

# 这里是一段版权声明，告诉我们这个代码是微软公司写的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，简单说明了下面的函数是关于拓扑排序的工具方法
"""这是一个用于拓扑排序的实用方法。"""

# 再次导入TopologicalSorter，确保我们能用到它
from graphlib import TopologicalSorter

# 定义一个名为topological_sort的函数，它接受一个字典作为参数
# 这个字典的键是字符串，值是字符串列表，表示图中的节点和它们的邻接节点
def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """执行拓扑排序的函数"""
    
    # 创建一个TopologicalSorter对象，传入我们的图
    ts = TopologicalSorter(graph)
    
    # 使用这个对象的static_order()方法获取排序后的节点列表，并转换为列表返回
    return list(ts.static_order())

