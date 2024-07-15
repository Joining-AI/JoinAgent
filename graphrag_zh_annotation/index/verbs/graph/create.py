# 这段代码是用来创建一个图形（graph）的，图形由节点（nodes）和边（edges）组成。让我们逐行解释：

from typing import Any
# 这行导入了一个叫做 "Any" 的类型，它在Python中用于表示任何类型的值。

import networkx as nx
# 导入了一个名为 "networkx" 的库，这个库专门用来创建和操作图形。

import pandas as pd
# 导入了 "pandas" 库，这是一个强大的数据处理库，通常用来处理表格数据。

from datashaper import TableContainer, VerbCallbacks, VerbInput, progress_iterable, verb
# 导入了一些来自 "datashaper" 库的工具，它们帮助处理数据并显示进度。

from graphrag.index.utils import clean_str
# 导入了一个名为 "clean_str" 的函数，它可能用于清理或格式化字符串。

# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License
# 这是版权信息，说明代码由微软公司编写，并遵循MIT许可证。

"""
# 这是一个多行注释，描述了这个模块包含的功能。
"""

from typing import Any
# 这行再次导入 "Any" 类型，可能是因为文件中有多个代码块。

import networkx as nx
import pandas as pd
from datashaper import TableContainer, VerbCallbacks, VerbInput, progress_iterable, verb
from graphrag.index.utils import clean_str
# 这些导入语句与上面相同，确保库被正确引入。

# 定义一些默认的节点和边的属性名：
DEFAULT_NODE_ATTRIBUTES = ["label", "type", "id", "name", "description", "community"]
# 这是一个列表，包含了创建节点时可能用到的属性名。

DEFAULT_EDGE_ATTRIBUTES = ["label", "type", "name", "source", "target"]
# 这也是一个列表，包含了创建边时可能用到的属性名。

# 下面是一个带注释的函数，叫做 "create_graph"，它的具体功能我们会在接下来的代码中看到。
@verb(name="create_graph")

# 定义一个函数，叫 create_graph
def create_graph(
    # 这个函数需要的输入参数：
    # input 是一个 VerbInput 类型的东西，用来获取数据
    input: VerbInput,
    # callbacks 是一个 VerbCallbacks 类型的东西，用来做回调操作
    callbacks: VerbCallbacks,
    # to 是一个字符串，表示新生成的图要放在数据框的哪个列
    to: str,
    # type 也是一个字符串，表示我们要创建的图的类型，可以是 'node' 或 'edge'
    type: str,  # noqa A002 (这个注释是给代码检查工具用的，可以忽略)
    # graph_type 默认是 'undirected'，表示无向图
    graph_type: str = "undirected",
    # 其他任何额外的参数都可以通过 **kwargs 传进来
    **kwargs,
) -> TableContainer:
    """
    这个函数会从数据框创建一个图。它会在数据框里添加一列，里面是图的数据。

    注意：所有行会被合并成一个图。

    使用方法示例：

# 定义一个函数，输入是任何类型，返回值是字符串
def _clean_value(value: Any) -> str:
    # 如果输入的值是None，返回空字符串
    if value is None:
        return ""
    # 如果输入的值是字符串，调用clean_str函数处理并返回
    if isinstance(value, str):
        return clean_str(value)

    # 创建一个错误信息，说明输入的值必须是字符串或None，但实际得到的是其他类型
    msg = f"Value must be a string or None, got {type(value)}"
    # 抛出一个类型错误，附带错误信息
    raise TypeError(msg)

# 定义一个函数，输入是一个包含键为字符串的字典，返回值也是一个字符串的字典
def _get_node_attributes(args: dict[str, Any]) -> dict[str, Any]:
    # 获取args字典中"attributes"键对应的值，如果没有就用DEFAULT_NODE_ATTRIBUTES替换
    mapping = _get_attribute_column_mapping(
        args.get("attributes", DEFAULT_NODE_ATTRIBUTES)
    )
    # 检查mapping中是否包含"id"、"label"和"name"中的任何一个
    if "id" not in mapping and "label" not in mapping and "name" not in mapping:
        # 如果都不包含，创建一个错误信息
        msg = "You must specify an id, label, or name column in the node attributes"
        # 抛出一个值错误，附带错误信息
        raise ValueError(msg)
    # 返回处理后的映射字典
    return mapping

# 类似于_get_node_attributes的函数，但用于处理边的属性
def _get_edge_attributes(args: dict[str, Any]) -> dict[str, Any]:
    mapping = _get_attribute_column_mapping(
        args.get("attributes", DEFAULT_EDGE_ATTRIBUTES)
    )
    # 检查mapping中是否包含"source"和"target"两个键
    if "source" not in mapping or "target" not in mapping:
        # 如果缺少任何一个，创建一个错误信息
        msg = "You must specify a source and target column in the edge attributes"
        # 抛出一个值错误，附带错误信息
        raise ValueError(msg)
    # 返回处理后的映射字典
    return mapping

# 定义一个函数，输入可以是字符串到任何类型的字典或字符串列表，返回值是字符串到字符串的字典
def _get_attribute_column_mapping(
    in_attributes: dict[str, Any] | list[str],
) -> dict[str, str]:
    # 如果输入的是字典，直接返回并添加一个空格
    if isinstance(in_attributes, dict):
        return {
            **in_attributes,
        }
    # 如果输入的是列表，创建一个字典，将列表中的每个元素作为键和值
    else:
        return {attrib: attrib for attrib in in_attributes}

# 定义一个函数，根据输入的字符串（"directed"或其它），返回一个有向图（nx.DiGraph）或无向图（nx.Graph）
def _create_nx_graph(graph_type: str) -> nx.Graph:
    # 如果graph_type是"directed"，返回有向图
    if graph_type == "directed":
        return nx.DiGraph()
    # 其它情况，返回无向图
    else:
        return nx.Graph()

