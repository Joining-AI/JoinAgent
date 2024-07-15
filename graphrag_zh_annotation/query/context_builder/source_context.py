# 导入随机数模块，用于生成随机数
import random

# 从typing模块导入Any和cast，它们是类型检查的工具
from typing import Any, cast

# 导入pandas库，这是一个用于数据分析的库
import pandas as pd

# 导入tiktoken库，这个库可能用于处理特定的令牌或文本操作
import tiktoken

# 从graphrag.model导入三个类：Entity（实体）、Relationship（关系）和TextUnit（文本单元）
from graphrag.model import Entity, Relationship, TextUnit

# 从graphrag.query.llm.text_utils导入num_tokens函数，它可能用于计算文本中的令牌数量
from graphrag.query.llm.text_utils import num_tokens

# 这段文字是版权信息，表示代码归微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了下面的代码是关于什么的
"""
这是一个包含用于构建文本单元上下文的实用方法的模块。
这些方法用于搜索系统的提示。
"""

# 定义一个函数，名为 build_text_unit_context，它接受一些参数
def build_text_unit_context(
    text_units: list[TextUnit],  # 一个包含 TextUnit 类型对象的列表
    token_encoder: tiktoken.Encoding | None = None,  # 用于编码文本的工具，可选
    column_delimiter: str = "|",  # 列之间的分隔符，默认为 "|"
    shuffle_data: bool = True,  # 是否打乱数据，默认是 True
    max_tokens: int = 8000,  # 最大允许的文本单元数，默认为 8000
    context_name: str = "Sources",  # 上下文名称，默认为 "Sources"
    random_state: int = 86,  # 设置随机种子，默认为 86
) -> tuple[str, dict[str, pd.DataFrame]]:  # 返回一个字符串和一个字典，字典包含一个 DataFrame

    # 如果 text_units 为空或没有元素，直接返回空字符串和空字典
    if text_units is None or len(text_units) == 0:
        return ("", {})

    # 如果需要打乱数据，设置随机种子并打乱 text_units 列表
    if shuffle_data:
        random.seed(random_state)
        random.shuffle(text_units)

    # 添加上下文标题
    current_context_text = f"-----{context_name}-----" + "\n"

    # 创建列名
    header = ["id", "text"]  # 基本列名
    attribute_cols = (  # 获取 text_units 第一个对象的属性键
        list(text_units[0].attributes.keys())
        if text_units[0].attributes
        else []
    )
    # 保留不在基本列名中的属性列
    attribute_cols = [col for col in attribute_cols if col not in header]
    # 将属性列添加到头信息中
    header.extend(attribute_cols)

    # 添加表头到上下文文本
    current_context_text += column_delimiter.join(header) + "\n"
    # 计算当前上下文文本的 token 数量
    current_tokens = num_tokens(current_context_text, token_encoder)
    # 初始化记录列表
    all_context_records = [header]

    # 遍历 text_units 中的每个单元
    for unit in text_units:
        # 创建新的上下文信息
        new_context = [
            unit.short_id,  # 单元的短 ID
            unit.text,  # 单元的文本
            *[
                str(unit.attributes.get(field, ""))  # 单元的属性值，如果不存在则为空字符串
                if unit.attributes
                else ""
                for field in attribute_cols
            ],
        ]
        # 将新上下文信息转换为字符串并添加换行符
        new_context_text = column_delimiter.join(new_context) + "\n"
        # 计算新上下文文本的 token 数量
        new_tokens = num_tokens(new_context_text, token_encoder)

        # 如果当前 token 数加上新 token 数超过最大值，停止添加
        if current_tokens + new_tokens > max_tokens:
            break

        # 将新上下文文本添加到当前上下文文本
        current_context_text += new_context_text
        # 将新上下文信息添加到记录列表
        all_context_records.append(new_context)
        # 更新当前 token 数量
        current_tokens += new_tokens

    # 如果记录列表有多个元素，创建 DataFrame
    if len(all_context_records) > 1:
        record_df = pd.DataFrame(
            all_context_records[1:], columns=cast(Any, all_context_records[0])
        )
    else:
        record_df = pd.DataFrame()  # 否则创建空 DataFrame
    # 返回当前上下文文本和包含 DataFrame 的字典
    return current_context_text, {context_name.lower(): record_df}

# 定义一个函数count_relationships，接收三个参数：text_unit（文本单元），entity（实体）和relationships（关系字典）
def count_relationships(
    text_unit: TextUnit,  # 这是一个特定的文本单元对象
    entity: Entity,  # 这是一个特定的实体对象
    relationships: dict[str, Relationship]  # 关系字典，键是字符串，值是关系对象
) -> int:  # 函数返回一个整数，表示找到的关系数量

    # 创建一个空列表，用来存储匹配到的关系
    matching_relationships = list[Relationship]()

    # 如果文本单元的关系ID列表不存在（即为None）
    if text_unit.relationship_ids is None:

        # 遍历关系字典中的所有值（关系对象）
        entity_relationships = [
            rel  # 将与实体相关的所有关系添加到列表中
            for rel in relationships.values()  # 在字典值中查找
            if rel.source == entity.title or rel.target == entity.title  # 如果关系的源或目标是实体
        ]

        # 筛选出有文本单元ID的关系
        entity_relationships = [
            rel  # 添加到列表中
            for rel in entity_relationships  # 遍历之前找到的关系
            if rel.text_unit_ids  # 只保留有文本单元ID的关系
        ]

        # 再次筛选，找出与当前文本单元ID匹配的关系
        matching_relationships = [
            rel  # 添加到匹配关系列表中
            for rel in entity_relationships  # 遍历有文本单元ID的关系
            if text_unit.id in rel.text_unit_ids  # 检查文本单元ID是否在关系的文本单元ID列表里
        ]  # 注意：这里的两个"ignore"是为了忽略类型检查的警告

    # 如果文本单元的关系ID列表存在
    else:

        # 根据文本单元的关系ID找到对应的关系对象
        text_unit_relationships = [
            relationships[rel_id]  # 添加到列表中
            for rel_id in text_unit.relationship_ids  # 遍历文本单元的关系ID
            if rel_id in relationships  # 检查关系ID是否在关系字典中
        ]

        # 筛选出与实体相关的关系
        matching_relationships = [
            rel  # 添加到匹配关系列表中
            for rel in text_unit_relationships  # 遍历文本单元的关系
            if rel.source == entity.title or rel.target == entity.title  # 如果关系的源或目标是实体
        ]

    # 返回匹配到的关系数量
    return len(matching_relationships)

