# 导入一些工具库，让我们的代码能处理数据和计算
from collections import defaultdict  # 用于创建默认值的字典
from typing import Any, cast  # 类型检查，帮助我们确保数据类型正确
import pandas as pd  # 用于处理表格数据
import tiktoken  # 可能是一个处理文本或令牌的库

# 引入模型和查询相关模块
from graphrag.model import Covariate, Entity, Relationship  # 定义了三种数据类型：协变量、实体和关系
from graphrag.query.input.retrieval.covariates import (
    get_candidate_covariates,  # 获取可能的协变量
    to_covariate_dataframe,  # 将协变量转换成表格形式
)
from graphrag.query.input.retrieval.entities import to_entity_dataframe  # 将实体转换成表格形式
from graphrag.query.input.retrieval.relationships import (
    get_candidate_relationships,  # 获取可能的关系
    get_entities_from_relationships,  # 从关系中获取实体
    get_in_network_relationships,  # 获取网络内的关系
    get_out_network_relationships,  # 获取网络外的关系
    to_relationship_dataframe,  # 将关系转换成表格形式
)
from graphrag.query.llm.text_utils import num_tokens  # 用于计算文本中的令牌数量

# 版权信息，这个代码是微软公司2024年的作品，遵循MIT许可证

# 这个文件是用来构建局部上下文的
# 我们将使用上述导入的工具和函数来处理数据，比如协变量、实体和它们之间的关系

# 定义一个函数，叫做 build_entity_context，它接收一些参数
def build_entity_context(
    selected_entities: list[Entity],  # 一个包含实体（Entity）的列表
    token_encoder: tiktoken.Encoding | None = None,  # 用于编码的工具，可能是某种编码器，也可能没有
    max_tokens: int = 8000,  # 最大允许的字符数
    include_entity_rank: bool = True,  # 是否包含实体的排名
    rank_description: str = "number of relationships",  # 排名的描述
    column_delimiter: str = "|",  # 列之间的分隔符，默认是竖线 |
    context_name="Entities",  # 上下文名称，默认是"Entities"
) -> tuple[str, pd.DataFrame]:  # 函数返回一个字符串和一个数据框

    """这个函数用来准备实体数据表作为系统提示的上下文信息。"""

    # 如果没有选择任何实体，就返回空字符串和空数据框
    if len(selected_entities) == 0:
        return "", pd.DataFrame()

    # 添加标题行
    current_context_text = f"-----{context_name}-----" + "\n"  # 创建一个标题，比如 "-----Entities-----"
    header = ["id", "entity", "description"]  # 表头：id、实体、描述

    # 如果要包含排名
    if include_entity_rank:
        header.append(rank_description)  # 将排名描述添加到表头

    # 获取第一个实体的属性键，如果没有属性则为空列表
    attribute_cols = (
        list(selected_entities[0].attributes.keys())
        if selected_entities[0].attributes
        else []
    )

    # 将属性键添加到表头
    header.extend(attribute_cols)
    current_context_text += column_delimiter.join(header) + "\n"  # 将表头连接成一行并添加到文本中

    # 计算当前文本的字符数
    current_tokens = num_tokens(current_context_text, token_encoder)

    # 初始化一个记录列表，存放数据框的行
    all_context_records = [header]

    # 遍历所有实体
    for entity in selected_entities:
        # 创建一行数据
        new_context = [
            entity.short_id if entity.short_id else "",  # 实体的简短ID，如果没有则为空
            entity.title,  # 实体的标题
            entity.description if entity.description else "",  # 实体的描述，如果没有则为空
        ]

        # 如果要包含排名
        if include_entity_rank:
            new_context.append(str(entity.rank))  # 添加实体的排名

        # 遍历属性列，添加属性值
        for field in attribute_cols:
            field_value = (
                str(entity.attributes.get(field))
                if entity.attributes and entity.attributes.get(field)
                else ""
            )
            new_context.append(field_value)  # 将属性值添加到数据行中

        # 将新的一行数据连接成文本并计算字符数
        new_context_text = column_delimiter.join(new_context) + "\n"
        new_tokens = num_tokens(new_context_text, token_encoder)

        # 如果当前字符数加上新行的字符数超过最大值，停止添加
        if current_tokens + new_tokens > max_tokens:
            break

        # 将新行数据添加到文本和记录列表中
        current_context_text += new_context_text
        all_context_records.append(new_context)
        current_tokens += new_tokens

    # 如果有至少两行数据，创建数据框
    if len(all_context_records) > 1:
        record_df = pd.DataFrame(
            all_context_records[1:], columns=cast(Any, all_context_records[0])
        )
    else:
        record_df = pd.DataFrame()  # 否则，创建一个空的数据框

    # 返回最终的文本和数据框
    return current_context_text, record_df



