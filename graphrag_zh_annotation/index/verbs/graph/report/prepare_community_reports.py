# 导入logging模块，它用于记录程序运行时的日志信息
import logging

# 导入cast函数，它是类型转换的工具，来自typing模块
from typing import cast

# 导入pandas库，这是一个用于数据分析的库，我们用它来处理数据
import pandas as pd

# 导入datashaper的一些组件，它们是数据处理的工具
from datashaper import (
    # TableContainer是用来存储表格数据的类
    TableContainer,
    # VerbCallbacks是处理命令的回调函数集合
    VerbCallbacks,
    # VerbInput是处理输入的类
    VerbInput,
    # progress_iterable是一个可以显示进度的迭代器
    progress_iterable,
    # verb是定义数据处理命令的装饰器
    verb,
)

# 导入graphrag.index.graph.extractors.community_reports.schemas中的数据结构
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 导入graphrag.index.graph.extractors.community_reports模块中的一些函数，用于过滤和处理数据
from graphrag.index.graph.extractors.community_reports import (
    # 过滤声明到节点的函数
    filter_claims_to_nodes,
    # 过滤边到节点的函数
    filter_edges_to_nodes,
    # 过滤节点到特定级别的函数
    filter_nodes_to_level,
    # 获取层级的函数
    get_levels,
    # 设置上下文超出标志的函数
    set_context_exceeds_flag,
    # 设置上下文大小的函数
    set_context_size,
    # 对上下文进行排序的函数
    sort_context,
)

# 导入graphrag.index.utils.ds_util中的两个辅助函数，用于获取输入表
from graphrag.index.utils.ds_util import get_named_input_table, get_required_input_table

# 引入logging模块的日志系统，并设置日志记录器的名字为当前模块的名字
log = logging.getLogger(__name__)

# 定义一个名为"prepare_community_reports"的数据处理命令
@verb(name="prepare_community_reports")

# 定义一个函数，叫 prepare_community_reports，它需要3个参数
def prepare_community_reports(
    输入：VerbInput,  # 这是一个特定类型的输入数据
    回调函数：VerbCallbacks,  # 另一个特定类型的回调函数，用来追踪进度
    最大令牌数：int = 16_000,  # 默认值是16000，可能是一个限制数据量的数字
    **_kwargs,  # 其他任意多的键值对参数，但这里我们不用它们
) -> TableContainer:  # 函数会返回一个 TableContainer 类型的结果

    """
    这个函数用来生成每个行的实体，并可选地生成这些实体的图。
    """

    # 准备社区报告
    # 获取输入中的 "nodes" 表格，并转换成 DataFrame（一种数据结构）
    节点_df = cast(pd.DataFrame, get_required_input_table(input, "nodes").table)
    
    # 获取输入中的 "edges" 表格，也转换成 DataFrame
    边_df = cast(pd.DataFrame, get_required_input_table(input, "edges").table)

    # 获取输入中可选的 "claims" 表格，如果有的话，同样转成 DataFrame
    声明_df = get_named_input_table(input, "claims")
    if 声明_df is not None:  # 如果 "claims" 存在
        声明_df = cast(pd.DataFrame, 声明_df.table)

    # 根据 "nodes" 数据获取不同级别的列表
    级别列表 = get_levels(node_df, schemas.NODE_LEVEL)

    # 创建一个空列表，用来存放处理后的数据
    处理过的表格 = []

    # 遍历每个级别（用一个带进度条的迭代器，让操作看起来更直观）
    for 级别 in progress_iterable(levels, callbacks.progress, len(levels)):
        # 对当前级别准备报告
        当前级别社区_df = _prepare_reports_at_level(
            节点_df, 边_df, 声明_df, 级别, 最大令牌数
        )
        
        # 把处理好的数据添加到列表里
        处理过的表格.append(当前级别社区_df)

    # 将所有级别处理过的数据合并成一个大的 DataFrame
    合并后的表格 = pd.concat(dfs)

    # 返回结果，即包含所有社区信息的表格容器
    return TableContainer(table=合并后的表格)

