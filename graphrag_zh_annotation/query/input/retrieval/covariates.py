# 导入必要的工具模块
from typing import Any, cast
import pandas as pd  # 用于数据处理的库
from graphrag.model import Covariate, Entity  # 从graphrag.model导入Covariate和Entity类

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这里是一些辅助函数，用于从集合中获取协变量（Covariates）

from typing import Any, cast

import pandas as pd

from graphrag.model import Covariate, Entity


# 定义一个函数，获取与选定实体相关的协变量
def get_candidate_covariates(
    selected_entities: list[Entity],  # 输入的选定实体列表
    covariates: list[Covariate],  # 所有可用的协变量列表
) -> list[Covariate]:  # 返回与选定实体相关的协变量列表
    """找出与选择的实体相关的所有协变量"""
    # 获取选定实体的名称列表
    selected_entity_names = [entity.title for entity in selected_entities]
    # 遍历协变量列表，如果协变量的主体在选定实体的名称中，则保留
    return [
        covariate
        for covariate in covariates
        if covariate.subject_id in selected_entity_names
    ]


# 定义一个函数，将协变量列表转换为pandas数据框
def to_covariate_dataframe(covariates: list[Covariate]) -> pd.DataFrame:
    """将协变量列表转换为易于查看的数据表"""
    # 如果没有协变量，返回空数据框
    if len(covariates) == 0:
        return pd.DataFrame()

    # 创建数据框的列名
    header = ["id", "entity"]  # 基本列名
    # 获取第一个协变量的属性（如果有的话）
    attributes = covariates[0].attributes or {} if len(covariates) > 0 else {}
    # 获取属性列名
    attribute_cols = list(attributes.keys()) if len(covariates) > 0 else []
    # 从列名中移除已存在的基本列名
    attribute_cols = [col for col in attribute_cols if col not in header]

    # 将header扩展为包括所有属性列
    header.extend(attribute_cols)

    # 初始化记录列表
    records = []
    # 遍历每个协变量
    for covariate in covariates:
        # 创建新记录，包含id和主体id
        new_record = [
            covariate.short_id if covariate.short_id else "",
            covariate.subject_id,
        ]
        # 遍历属性列，添加属性值到记录
        for field in attribute_cols:
            # 将属性值转换为字符串，如果没有则为空
            field_value = (
                str(covariate.attributes.get(field))
                if covariate.attributes and covariate.attributes.get(field)
                else ""
            )
            new_record.append(field_value)
        # 添加新记录到记录列表
        records.append(new_record)
    # 创建并返回数据框，列名使用cast转换为Any类型
    return pd.DataFrame(records, columns=cast(Any, header))

