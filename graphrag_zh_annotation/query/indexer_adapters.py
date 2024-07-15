# 导入必要的模块，让Python知道我们要用什么工具
from typing import cast  # 类型转换工具
import pandas as pd  # 数据处理库

# 从graphrag.model导入我们需要的数据模型类
from graphrag.model import CommunityReport, Covariate, Entity, Relationship, TextUnit

# 从graphrag.query.input.loaders.dfs导入数据读取函数
from graphrag.query.input.loaders.dfs import (
    read_community_reports,
    read_covariates,
    read_entities,
    read_relationships,
    read_text_units,
)

# 这是代码的作者和许可信息，表示这个代码由微软公司创作，遵循MIT许可证
# """Indexing-Engine to Query Read Adapters.

# 这段文字说明了这些函数的作用，它们可能最终会简化，直接将数据读入对象模型。
# """

# 定义一个函数，用于读取文本单元
def read_indexer_text_units(final_text_units: pd.DataFrame) -> list[TextUnit]:
    """从原始索引输出中读取文本单元数据。"""
    # 使用特定的函数处理数据框，并传入参数
    return read_text_units(
        df=final_text_units,  # 传入数据框
        short_id_col=None,  # 指定短ID列（这里没有）
        covariates_col=None,  # 指定协变量列（这里没有）
    )

# 定义一个函数，用于读取协变量（比如索赔数据）
def read_indexer_covariates(final_covariates: pd.DataFrame) -> list[Covariate]:
    """从原始索引输出中读取协变量（比如索赔）数据。"""
    # 处理协变量数据框，将"id"列转为字符串类型
    covariate_df = final_covariates
    covariate_df["id"] = covariate_df["id"].astype(str)
    # 使用特定的函数处理数据框，并传入参数
    return read_covariates(
        df=covariate_df,  # 传入处理后的数据框
        short_id_col="human_readable_id",  # 指定人类可读的ID列
        attributes_cols=[  # 指定其他属性列
            "object_id",
            "status",
            "start_date",
            "end_date",
            "description",
        ],
        text_unit_ids_col=None,  # 指定文本单元ID列（这里没有）
    )

# 定义一个函数read_indexer_relationships，它接收一个名为final_relationships的数据框（DataFrame类型）
def read_indexer_relationships(final_relationships: pd.DataFrame) -> list[Relationship]:
    """这个函数用来读取原始索引输出中的关系信息."""
    # 调用另一个函数read_relationships，传入参数
    # df是final_relationships数据框，short_id_col指定的列是"human_readable_id"
    # description_embedding_col和document_ids_col没有指定值，设为None
    # attributes_cols包含的列是"rank"
    return read_relationships(
        df=final_relationships,
        short_id_col="human_readable_id",
        description_embedding_col=None,
        document_ids_col=None,
        attributes_cols=["rank"],
    )

# 定义一个函数read_indexer_reports，它接收3个参数：final_community_reports数据框，final_nodes数据框和community_level整数
def read_indexer_reports(
    final_community_reports: pd.DataFrame,
    final_nodes: pd.DataFrame,
    community_level: int,
) -> list[CommunityReport]:
    """这个函数用来从原始索引输出中读取社区报告."""
    
    # 将final_community_reports赋值给变量report_df
    report_df = final_community_reports
    # 将final_nodes赋值给变量entity_df
    entity_df = final_nodes

    # 调用一个内部函数，过滤entity_df中低于community_level的行
    entity_df = _filter_under_community_level(entity_df, community_level)

    # 填充entity_df中"community"列的缺失值为-1
    entity_df["community"] = entity_df["community"].fillna(-1)
    # 将"community"列转换为整数类型
    entity_df["community"] = entity_df["community"].astype(int)

    # 按"title"列对entity_df进行分组，取"community"列的最大值，然后重置索引
    entity_df = entity_df.groupby(["title"]).agg({"community": "max"}).reset_index()
    # 将"community"列转换为字符串类型
    entity_df["community"] = entity_df["community"].astype(str)

    # 获取"community"列的唯一值
    filtered_community_df = entity_df["community"].drop_duplicates()

    # 对report_df应用相同的过滤操作，过滤低于community_level的行
    report_df = _filter_under_community_level(report_df, community_level)
    # 使用inner连接方式，将report_df与filtered_community_df按"community"列合并
    report_df = report_df.merge(filtered_community_df, on="community", how="inner")

    # 调用read_community_reports函数，传入参数
    # df是处理后的report_df，id_col和short_id_col都是"community"
    # summary_embedding_col和content_embedding_col没有指定值，设为None
    return read_community_reports(
        df=report_df,
        id_col="community",
        short_id_col="community",
        summary_embedding_col=None,
        content_embedding_col=None,
    )

# 定义一个函数read_indexer_entities，它接受3个参数：final_nodes（数据框），final_entities（数据框）和community_level（整数）
def read_indexer_entities(
    final_nodes: pd.DataFrame,  # 这是关于节点的信息
    final_entities: pd.DataFrame,  # 这是关于实体的信息
    community_level: int,  # 这是我们关心的社区级别
) -> list[Entity]:  # 函数返回一个实体列表

    # 将final_nodes赋值给entity_df
    entity_df = final_nodes
    # 将final_entities赋值给entity_embedding_df
    entity_embedding_df = final_entities

    # 根据community_level过滤entity_df
    entity_df = _filter_under_community_level(entity_df, community_level)
    
    # 转换并重命名entity_df的列
    entity_df = cast(pd.DataFrame, entity_df[["title", "degree", "community"]]).rename(
        columns={"title": "name", "degree": "rank"}
    )

    # 将community列中缺失的值填充为-1
    entity_df["community"] = entity_df["community"].fillna(-1)
    # 将community列转换为整数类型
    entity_df["community"] = entity_df["community"].astype(int)
    # 将rank列转换为整数类型
    entity_df["rank"] = entity_df["rank"].astype(int)

    # 对于重复的实体，保留社区级别最高的那个
    entity_df = (
        entity_df.groupby(["name", "rank"]).agg({"community": "max"}).reset_index()
    )
    # 将community列的值转换为字符串列表
    entity_df["community"] = entity_df["community"].apply(lambda x: [str(x)])
    # 根据"name"列与entity_embedding_df合并数据，并删除重复的"name"列
    entity_df = entity_df.merge(
        entity_embedding_df, on="name", how="inner"
    ).drop_duplicates(subset=["name"])

    # 将处理后的数据框转换为知识模型对象列表并返回
    return read_entities(
        df=entity_df,  # 输入数据框
        id_col="id",  # ID列名
        title_col="name",  # 标题列名
        type_col="type",  # 类型列名
        short_id_col="human_readable_id",  # 简短ID列名
        description_col="description",  # 描述列名
        community_col="community",  # 社区列名
        rank_col="rank",  # 排名列名
        name_embedding_col=None,  # 名称嵌入列名
        description_embedding_col="description_embedding",  # 描述嵌入列名
        graph_embedding_col=None,  # 图嵌入列名
        text_unit_ids_col="text_unit_ids",  # 文本单元ID列名
        document_ids_col=None,  # 文档ID列名
    )

# 定义一个辅助函数_filter_under_community_level，用于过滤低于指定社区级别的行
def _filter_under_community_level(
    df: pd.DataFrame,  # 输入数据框
    community_level: int,  # 指定的社区级别
) -> pd.DataFrame:  # 返回过滤后的数据框
    # 返回level列不大于community_level的行
    return cast(
        pd.DataFrame,
        df[df.level <= community_level],
    )