# 定义一个函数，用来准备不同级别的报告
def _prepare_reports_at_level(
    # 输入的数据框（DataFrame）：节点信息、边信息、可能有的主张信息
    node_df: pd.DataFrame,
    edge_df: pd.DataFrame,
    claim_df: pd.DataFrame | None,
    # 当前处理的级别
    level: int,
    # 最大允许的文本长度
    max_tokens: int = 16_000,
    # 各种列名的默认值
    # ...
):

    # 定义一个内部函数，用于获取与边相关的节点详情
    def get_edge_details(node_df, edge_df, name_col):
        # 将边数据框中指定列与节点名称列合并
        return node_df.merge(
            # 选择边的特定列并重命名
            cast(pd.DataFrame, edge_df[[name_col, schemas.EDGE_DETAILS]]).rename(
                columns={name_col: schemas.NODE_NAME}
            ),
            # 根据节点名称进行左连接
            on=schemas.NODE_NAME,
            how="left",
        )

    # 过滤出指定级别的节点
    level_node_df = filter_nodes_to_level(node_df, level)
    # 打印当前级别节点的数量
    log.info("Number of nodes at level=%s => %s", level, len(level_node_df))
    # 获取当前级别所有节点的名字
    nodes = level_node_df[node_name_column].tolist()

    # 过滤出与目标节点相关的边
    level_edge_df = filter_edges_to_nodes(edge_df, nodes)
    # 过滤出与目标节点相关的主张（如果存在）
    level_claim_df = filter_claims_to_nodes(claim_df, nodes) if claim_df is not None else None

    # 将所有边的详情按节点合并
    merged_node_df = pd.concat([
        # 获取以节点为源和目标的边详情
        get_edge_details(level_node_df, level_edge_df, edge_source_column),
        get_edge_details(level_node_df, level_edge_df, edge_target_column),
    ], axis=0)
    # 按照特定列进行分组，聚合某些列的值
    merged_node_df = (
        merged_node_df.groupby([
            node_name_column,
            node_community_column,
            node_degree_column,
            node_level_column,
        ])
        .agg({node_details_column: "first", edge_details_column: list})
        .reset_index()
    )

    # 如果有主张信息，将其与节点合并
    if level_claim_df is not None:
        merged_node_df = merged_node_df.merge(
            # 选择主张的特定列并重命名
            cast(pd.DataFrame, level_claim_df[[claim_subject_column, claim_details_column]]).rename(
                columns={claim_subject_column: node_name_column}
            ),
            on=node_name_column,
            how="left",
        )
    # 再次按特定列进行分组，聚合某些列的值
    merged_node_df = (
        merged_node_df.groupby([
            node_name_column,
            node_community_column,
            node_level_column,
            node_degree_column,
        ])
        .agg({
            node_details_column: "first",
            edge_details_column: "first",
            **({claim_details_column: list} if level_claim_df is not None else {}),
        })
        .reset_index()
    )

    # 创建包含所有节点详细信息的新列
    merged_node_df[schemas.ALL_CONTEXT] = merged_node_df.apply(
        # 生成包含各列信息的字典
        lambda x: {
            node_name_column: x[node_name_column],
            node_degree_column: x[node_degree_column],
            node_details_column: x[node_details_column],
            edge_details_column: x[edge_details_column],
            claim_details_column: x[claim_details_column]
            if level_claim_df is not None
            else [],
        },
        axis=1,
    )

    # 按社区分组，收集所有节点的详细信息
    community_df = (
        merged_node_df.groupby(node_community_column)
        .agg({schemas.ALL_CONTEXT: list})
        .reset_index()
    )
    # 对每个社区的上下文信息进行排序和处理
    community_df[schemas.CONTEXT_STRING] = community_df[schemas.ALL_CONTEXT].apply(
        lambda x: sort_context(
            x,
            # ...各种列名参数...
        )
    )
    # 设置社区的上下文大小
    set_context_size(community_df)
    # 检查上下文是否超过最大长度
    set_context_exceeds_flag(community_df, max_tokens)

    # 添加当前级别的信息
    community_df[schemas.COMMUNITY_LEVEL] = level
    # 返回处理后的社区数据框
    return community_df

