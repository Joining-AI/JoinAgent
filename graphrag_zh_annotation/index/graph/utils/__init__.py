# 导入一个叫做 normalize_node_names 的函数，它会帮助我们整理节点的名字
from .normalize_node_names import normalize_node_names

# 导入一个叫做 stable_largest_connected_component 的函数，这个函数能找出图中最大的稳定连接部分
from .stable_lcc import stable_largest_connected_component

# 这是微软公司的版权声明，告诉我们这个代码的版权属于微软，2024年的时候
# 版权信息：(c) 2024 Microsoft Corporation.（版权所有，2024年微软公司）

# 使用的是 MIT 许可证，意味着你可以自由使用，但需要遵守一定的规则
# Licensed under the MIT License（根据 MIT 许可证授权）

# 这个模块的主要功能是关于索引引擎图的工具包
# "The Indexing Engine graph utils package root."

# 再次导入 normalize_node_names 和 stable_largest_connected_component
# 这样在使用这个模块时，可以直接调用这两个函数，而不用写全路径
from .normalize_node_names import normalize_node_names
from .stable_lcc import stable_largest_connected_component

# 这里定义了 __all__ 变量，告诉别人这个模块导出的公共函数有哪两个
# "__all__" 列表里的就是其他人能直接使用的函数名字
__all__ = ["normalize_node_names", "stable_largest_connected_component"]

