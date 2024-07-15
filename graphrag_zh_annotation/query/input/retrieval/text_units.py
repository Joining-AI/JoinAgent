# 导入必要的工具
from typing import Any, cast  # 这是用于类型检查的，帮助我们确保变量的类型正确
import pandas as pd  # 用于数据处理的库
from graphrag.model import Entity, TextUnit  # 从graphrag.model中导入两个类：实体（Entity）和文本单元（TextUnit）

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.  # 这是代码的版权归属
# Licensed under the MIT License  # 使用MIT许可证授权

# 定义一个模块，包含一些实用函数来从集合中获取文本单元

# 函数1：获取与选定实体相关的文本单元
def get_candidate_text_units(  # 输入是选择的实体列表和文本单元列表
    selected_entities: list[Entity],  # 选择的实体列表
    text_units: list[TextUnit],  # 所有的文本单元列表
) -> pd.DataFrame:  # 输出是一个数据框（DataFrame）
    """找到与所选实体关联的所有文本单元。"""
    # 获取所有选定实体的文本单元ID
    selected_text_ids = [
        entity.text_unit_ids for entity in selected_entities if entity.text_unit_ids
    ]
    # 将嵌套列表展开成单一列表
    selected_text_ids = [item for sublist in selected_text_ids for item in sublist]
    # 根据ID找出相关的文本单元
    selected_text_units = [unit for unit in text_units if unit.id in selected_text_ids]
    # 转换成数据框并返回
    return to_text_unit_dataframe(selected_text_units)

# 函数2：将文本单元列表转换为数据框
def to_text_unit_dataframe(  # 输入是文本单元列表
    text_units: list[TextUnit],  # 文本单元列表
) -> pd.DataFrame:  # 输出是数据框
    """将文本单元列表转换成Pandas DataFrame格式。"""
    # 如果没有文本单元，返回空数据框
    if len(text_units) == 0:
        return pd.DataFrame()

    # 创建表头
    header = ["id", "text"]  # 基本列名
    # 获取第一个文本单元的属性键，如果有的话
    attribute_cols = (
        list(text_units[0].attributes.keys()) if text_units[0].attributes else []
    )
    # 删除已存在的表头中的属性键
    attribute_cols = [col for col in attribute_cols if col not in header]
    # 将属性键添加到表头
    header.extend(attribute_cols)

    # 创建记录列表
    records = []
    # 遍历每个文本单元
    for unit in text_units:
        # 创建新记录，包括ID、文本和属性值
        new_record = [
            unit.short_id,  # 短ID
            unit.text,  # 文本内容
            *[
                str(unit.attributes.get(field, ""))  # 将属性值转换为字符串，如果存在的话
                if unit.attributes and unit.attributes.get(field)  # 检查属性是否存在
                else ""  # 如果不存在，用空字符串填充
                for field in attribute_cols  # 遍历属性列
            ],
        ]
        # 添加新记录到记录列表
        records.append(new_record)
    # 创建数据框并返回
    return pd.DataFrame(records, columns=cast(Any, header))  # 数据框的列设置为header

