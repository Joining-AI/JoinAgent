# 导入一个库，它能生成唯一的标识符
import uuid

# 导入一个Python内置的模块，用于检查是否可以迭代
from collections.abc import Iterable

# 导入Python的类型注解模块，用于更清晰地定义函数参数类型
from typing import Any, cast

# 导入pandas库，用于数据处理
import pandas as pd

# 从graphrag.model导入Entity类，可能是一个数据模型
from graphrag.model import Entity

# 这是微软公司的版权信息，表明代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含获取实体的实用函数
"""Util functions to get entities from a collection."""

# 定义一个函数，通过键值对获取实体
def get_entity_by_key(
    # 参数：一个可以迭代的实体列表，键的名称，以及键对应的价值（字符串或整数）
    entities: Iterable[Entity], key: str, value: str | int
) -> Entity | None:
    """根据键获取实体。"""
    # 遍历所有实体
    for entity in entities:
        # 如果值是字符串并且是有效的UUID（一种唯一标识）
        if isinstance(value, str) and is_valid_uuid(value):
            # 检查实体的属性与值是否匹配，或者去掉短横线后匹配
            if getattr(entity, key) == value or getattr(entity, key) == value.replace(
                "-", ""
            ):
                # 如果匹配，返回该实体
                return entity
        else:
            # 如果值不是字符串，直接检查实体的属性与值是否匹配
            if getattr(entity, key) == value:
                # 匹配则返回实体
                return entity
    # 如果没有找到匹配的实体，返回None
    return None


# 定义一个函数，通过名字获取实体列表
def get_entity_by_name(entities: Iterable[Entity], entity_name: str) -> list[Entity]:
    """根据名字获取实体列表。"""
    # 使用列表推导式，找出所有名字与给定名字相同的实体
    return [entity for entity in entities if entity.title == entity_name]


# 定义一个函数，通过属性名和属性值获取实体列表
def get_entity_by_attribute(
    entities: Iterable[Entity], attribute_name: str, attribute_value: Any
) -> list[Entity]:
    """根据属性获取实体列表。"""
    # 使用列表推导式，找出所有具有指定属性名且属性值相等的实体
    return [
        entity
        for entity in entities
        # 检查实体有属性，并且该属性的值等于给定的值
        if entity.attributes and entity.attributes.get(attribute_name) == attribute_value
    ]

# 定义一个名为to_entity_dataframe的函数，它接受一个实体列表（entities）、一个布尔值（include_entity_rank，默认为True）和一个字符串（rank_description，默认为"number of relationships"），返回一个Pandas数据框。
def to_entity_dataframe(
    entities: list[Entity],
    include_entity_rank: bool = True,
    rank_description: str = "number of relationships",
) -> pd.DataFrame:
    """将实体列表转换为Pandas数据框。"""
    # 如果实体列表为空，直接返回空数据框
    if len(entities) == 0:
        return pd.DataFrame()

    # 初始化列名，包含"id"、"entity"和"description"
    header = ["id", "entity", "description"]

    # 如果include_entity_rank为真，添加rank_description这一列
    if include_entity_rank:
        header.append(rank_description)

    # 获取第一个实体的属性键（如果有的话），否则为空列表
    attribute_cols = (
        list(entities[0].attributes.keys()) if entities[0].attributes else []
    )

    # 从属性键中移除已经存在于header中的列
    attribute_cols = [col for col in attribute_cols if col not in header]

    # 将属性键添加到列名列表中
    header.extend(attribute_cols)

    # 初始化一个用于存储数据框记录的列表
    records = []

    # 遍历每个实体
    for entity in entities:
        # 创建一个新的记录列表，包含id、名称和描述
        new_record = [
            entity.short_id if entity.short_id else "",
            entity.title,
            entity.description if entity.description else "",
        ]

        # 如果include_entity_rank为真，添加排名到记录列表
        if include_entity_rank:
            new_record.append(str(entity.rank))

        # 遍历属性列，添加属性值到记录列表
        for field in attribute_cols:
            field_value = (
                str(entity.attributes.get(field))
                if entity.attributes and entity.attributes.get(field)
                else ""
            )
            new_record.append(field_value)
        # 将新记录添加到记录列表中
        records.append(new_record)
    
    # 根据记录列表和列名创建并返回数据框
    return pd.DataFrame(records, columns=cast(Any, header))

# 定义一个名为is_valid_uuid的函数，判断一个字符串是否是有效的UUID
def is_valid_uuid(value: str) -> bool:
    """检查字符串是否符合UUID格式。"""
    # 尝试将字符串转换为UUID
    try:
        uuid.UUID(str(value))
    # 如果转换失败（即ValueError），返回False
    except ValueError:
        return False
    # 如果转换成功，返回True
    else:
        return True

