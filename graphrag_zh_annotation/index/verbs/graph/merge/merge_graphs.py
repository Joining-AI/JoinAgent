# 导入不同的模块，它们帮助我们处理数据和图形
from typing import Any, cast  # 用于指定函数参数和返回值类型的工具
import networkx as nx  # 用于创建和操作图的库
import pandas as pd  # 用于数据处理的库
from datashaper import TableContainer, VerbCallbacks, VerbInput, progress_iterable, verb  # 用于数据操作的库

# 从 graphrag.index.utils 导入加载图的函数
from graphrag.index.utils import load_graph

# 从当前模块的 defaults 子模块导入默认设置
from .defaults import (
    DEFAULT_CONCAT_SEPARATOR,
    DEFAULT_EDGE_OPERATIONS,
    DEFAULT_NODE_OPERATIONS,
)

# 从当前模块的 typing 子模块导入特定的数据类型定义
from .typing import (
    BasicMergeOperation,
    DetailedAttributeMergeOperation,
    NumericOperation,
    StringOperation,
)

# 这是 Microsoft 公司的版权信息，表示代码遵循 MIT 许可证
# """这是一个模块，里面定义了合并图、节点、边和属性的方法。"""

# 使用 @verb 装饰器定义一个名为 "merge_graphs" 的函数，它可能是用来合并多个图的
@verb(name="merge_graphs")

