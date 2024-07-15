# 导入必要的工具，让Python知道我们将会用到的类型和库
from typing import Any, cast  # 这些是关于数据类型的工具，帮助我们确保代码的准确性
import pandas as pd  # pandas库，用于处理表格数据
from graphrag.model import Entity, Relationship  # 从graphrag.model导入两个类：Entity和Relationship

# 这段文字是版权信息，告诉我们这个代码是由微软公司创建的，使用的是MIT许可证

# 定义一个有用的函数，用来从一组关系中获取选定实体之间的连接
def get_in_network_relationships(  # 输入两个列表和一个字符串
    selected_entities: list[Entity],  # 一个包含Entity对象的列表，代表选定的实体
    relationships: list[Relationship],  # 一个包含Relationship对象的列表，代表所有关系
    ranking_attribute: str = "rank",  # 一个字符串，默认值为"rank"，用于排序关系
) -> list[Relationship]:  # 函数返回一个按排名排序的Relationship对象列表

    # 获取选定实体的名称列表
    selected_entity_names = [entity.title for entity in selected_entities]

    # 找出源和目标都在选定实体列表中的关系
    selected_relationships = [
        relationship
        for relationship in relationships
        if relationship.source in selected_entity_names  # 检查关系的起点
        and relationship.target in selected_entity_names  # 检查关系的终点
    ]

    # 如果找到的关系少于或等于1个，直接返回这些关系
    if len(selected_relationships) <= 1:
        return selected_relationships

    # 根据指定的排名属性对关系进行排序
    return sort_relationships_by_ranking_attribute(
        selected_relationships, selected_entities, ranking_attribute
    )  # 调用另一个函数来完成排序，然后返回排序后的关系列表

# 定义一个函数，获取选定实体之间的外部网络关系，按指定属性排序
def get_out_network_relationships(
    selected_entities: list[Entity],  # 输入的选定实体列表
    relationships: list[Relationship],  # 输入的关系列表
    ranking_attribute: str = "rank",  # 排序依据的属性，默认是"rank"
) -> list[Relationship]:  # 返回值类型为关系列表
    """获取从选定实体到其他未选中实体的关系，按ranking_attribute排序"""
    # 获取选定实体的名称列表
    selected_entity_names = [entity.title for entity in selected_entities]
    
    # 找出源实体在选定实体中，目标实体不在选定实体中的关系
    source_relationships = [
        relationship
        for relationship in relationships
        if relationship.source in selected_entity_names
        and relationship.target not in selected_entity_names
    ]
    
    # 找出目标实体在选定实体中，源实体不在选定实体中的关系
    target_relationships = [
        relationship
        for relationship in relationships
        if relationship.target in selected_entity_names
        and relationship.source not in selected_entity_names
    ]
    
    # 合并两种关系列表
    selected_relationships = source_relationships + target_relationships
    
    # 按照指定属性对关系列表进行排序并返回
    return sort_relationships_by_ranking_attribute(
        selected_relationships, selected_entities, ranking_attribute
    )

# 定义一个函数，获取与选定实体相关的所有关系
def get_candidate_relationships(
    selected_entities: list[Entity],  # 输入的选定实体列表
    relationships: list[Relationship],  # 输入的关系列表
) -> list[Relationship]:  # 返回值类型为关系列表
    """获取所有与选定实体相关联的关系"""
    # 获取选定实体的名称列表
    selected_entity_names = [entity.title for entity in selected_entities]
    
    # 找出源实体或目标实体在选定实体中的关系
    return [
        relationship
        for relationship in relationships
        if relationship.source in selected_entity_names
        or relationship.target in selected_entity_names
    ]

# 定义一个函数，从关系列表中获取相关实体
def get_entities_from_relationships(
    relationships: list[Relationship],  # 输入的关系列表
    entities: list[Entity],  # 输入的实体列表
) -> list[Entity]:  # 返回值类型为实体列表
    """获取与选定关系相关联的所有实体"""
    # 获取所有关系的源和目标实体名称
    selected_entity_names = [relationship.source for relationship in relationships] + [
        relationship.target for relationship in relationships
    ]
    
    # 找出名称在选定实体名称列表中的实体
    return [entity for entity in entities if entity.title in selected_entity_names]

# 定义一个名为calculate_relationship_combined_rank的函数，它接收三个参数
# 1. 一个Relationship类型的列表（关系列表）
# 2. 一个Entity类型的列表（实体列表）
# 3. 一个默认字符串"rank"（排名属性）

