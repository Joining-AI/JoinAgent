# 导入必要的工具
from typing import cast  # 类型转换工具
import pandas as pd  # 数据处理库
import graphrag.index.graph.extractors.community_reports.schemas as schemas  # 图谱报告的模式模块
from graphrag.query.llm.text_utils import num_tokens  # 计算文本中单词数量的函数

# 版权声明
# 2024年微软公司的版权
# 根据MIT许可证授权

# 这个模块包含了社区报告生成的实用工具

# 定义一个函数，计算上下文（context）中的单词数
def set_context_size(df: pd.DataFrame) -> None:
    """测量每个上下文有多少个单词。"""
    # 在数据框中新增一列，存储每个上下文的单词数
    df[schemas.CONTEXT_SIZE] = df[schemas.CONTEXT_STRING].apply(lambda x: num_tokens(x))  # 应用函数计算单词数

# 定义一个函数，设置标志来表示上下文是否超过限制
def set_context_exceeds_flag(df: pd.DataFrame, max_tokens: int) -> None:
    """如果上下文超过最大单词数，设置一个标记。"""
    # 新增一列，如果上下文单词数大于最大值，则该列值为True，否则为False
    df[schemas.CONTEXT_EXCEED_FLAG] = df[schemas.CONTEXT_SIZE].apply(lambda x: x > max_tokens)

# 定义一个函数，获取社区的层级列表
def get_levels(df: pd.DataFrame, level_column: str = schemas.NODE_LEVEL) -> list[int]:
    """获取社区的各个层级。"""
    # 排序并去除重复的层级值，将-1排除在外
    result = sorted(df[level_column].fillna(-1).unique().tolist(), reverse=True)
    # 返回不等于-1的层级值列表
    return [r for r in result if r != -1]

# 定义一个函数，筛选出特定层级的节点
def filter_nodes_to_level(node_df: pd.DataFrame, level: int) -> pd.DataFrame:
    """筛选出处于指定层级的节点。"""
    # 返回节点数据框中层级等于给定层级的行
    return cast(pd.DataFrame, node_df[node_df[schemas.NODE_LEVEL] == level])

# 定义一个函数，筛选出与给定节点相关的边
def filter_edges_to_nodes(edge_df: pd.DataFrame, nodes: list[str]) -> pd.DataFrame:
    """筛选出源节点和目标节点都在给定节点列表中的边。"""
    # 返回边数据框中源节点和目标节点都存在于给定节点列表中的行
    return cast(
        pd.DataFrame,
        edge_df[
            edge_df[schemas.EDGE_SOURCE].isin(nodes)
            & edge_df[schemas.EDGE_TARGET].isin(nodes)
        ],
    )

# 定义一个函数，筛选出与给定节点相关的主张（claims）
def filter_claims_to_nodes(claims_df: pd.DataFrame, nodes: list[str]) -> pd.DataFrame:
    """筛选出主题节点在给定节点列表中的主张。"""
    # 返回主张数据框中主张主题存在于给定节点列表中的行
    return cast(
        pd.DataFrame,
        claims_df[claims_df[schemas.CLAIM_SUBJECT].isin(nodes)],
    )