# 定义一个名为build_covariates_context的函数，它接受四个参数：选定的实体列表、协变量列表、编码器（可选）和最大令牌数
def build_covariates_context(
    selected_entities: list[Entity],  # 输入的实体列表
    covariates: list[Covariate],  # 输入的协变量列表
    token_encoder: tiktoken.Encoding | None = None,  # 编码器，默认为None
    max_tokens: int = 8000,  # 最大允许的令牌数，默认是8000
    column_delimiter: str = "|",  # 列分隔符，默认是"|"
    context_name: str = "Covariates",  # 上下文名称，默认是"Covariates"
) -> tuple[str, pd.DataFrame]:  # 返回一个包含文本和数据框的元组

    # 如果没有选定的实体或协变量，返回空字符串和空数据框
    if len(selected_entities) == 0 or len(covariates) == 0:
        return "", pd.DataFrame()

    # 创建一个空的协变量列表
    selected_covariates = list[Covariate]()

    # 创建一个空的数据框
    record_df = pd.DataFrame()

    # 添加上下文标题
    current_context_text = f"-----{context_name}-----" + "\n"

    # 添加列头
    header = ["id", "entity"]  # 初始化列头
    # 获取第一个协变量的属性，如果没有协变量，则为空字典
    attributes = covariates[0].attributes or {} if len(covariates) > 0 else {}
    # 获取属性列名
    attribute_cols = list(attributes.keys()) if len(covariates) > 0 else []
    # 将属性列名添加到列头
    header.extend(attribute_cols)
    # 将列头连接成字符串并添加到上下文文本
    current_context_text += column_delimiter.join(header) + "\n"
    # 计算当前上下文文本的令牌数
    current_tokens = num_tokens(current_context_text, token_encoder)

    # 初始化所有上下文记录列表
    all_context_records = [header]

    # 遍历选定的实体，将与之匹配的协变量添加到selected_covariates列表
    for entity in selected_entities:
        selected_covariates.extend([
            cov for cov in covariates if cov.subject_id == entity.title
        ])

    # 遍历选定的协变量
    for covariate in selected_covariates:
        # 初始化新的上下文内容
        new_context = [
            covariate.short_id if covariate.short_id else "",
            covariate.subject_id,
        ]
        # 遍历属性列名，获取属性值并添加到新上下文内容
        for field in attribute_cols:
            field_value = (
                str(covariate.attributes.get(field))
                if covariate.attributes and covariate.attributes.get(field)
                else ""
            )
            new_context.append(field_value)

        # 将新上下文内容连接成字符串并添加换行符
        new_context_text = column_delimiter.join(new_context) + "\n"
        # 计算新上下文文本的令牌数
        new_tokens = num_tokens(new_context_text, token_encoder)
        # 如果当前令牌数加上新令牌数超过最大令牌数，停止添加
        if current_tokens + new_tokens > max_tokens:
            break
        # 将新上下文文本添加到当前上下文文本
        current_context_text += new_context_text
        # 将新上下文内容添加到所有上下文记录列表
        all_context_records.append(new_context)
        # 更新当前令牌数
        current_tokens += new_tokens

        # 如果有多个记录，创建数据框
        if len(all_context_records) > 1:
            record_df = pd.DataFrame(
                all_context_records[1:], columns=cast(Any, all_context_records[0])
            )
        # 否则，创建空数据框
        else:
            record_df = pd.DataFrame()

    # 返回当前上下文文本和数据框
    return current_context_text, record_df







# 定义一个函数_filter_relationships，它接受四个参数：
# selected_entities：一个实体列表
# relationships：一个关系列表
# top_k_relationships：默认为10，表示要返回的最高优先级关系数量
# relationship_ranking_attribute：默认为"rank"，用于排序关系的属性名

