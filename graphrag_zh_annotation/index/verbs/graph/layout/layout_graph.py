# 导入一些Python库，这些库帮助我们处理数据和图形
from enum import Enum # 用于创建枚举类型，类似于列表但每个项都有唯一的名字
from typing import Any, cast # 帮助我们指定函数参数和返回值的类型
import networkx as nx # 用于创建和操作图的库
import pandas as pd # 用于处理表格数据的库
from datashaper import TableContainer, VerbCallbacks, VerbInput, progress_callback, verb # 用于数据操作的库
from graphrag.index.graph.visualization import GraphLayout # 用于图可视化的类
from graphrag.index.utils import load_graph # 用于加载图的辅助函数
from graphrag.index.verbs.graph.embed.typing import NodeEmbeddings # 用于定义节点嵌入的类型

# 这是微软公司的版权信息
# 版权所有 2024 微软公司
# 根据MIT许可证授权

# 定义一个表示布局策略的枚举类
class LayoutGraphStrategyType(Enum):
    # 枚举项：UMAP（一种降维算法）
    umap = "umap"
    # 枚举项：零向量布局，所有节点都在原点
    zero = "zero"

    # 当打印或显示枚举对象时，返回其字符串形式
    def __repr__(self):
        return f'"{self.value}"'

# 定义一个名为"layout_graph"的函数，它是一个verb，用于处理数据
@verb(name="layout_graph")

# 定义一个名为layout_graph的函数，它接受一些参数
def layout_graph(
    input: VerbInput,       # 输入数据，可能是表格形式
    callbacks: VerbCallbacks,  # 回调函数，用于处理进度和交互
    strategy: dict[str, Any],  # 布局策略，字典形式，定义如何布局图形
    embeddings_column: str,  # 含有嵌入信息的列名
    graph_column: str,      # 含有图数据的列名
    to: str,                # 输出节点位置的新列名
    graph_to: str | None = None,  # 可选，输出布局后图的新列名，默认为None
    **_kwargs: dict,        # 其他未命名的参数，这里不使用
) -> TableContainer:  # 函数返回一个TableContainer对象，包含处理后的表格

    """
    这个函数的作用是将图形布局，输入的图应该是graphml格式。它会输出一个新的列，包含布局后的节点位置。

    使用方法示例：

# 定义一个名为_run_layout的函数，它接受四个参数：策略（布局方式）、图数据、节点嵌入信息、参数字典和报告器（用于报告错误）
def _run_layout(
    strategy: LayoutGraphStrategyType,  # 策略类型，比如UMAP或Zero
    graphml_or_graph: str | nx.Graph,  # 图的数据，可以是字符串（图的描述）或网络图对象
    embeddings: NodeEmbeddings,  # 节点的嵌入信息
    args: dict[str, Any],  # 额外的参数
    reporter: VerbCallbacks,  # 错误报告回调函数
) -> GraphLayout:  # 返回一个新的布局图形

    # 加载图数据
    graph = load_graph(graphml_or_graph)

    # 根据策略执行不同的布局方法
    # 如果策略是UMAP
    match strategy:
        case LayoutGraphStrategyType.umap:
            # 从.methods.umap模块导入run_umap函数
            from .methods.umap import run as run_umap

            # 执行UMAP布局并返回结果
            return run_umap(
                graph,  # 输入的图
                embeddings,  # 节点嵌入信息
                args,  # 额外参数
                # 如果出现错误，通过报告器报告错误
                lambda e, stack, d: reporter.error("Error in Umap", e, stack, d),
            )

        # 如果策略是Zero
        case LayoutGraphStrategyType.zero:
            # 从.methods.zero模块导入run_zero函数
            from .methods.zero import run as run_zero

            # 执行Zero布局并返回结果
            return run_zero(
                graph,  # 输入的图
                args,  # 额外参数
                # 如果出现错误，通过报告器报告错误
                lambda e, stack, d: reporter.error("Error in Zero", e, stack, d),
            )

        # 如果策略未知
        case _:
            # 创建一个错误消息
            msg = f"Unknown strategy {strategy}"
            # 抛出一个ValueError，因为策略无效
            raise ValueError(msg)

# 定义一个名为_apply_layout_to_graph的函数，它接受两个参数：图数据和布局结果
def _apply_layout_to_graph(
    graphml_or_graph: str | nx.Graph,  # 图的数据
    layout: GraphLayout,  # 布局结果
) -> str:  # 返回更新后的图描述字符串

    # 加载图数据
    graph = load_graph(graphml_or_graph)

    # 遍历布局结果中的每个节点位置
    for node_position in layout:
        # 如果节点存在于图中
        if node_position.label in graph.nodes:
            # 更新节点的x坐标、y坐标和大小
            graph.nodes[node_position.label]["x"] = node_position.x
            graph.nodes[node_position.label]["y"] = node_position.y
            graph.nodes[node_position.label]["size"] = node_position.size

    # 将更新后的图转换为GraphML格式的字符串并返回
    return "\n".join(nx.generate_graphml(graph))