def calculate_relationship_combined_rank(
    relationships: list[Relationship],
    entities: list[Entity],
    ranking_attribute: str = "rank",
) -> list[Relationship]:
    """这个函数用来根据源实体和目标实体的组合排名，计算关系的默认排名。"""

    # 创建一个字典，键是实体的名称，值是实体本身
    entity_mappings = {entity.title: entity for entity in entities}

    # 遍历每一个关系
    for relationship in relationships:
        # 如果关系的属性为空，就给它一个空字典
        if relationship.attributes is None:
            relationship.attributes = {}

        # 尝试从实体映射中找到关系的源实体
        source = entity_mappings.get(relationship.source)
        # 尝试从实体映射中找到关系的目标实体
        target = entity_mappings.get(relationship.target)

        # 如果源实体存在且有排名，就取其排名，否则设为0
        source_rank = source.rank if source and source.rank else 0
        # 如果目标实体存在且有排名，就取其排名，否则设为0
        target_rank = target.rank if target and target.rank else 0

        # 把源实体和目标实体排名相加，保存到关系的属性中，指定的属性名为ranking_attribute
        relationship.attributes[ranking_attribute] = source_rank + target_rank  # type: ignore

    # 最后，返回处理过的关系列表
    return relationships

# 定义一个函数，名为sort_relationships_by_ranking_attribute，它接受三个参数
# relationships：一个列表，包含 Relationship 类型的对象
# entities：一个列表，包含 Entity 类型的对象
# ranking_attribute：一个字符串，表示我们要根据哪个属性进行排序，默认值是 "rank"

def sort_relationships_by_ranking_attribute(
    relationships: list[Relationship],
    entities: list[Entity],
    ranking_attribute: str = "rank",
) -> list[Relationship]:
    """
    根据 ranking_attribute 对关系进行排序。

    如果没有排名属性，就按照源和目标实体的组合排名进行排序。
    """
    # 如果关系列表为空，直接返回原列表
    if len(relationships) == 0:
        return relationships

    # 首先尝试按 ranking_attribute 排序
    # 获取关系的第一个对象的属性键列表
    attribute_names = (
        list(relationships[0].attributes.keys()) if relationships[0].attributes else []
    )
    # 如果 ranking_attribute 在属性键列表中
    if ranking_attribute in attribute_names:
        # 使用 lambda 函数作为排序键，将关系按 ranking_attribute 的数值（转换为整数）降序排列
        relationships.sort(
            key=lambda x: int(x.attributes[ranking_attribute]) if x.attributes else 0,
            reverse=True,
        )
    # 如果 ranking_attribute 是 "weight"
    elif ranking_attribute == "weight":
        # 按照关系的权重（如果存在）降序排列
        relationships.sort(key=lambda x: x.weight if x.weight else 0.0, reverse=True)
    else:
        # ranking_attribute 不存在，计算综合排名
        relationships = calculate_relationship_combined_rank(
            relationships, entities, ranking_attribute
        )
        # 按照计算出的 ranking_attribute 值（转换为整数）降序排列
        relationships.sort(
            key=lambda x: int(x.attributes[ranking_attribute]) if x.attributes else 0,
            reverse=True,
        )

    # 返回排序后的关系列表
    return relationships

# 定义一个函数，名为to_relationship_dataframe，它接受一个Relationship类型的列表和一个布尔值
def to_relationship_dataframe(
    relationships: list[Relationship], include_relationship_weight: bool = True
) -> pd.DataFrame:
    """这个函数的作用是把一系列的关系转换成一个pandas数据框（表格）"""
    
    # 如果关系列表为空，返回一个空的数据框
    if len(relationships) == 0:
        return pd.DataFrame()

    # 初始化表头，包含id, source, target, description
    header = ["id", "source", "target", "description"]
    
    # 如果include_relationship_weight为真，添加"weight"到表头
    if include_relationship_weight:
        header.append("weight")

    # 获取第一个关系对象的属性键，如果没有属性则为空列表
    attribute_cols = (
        list(relationships[0].attributes.keys()) if relationships[0].attributes else []
    )

    # 过滤出不在表头中的属性列
    attribute_cols = [col for col in attribute_cols if col not in header]
    
    # 将属性列添加到表头
    header.extend(attribute_cols)

    # 初始化一个空的记录列表，用于存储每一行的数据
    records = []

    # 遍历每一个关系
    for rel in relationships:
        # 创建新记录，包含id, source, target, description
        new_record = [
            rel.short_id if rel.short_id else "",  # id，如果有的话
            rel.source,  # 来源
            rel.target,  # 目标
            rel.description if rel.description else "",  # 描述，如果有的话
        ]

        # 如果包含权重，添加权重到新记录
        if include_relationship_weight:
            new_record.append(str(rel.weight if rel.weight else ""))

        # 遍历属性列，添加属性值到新记录，如果属性存在则转为字符串，否则为空
        for field in attribute_cols:
            field_value = (
                str(rel.attributes.get(field))
                if rel.attributes and rel.attributes.get(field)
                else ""
            )
            new_record.append(field_value)
        
        # 将新记录添加到记录列表
        records.append(new_record)

    # 使用记录列表创建数据框并返回，将header转换为Any类型以匹配返回类型
    return pd.DataFrame(records, columns=cast(Any, header))