def _filter_relationships(
    selected_entities: list[Entity],
    relationships: list[Relationship],
    top_k_relationships: int = 10,
    relationship_ranking_attribute: str = "rank",
) -> list[Relationship]:
    """根据选定的实体和排序属性过滤并排序关系。"""

    # 首先，找出网络内的关系（即，选定实体之间）
    in_network_relationships = get_in_network_relationships(
        selected_entities=selected_entities,
        relationships=relationships,
        ranking_attribute=relationship_ranking_attribute,
    )

    # 其次，找出网络外的关系（即，选定实体与其他不在选定实体中的实体之间的关系）
    out_network_relationships = get_out_network_relationships(
        selected_entities=selected_entities,
        relationships=relationships,
        ranking_attribute=relationship_ranking_attribute,
    )

    # 如果网络外的关系少于或等于1个，直接将它们与网络内关系合并后返回
    if len(out_network_relationships) <= 1:
        return in_network_relationships + out_network_relationships

    # 在网络外的关系中，优先考虑相互关系（即，与多个选定实体共享的外部实体）
    selected_entity_names = [entity.title for entity in selected_entities]
    out_network_source_names = [
        relationship.source
        for relationship in out_network_relationships
        if relationship.source not in selected_entity_names
    ]
    out_network_target_names = [
        relationship.target
        for relationship in out_network_relationships
        if relationship.target not in selected_entity_names
    ]
    out_network_entity_names = list(
        set(out_network_source_names + out_network_target_names)
    )
    out_network_entity_links = defaultdict(int)  # 初始化一个字典，用于存储每个外部实体的连接数

    # 计算每个外部实体的连接数
    for entity_name in out_network_entity_names:
        targets = [
            relationship.target
            for relationship in out_network_relationships
            if relationship.source == entity_name
        ]
        sources = [
            relationship.source
            for relationship in out_network_relationships
            if relationship.target == entity_name
        ]
        out_network_entity_links[entity_name] = len(set(targets + sources))

    # 将网络外的关系按连接数和排名属性进行排序
    for rel in out_network_relationships:
        # 给关系添加一个名为"links"的属性，如果关系没有属性，就创建一个空字典
        if rel.attributes is None:
            rel.attributes = {}
        # 设置"links"属性的值，取来源或目标的连接数，哪个存在就用哪个
        rel.attributes["links"] = (
            out_network_entity_links[rel.source]
            if rel.source in out_network_entity_links
            else out_network_entity_links[rel.target]
        )

    # 根据"links"属性和排名属性对关系进行排序，先按连接数，然后按排名属性
    # 如果排名属性是"weight"，则按降序排列
    if relationship_ranking_attribute == "weight":
        out_network_relationships.sort(
            key=lambda x: (x.attributes["links"], x.weight),  # 忽略类型检查
            reverse=True,  # 忽略类型检查
        )
    # 否则，按指定的排名属性进行降序排列
    else:
        out_network_relationships.sort(
            key=lambda x: (
                x.attributes["links"],  # 忽略类型检查
                x.attributes[relationship_ranking_attribute],  # 忽略类型检查
            ),  # 忽略类型检查
            reverse=True,
        )

    # 计算可返回的关系预算，等于top_k_relationships乘以选定实体的数量
    relationship_budget = top_k_relationships * len(selected_entities)

    # 最后，返回网络内关系加上预算范围内的网络外关系
    return in_network_relationships + out_network_relationships[:relationship_budget]

# 定义一个名为get_candidate_context的函数，它需要一些参数：
# selected_entities: 已选择的实体列表
# entities: 所有实体列表
# relationships: 关系列表
# covariates: 各种协变量（变量）的字典，每个键是协变量的名称，值是协变量的列表
# include_entity_rank: 是否包含实体的排名，默认为True
# entity_rank_description: 描述实体排名的字符串，默认为"number of relationships"
# include_relationship_weight: 是否包含关系权重，默认为False

# 这个函数的目的是准备实体、关系和协变量的数据表作为系统提示的上下文数据

def get_candidate_context(
    selected_entities: list[Entity],
    entities: list[Entity],
    relationships: list[Relationship],
    covariates: dict[str, list[Covariate]],
    include_entity_rank: bool = True,
    entity_rank_description: str = "number of relationships",
    include_relationship_weight: bool = False,
) -> dict[str, pd.DataFrame]:
    # 创建一个空字典来存储结果数据
    candidate_context = {}

    # 获取与已选择实体相关的候选关系
    candidate_relationships = get_candidate_relationships(
        selected_entities=selected_entities,
        relationships=relationships,
    )

    # 将候选关系转换为数据框并添加到候选上下文中
    candidate_context["relationships"] = to_relationship_dataframe(
        relationships=candidate_relationships,
        include_relationship_weight=include_relationship_weight,
    )

    # 从候选关系中获取相关的候选实体
    candidate_entities = get_entities_from_relationships(
        relationships=candidate_relationships, entities=entities
    )

    # 将候选实体转换为数据框并添加到候选上下文中
    candidate_context["entities"] = to_entity_dataframe(
        entities=candidate_entities,
        include_entity_rank=include_entity_rank,
        rank_description=entity_rank_description,
    )

    # 遍历协变量字典中的每一个协变量
    for covariate in covariates:
        # 获取与已选择实体相关的候选协变量
        candidate_covariates = get_candidate_covariates(
            selected_entities=selected_entities,
            covariates=covariates[covariate],
        )

        # 将候选协变量转换为数据框并添加到候选上下文中，以协变量名称为键
        candidate_context[covariate.lower()] = to_covariate_dataframe(
            candidate_covariates
        )

    # 返回包含所有准备好的数据的候选上下文字典
    return candidate_context

