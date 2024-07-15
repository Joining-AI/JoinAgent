# 导入logging模块，它用于记录程序运行时的信息
import logging

# 使用typing模块中的cast函数，帮助类型转换
from typing import cast

# 导入pandas库，这是一个用于数据处理的库
import pandas as pd

# 导入图相关的报告模式（schemas）
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 从graphrag库中导入一些数据框操作函数
from graphrag.index.utils.dataframes import (
    antijoin,  # 取两个数据框的非交集
    drop_columns,  # 删除数据框中的列
    join,  # 合并数据框
    select,  # 选择数据框中的特定列
    transform_series,  # 转换数据框中的序列
    union,  # 合并多个数据框
    where_column_equals,  # 根据某一列的值筛选数据框
)

# 导入混合上下文构建函数
from .build_mixed_context import build_mixed_context

# 导入上下文排序函数
from .sort_context import sort_context

# 导入设置上下文大小的辅助函数
from .utils import set_context_size

# 这段文字是模块的文档字符串，描述了模块的功能
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为log的变量，它是logging模块的日志记录器，用于记录程序信息
log = logging.getLogger(__name__)

# 定义一个名为prep_community_report_context的函数，它接受5个参数
def prep_community_report_context(
    report_df: pd.DataFrame | None,  # 第一个参数是可能为None的pandas数据框，用于存放报告
    community_hierarchy_df: pd.DataFrame,  # 第二个参数是社区层级的数据框
    local_context_df: pd.DataFrame,  # 第三个参数是本地上下文的数据框
    level: int | str,  # 第四个参数是层级，可以是整数或字符串
    max_tokens: int,  # 第五个参数是最大允许的令牌（单词）数量
) -> pd.DataFrame:  # 函数返回一个pandas数据框

    """
    函数的作用是为给定层级的每个社区准备上下文。

    对于每个社区：
    - 检查本地上下文是否在限制内，如果在，则使用本地上下文
    - 如果本地上下文超过限制，从最大的子社区开始，逐步用子社区报告替换
    """

    # 如果report_df为空，就创建一个新的空数据框
    if report_df is None:
        report_df = pd.DataFrame()

    # 将level转换为整数
    level = int(level)
    # 获取指定层级的本地上下文数据框
    level_context_df = _at_level(level, local_context_df)
    # 确定在限制内的上下文数据框
    valid_context_df = _within_context(level_context_df)
    # 确定超过限制的上下文数据框
    invalid_context_df = _exceeding_context(level_context_df)

    # 如果没有需要替换的上下文记录（即invalid_context_df为空），直接返回valid_context_df
    # 这种情况通常发生在社区层级的最底部，没有子社区
    if invalid_context_df.empty:
        return valid_context_df

    # 如果report_df为空，处理invalid_context_df并返回结果
    if report_df.empty:
        # 对invalid_context_df中的上下文进行排序和截断
        invalid_context_df[schemas.CONTEXT_STRING] = _sort_and_trim_context(
            invalid_context_df, max_tokens
        )
        # 设置上下文大小
        set_context_size(invalid_context_df)
        # 设置超出标志为0
        invalid_context_df[schemas.CONTEXT_EXCEED_FLAG] = 0
        # 合并valid_context_df和invalid_context_df并返回
        return union(valid_context_df, invalid_context_df)

    # 移除level_context_df中已存在于report_df的数据
    level_context_df = _antijoin_reports(level_context_df, report_df)

    # 获取每个子社区的本地上下文和报告
    sub_context_df = _get_subcontext_df(level + 1, report_df, local_context_df)
    # 创建包含无效上下文及其子社区信息的社区数据框
    community_df = _get_community_df(
        level, invalid_context_df, sub_context_df, community_hierarchy_df, max_tokens
    )

    # 处理无法用子社区报告替换的剩余无效记录
    # 截断这些记录的本地上下文以适应限制
    remaining_df = _antijoin_reports(invalid_context_df, community_df)
    remaining_df[schemas.CONTEXT_STRING] = _sort_and_trim_context(
        remaining_df, max_tokens
    )

    # 合并所有结果数据框
    result = union(valid_context_df, community_df, remaining_df)
    # 设置结果数据框中上下文的大小
    set_context_size(result)
    # 设置超出标志为0
    result[schemas.CONTEXT_EXCEED_FLAG] = 0
    # 返回结果数据框
    return result

# 定义一个函数，从数据框中移除名为"社区级别"的列
def _drop_community_level(df: pd.DataFrame) -> pd.DataFrame:
    """删除数据框中的'社区级别'列"""
    return drop_columns(df, schemas.COMMUNITY_LEVEL)

# 定义一个函数，返回指定级别记录的数据框
def _at_level(level: int, df: pd.DataFrame) -> pd.DataFrame:
    """返回级别为给定值的记录"""
    return where_column_equals(df, schemas.COMMUNITY_LEVEL, level)

