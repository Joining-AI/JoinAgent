# 导入cast函数，它用于类型转换
from typing import cast

# 导入pandas库，它用于处理数据
import pandas as pd

# 导入datashaper库中的TableContainer、VerbInput和verb装饰器
from datashaper import TableContainer, VerbInput, verb

# 从graphrag.index.utils.ds_util模块导入get_required_input_table函数，这个函数帮助获取需要的输入表格
from graphrag.index.utils.ds_util import get_required_input_table

# 这是微软公司的版权信息，表示代码由他们所有
# Licensed under the MIT License 表示代码遵循MIT许可证

# 这个模块包含了create_graph、_get_node_attributes、_get_edge_attributes和_get_attribute_column_mapping方法的定义
# 方法是用来执行特定任务的代码块

# 定义一个名为"compute_edge_combined_degree"的verb，verb是datashaper中的一种特殊函数，通常用于数据操作
@verb(name="compute_edge_combined_degree")

# 定义一个名为compute_edge_combined_degree的函数，它接收一些参数并返回一个TableContainer对象
def compute_edge_combined_degree(
    # 输入：VerbInput类型的变量，表示图的边表
    input: VerbInput,
    # 输出列的名称，默认为"rank"
    to: str = "rank",
    # 节点名称列的名称，默认为"title"
    node_name_column: str = "title",
    # 节点度数列的名称，默认为"degree"
    node_degree_column: str = "degree",
    # 边源节点列的名称，默认为"source"
    edge_source_column: str = "source",
    # 边目标节点列的名称，默认为"target"
    edge_target_column: str = "target",
    # 其他可能的参数，这里用**_kwargs表示
    **_kwargs,
) -> TableContainer:
    """
    计算图中每条边的综合度数。

    输入表格：
    - input: 边表格
    - nodes: 节点表格。

    参数：
    - to: 综合度数输出列的名称，默认是"rank"。
    """

    # 将输入转换为DataFrame类型
    edge_df: pd.DataFrame = cast(pd.DataFrame, input.get_input())

    # 如果to指定的列已经存在于edge_df中，直接返回原表格
    if to in edge_df.columns:
        return TableContainer(table=edge_df)

    # 获取节点度数表格
    node_degree_df = _get_node_degree_table(input, node_name_column, node_degree_column)

    # 定义一个内部函数，将度数加入到给定的DataFrame中
    def join_to_degree(df: pd.DataFrame, column: str) -> pd.DataFrame:
        # 创建度数列的新名称
        degree_column = _degree_colname(column)
        # 将节点度数表格与df按column列合并，保留所有行（左连接）
        result = df.merge(
            node_degree_df.rename(
                columns={
                    node_name_column: column,  # 重命名节点名称列
                    node_degree_column: degree_column,  # 重命名节点度数列
                }
            ),
            on=column,  # 合并依据
            how="left",
        )
        # 将度数列中的缺失值填充为0
        result[degree_column] = result[degree_column].fillna(0)
        # 返回处理后的表格
        return result

    # 将源节点度数添加到edge_df
    edge_df = join_to_degree(edge_df, edge_source_column)
    # 将目标节点度数添加到edge_df
    edge_df = join_to_degree(edge_df, edge_target_column)

    # 计算每条边的综合度数（源节点度数 + 目标节点度数），并将结果存入新列'to'
    edge_df[to] = (
        edge_df[_degree_colname(edge_source_column)]  # 源节点度数
        + edge_df[_degree_colname(edge_target_column)]  # 目标节点度数
    )

    # 返回包含综合度数的表格
    return TableContainer(table=edge_df)

# 定义一个辅助函数，根据传入的列名生成度数列名
def _degree_colname(column: str) -> str:
    return f"{column}_degree"

# 定义另一个辅助函数，从输入获取节点度数表格
def _get_node_degree_table(
    input: VerbInput, node_name_column: str, node_degree_column: str
) -> pd.DataFrame:
    # 获取输入中必需的"nodes"表格
    nodes_container = get_required_input_table(input, "nodes")
    # 将nodes表格转换为DataFrame类型
    nodes = cast(pd.DataFrame, nodes_container.table)
    # 只保留node_name_column和node_degree_column这两列
    return cast(pd.DataFrame, nodes[[node_name_column, node_degree_column]])