# 定义一个函数叫 merge_graphs，它接受一些参数
def merge_graphs(
    # input 是一个 VerbInput 类型的变量，用来获取输入数据
    input: VerbInput,
    # callbacks 是一个 VerbCallbacks 类型的变量，用来处理回调函数
    callbacks: VerbCallbacks,
    # column 是一个字符串，表示包含图的列的名称（图是用 graphml 格式存储的）
    column: str,
    # to 是一个字符串，表示合并后的新图要存入的列名
    to: str,
    # nodes 是一个字典，定义了节点的操作，默认值是 DEFAULT_NODE_OPERATIONS
    nodes: dict[str, Any] = DEFAULT_NODE_OPERATIONS,
    # edges 是一个字典，定义了边的操作，默认值是 DEFAULT_EDGE_OPERATIONS
    edges: dict[str, Any] = DEFAULT_EDGE_OPERATIONS,
    # _kwargs 是一个关键字参数，这里不用传任何值
    **_kwargs,
) -> TableContainer:
    """
    这个函数的作用是将多个图合并成一个新的图。新图会包含所有原来的图，并且会在表格中新增一列来存放合并后的图。

    注意：这个函数会把所有行合并成一个单一的图。

    使用方法：

# 定义一个函数，用于将子图的节点合并到目标图中，使用node_ops字典中定义的操作
def merge_nodes(
    target: nx.Graph,  # 目标图
    subgraph: nx.Graph,  # 子图
    node_ops: dict[str, DetailedAttributeMergeOperation],  # 节点操作字典
):
    """将子图的节点合并到目标图，按node_ops指定的方式处理属性"""
    # 遍历子图的所有节点
    for node in subgraph.nodes:
        # 如果节点不在目标图中，添加该节点和它的属性
        if node not in target.nodes:
            target.add_node(node, **(subgraph.nodes[node] or {}))
        # 如果节点已在目标图中，合并属性
        else:
            merge_attributes(target.nodes[node], subgraph.nodes[node], node_ops)

# 定义一个函数，用于将子图的边合并到目标图中，使用edge_ops字典中定义的操作
def merge_edges(
    target_graph: nx.Graph,  # 目标图
    subgraph: nx.Graph,  # 子图
    edge_ops: dict[str, DetailedAttributeMergeOperation],  # 边操作字典
):
    """将子图的边合并到目标图，按edge_ops指定的方式处理属性"""
    # 遍历子图的所有边及其数据
    for source, target, edge_data in subgraph.edges(data=True):  # type: ignore
        # 如果目标图中没有这条边，添加边和它的属性
        if not target_graph.has_edge(source, target):
            target_graph.add_edge(source, target, **(edge_data or {}))
        # 如果边已存在，合并属性
        else:
            merge_attributes(target_graph.edges[(source, target)], edge_data, edge_ops)

# 定义一个函数，用于合并源项和目标项的属性，使用ops字典中定义的操作
def merge_attributes(
    target_item: dict[str, Any] | None,  # 目标项
    source_item: dict[str, Any] | None,  # 源项
    ops: dict[str, DetailedAttributeMergeOperation],  # 操作字典
):
    """根据ops中的操作，将源项的属性合并到目标项中"""
    # 确保源项和目标项都是字典
    source_item = source_item or {}
    target_item = target_item or {}
    # 处理通配符操作，遍历源项所有属性
    for op_attrib, op in ops.items():
        # 如果op_attrib是通配符 "*", 对每个属性应用操作
        if op_attrib == "*":
            for attrib in source_item:
                # 如果属性有特定操作，使用它
                if attrib not in ops:
                    apply_merge_operation(target_item, source_item, attrib, op)
        # 如果属性在源项或目标项中存在，应用对应的操作
        else:
            if op_attrib in source_item or op_attrib in target_item:
                apply_merge_operation(target_item, source_item, op_attrib, op)

# 定义一个函数apply_merge_operation，它接受四个参数：
# target_item：一个可能包含键值对的字典，或None
# source_item：另一个可能包含键值对的字典，或None
# attrib：一个字符串，表示要处理的属性名
# op：一个详细的属性合并操作对象

def apply_merge_operation(
    target_item: dict[str, Any] | None,
    source_item: dict[str, Any] | None,
    attrib: str,
    op: DetailedAttributeMergeOperation,
):
    """根据指定的操作，将源项的属性应用到目标项的属性上"""
    
    # 如果目标项或源项是None，用空字典替换
    source_item = source_item or {}
    target_item = target_item or {}

    # 检查操作类型，如果是要替换（无论是基本替换还是字符串替换）
    if (
        op.operation == BasicMergeOperation.Replace
        or op.operation == StringOperation.Replace
    ):
        # 将源项的属性值赋给目标项，如果源项没有值，则赋空字符串
        target_item[attrib] = source_item.get(attrib, None) or ""

    # 如果操作是要跳过（无论是基本跳过还是字符串跳过）
    elif (
        op.operation == BasicMergeOperation.Skip or op.operation == StringOperation.Skip
    ):
        # 保留目标项原有的属性值，如果没有值，则赋空字符串
        target_item[attrib] = target_item.get(attrib, None) or ""

    # 如果操作是字符串连接
    elif op.operation == StringOperation.Concat:
        # 使用分隔符（如果未提供则使用默认分隔符）
        separator = op.separator or DEFAULT_CONCAT_SEPARATOR
        # 获取目标项和源项的属性值，如果没有值，则赋空字符串
        target_attrib = target_item.get(attrib, "") or ""
        source_attrib = source_item.get(attrib, "") or ""
        # 连接两个字符串
        target_item[attrib] = f"{target_attrib}{separator}{source_attrib}"
        # 如果需要去重，慢速方法：排序并去重，再连接
        if op.distinct:
            target_item[attrib] = separator.join(
                sorted(set(target_item[attrib].split(separator)))
            )

    # 假设属性是数字，进行数值操作
    elif op.operation == NumericOperation.Sum:
        # 相加两个属性值，如果无值则视为0
        target_item[attrib] = (target_item.get(attrib, 0) or 0) + (
            source_item.get(attrib, 0) or 0
        )

    elif op.operation == NumericOperation.Average:
        # 计算两个属性值的平均数，如果无值则视为0
        target_item[attrib] = (
            (target_item.get(attrib, 0) or 0) + (source_item.get(attrib, 0) or 0)
        ) / 2

    elif op.operation == NumericOperation.Max:
        # 取两个属性值中的较大者，如果无值则视为0
        target_item[attrib] = max(
            (target_item.get(attrib, 0) or 0), (source_item.get(attrib, 0) or 0)
        )

    elif op.operation == NumericOperation.Min:
        # 取两个属性值中的较小者，如果无值则视为0
        target_item[attrib] = min(
            (target_item.get(attrib, 0) or 0), (source_item.get(attrib, 0) or 0)
        )

    elif op.operation == NumericOperation.Multiply:
        # 两个属性值相乘，如果无值则视为1
        target_item[attrib] = (target_item.get(attrib, 1) or 1) * (
            source_item.get(attrib, 1) or 1
        )

    # 如果操作类型无效，抛出错误
    else:
        msg = f"无效的操作类型：{op.operation}"
        raise ValueError(msg)

# 定义一个名为_get_detailed_attribute_merge_operation的函数，接收一个参数value，这个参数可以是字符串或包含字符串键和任意值的字典
def _get_detailed_attribute_merge_operation(
    value: str | dict[str, Any],
) -> DetailedAttributeMergeOperation:

    # 如果value是一个字符串
    if isinstance(value, str):
        # 创建一个DetailedAttributeMergeOperation对象，其中的operation属性设置为value的值
        return DetailedAttributeMergeOperation(operation=value)

    # 如果value不是一个字符串，那么它应该是一个字典
    else:
        # 使用字典中的所有内容来创建一个DetailedAttributeMergeOperation对象（这里的**value称为解包操作）
        return DetailedAttributeMergeOperation(**value)