# 定义一个函数，返回上下文超出限制的记录
def _exceeding_context(df: pd.DataFrame) -> pd.DataFrame:
    """返回上下文超出限制的记录"""
    return where_column_equals(df, schemas.CONTEXT_EXCEED_FLAG, 1)

# 定义一个函数，返回上下文在限制内的记录
def _within_context(df: pd.DataFrame) -> pd.DataFrame:
    """返回上下文在限制内的记录"""
    return where_column_equals(df, schemas.CONTEXT_EXCEED_FLAG, 0)

# 定义一个函数，返回数据框df中不在reports数据框中的记录
def _antijoin_reports(df: pd.DataFrame, reports: pd.DataFrame) -> pd.DataFrame:
    """返回df中不在reports中的记录"""
    return antijoin(df, reports, schemas.NODE_COMMUNITY)

# 定义一个函数，对上下文进行排序并截断以适应最大令牌数
def _sort_and_trim_context(df: pd.DataFrame, max_tokens: int) -> pd.Series:
    """对上下文排序并截断以适应限制"""
    series = cast(pd.Series, df[schemas.ALL_CONTEXT])
    return transform_series(series, lambda x: sort_context(x, max_tokens=max_tokens))

# 定义一个函数，构建混合上下文，适应最大令牌数
def _build_mixed_context(df: pd.DataFrame, max_tokens: int) -> pd.Series:
    """创建混合上下文，适应最大令牌数"""
    series = cast(pd.Series, df[schemas.ALL_CONTEXT])
    return transform_series(
        series, lambda x: build_mixed_context(x, max_tokens=max_tokens)
    )

# 定义一个函数，为每个社区获取子社区上下文数据框
def _get_subcontext_df(
    level: int, report_df: pd.DataFrame, local_context_df: pd.DataFrame
) -> pd.DataFrame:
    """为每个社区获取子社区上下文"""
    # 获取指定级别的报告数据框
    sub_report_df = _drop_community_level(_at_level(level, report_df))
    # 获取指定级别的本地上下文数据框
    sub_context_df = _at_level(level, local_context_df)
    # 将两个数据框按'节点社区'列连接
    sub_context_df = join(sub_context_df, sub_report_df, schemas.NODE_COMMUNITY)
    # 重命名'节点社区'列为'SUB_COMMUNITY'
    sub_context_df.rename(columns={schemas.NODE_COMMUNITY: schemas.SUB_COMMUNITY}, inplace=True)
    # 返回结果数据框
    return sub_context_df

# 定义一个名为_get_community_df的函数，它需要5个参数：
# - level：一个整数，表示社区的级别
# - invalid_context_df：一个包含无效上下文的DataFrame（数据表格）
# - sub_context_df：一个包含子社区上下文的DataFrame
# - community_hierarchy_df：一个关于社区层级的DataFrame
# - max_tokens：一个整数，表示最大文本长度

def _get_community_df(
    level: int,
    invalid_context_df: pd.DataFrame,
    sub_context_df: pd.DataFrame,
    community_hierarchy_df: pd.DataFrame,
    max_tokens: int,
) -> pd.DataFrame:
    """获取每个社区的上下文信息。"""
    
    # 从社区层级数据中选取指定级别的社区
    community_df = _drop_community_level(_at_level(level, community_hierarchy_df))

    # 从无效上下文数据中选取社区ID
    invalid_community_ids = select(invalid_context_df, schemas.NODE_COMMUNITY)

    # 从子社区数据中选取需要的列
    subcontext_selection = select(
        sub_context_df,
        schemas.SUB_COMMUNITY,
        schemas.FULL_CONTENT,
        schemas.ALL_CONTEXT,
        schemas.CONTEXT_SIZE,
    )

    # 将无效社区ID与社区数据合并
    invalid_communities = join(
        community_df, invalid_community_ids, schemas.NODE_COMMUNITY, "inner"
    )

    # 将子社区数据与之前的结果合并
    community_df = join(
        invalid_communities, subcontext_selection, schemas.SUB_COMMUNITY
    )

    # 创建一个新的列，将所需信息整合成字典
    community_df[schemas.ALL_CONTEXT] = community_df.apply(
        lambda x: {
            schemas.SUB_COMMUNITY: x[schemas.SUB_COMMUNITY],
            schemas.ALL_CONTEXT: x[schemas.ALL_CONTEXT],
            schemas.FULL_CONTENT: x[schemas.FULL_CONTENT],
            schemas.CONTEXT_SIZE: x[schemas.CONTEXT_SIZE],
        },
        axis=1,
    )

    # 按社区ID分组，将所有上下文信息合并成列表
    community_df = (
        community_df.groupby(schemas.NODE_COMMUNITY)
        .agg({schemas.ALL_CONTEXT: list})
        .reset_index()
    )

    # 构建混合上下文字符串
    community_df[schemas.CONTEXT_STRING] = _build_mixed_context(
        community_df, max_tokens
    )

    # 添加列，记录社区的级别
    community_df[schemas.COMMUNITY_LEVEL] = level

    # 返回处理后的DataFrame
    return community_df

