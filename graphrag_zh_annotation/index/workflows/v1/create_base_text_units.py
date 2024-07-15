# 导入一个叫做DEFAULT_INPUT_NAME的变量，它来自datashaper模块
from datashaper import DEFAULT_INPUT_NAME

# 从graphrag.index.config模块导入两个类：PipelineWorkflowConfig和PipelineWorkflowStep
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权信息，代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段代码定义了一个模块，里面有一个方法build_steps（注：这里没有实际显示方法的代码）
# 这是一个注释，用来描述这个模块的作用
"""

A module containing build_steps method definition.

"""

# 定义一个变量workflow_name，它的值是字符串"create_base_text_units"
workflow_name = "create_base_text_units"

# 定义一个名为 build_steps 的函数，它接受一个名为 config 的参数
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    创建一个用于文本单元的基础表格。

    ## 依赖项
    无
    """
    # 从 config 中获取或默认使用 "chunk" 作为 chunk_column_name
    chunk_column_name = config.get("chunk_column", "chunk")
    
    # 从 config 中获取或默认使用一个空列表作为 chunk_by_columns
    chunk_by_columns = config.get("chunk_by", []) or []

    # 从 config 中获取或默认使用 "n_tokens" 作为 n_tokens_column_name
    n_tokens_column_name = config.get("n_tokens_column", "n_tokens")

    # 返回一系列的操作步骤
    return [
        # 按 "id" 列升序排序
        {
            "verb": "orderby",
            "args": {
                "orders": [
                    {"column": "id", "direction": "asc"},
                ]
            },
            "input": {"source": DEFAULT_INPUT_NAME},
        },
        # 把 "id" 和 "text" 列组合成新的列 "text_with_ids"
        {
            "verb": "zip",
            "args": {
                "columns": ["id", "text"],
                "to": "text_with_ids",
            },
        },
        # 根据 chunk_by_columns 列进行分组，把 "text_with_ids" 列聚合为 "texts"
        {
            "verb": "aggregate_override",
            "args": {
                "groupby": [*chunk_by_columns] if len(chunk_by_columns) > 0 else None,
                "aggregations": [
                    {
                        "column": "text_with_ids",
                        "operation": "array_agg",
                        "to": "texts",
                    }
                ],
            },
        },
        # 把 "texts" 列分割成 "chunks"，根据 config 中的 "text_chunk" 参数
        {
            "verb": "chunk",
            "args": {"column": "texts", "to": "chunks", **config.get("text_chunk", {})},
        },
        # 选择需要的列：chunk_by_columns 列和 "chunks" 列
        {
            "verb": "select",
            "args": {
                "columns": [*chunk_by_columns, "chunks"],
            },
        },
        # 把 "chunks" 列展开成多行
        {
            "verb": "unroll",
            "args": {
                "column": "chunks",
            },
        },
        # 把 "chunks" 列重命名为 chunk_column_name
        {
            "verb": "rename",
            "args": {
                "columns": {
                    "chunks": chunk_column_name,
                }
            },
        },
        # 生成每个 chunk 的唯一 id（使用 md5_hash 方法）
        {
            "verb": "genid",
            "args": {
                "to": "chunk_id",
                "method": "md5_hash",
                "hash": [chunk_column_name],
            },
        },
        # 把 chunk_column_name 列解压成 "document_ids", chunk_column_name 和 n_tokens_column_name 列
        {
            "verb": "unzip",
            "args": {
                "column": chunk_column_name,
                "to": ["document_ids", chunk_column_name, n_tokens_column_name],
            },
        },
        # 复制 "chunk_id" 列为 "id" 列
        {
            "verb": "copy",
            "args": {"column": "chunk_id", "to": "id"},
        },
        # 删除空的 chunk（过滤掉 chunk_column_name 为空的行）
        {
            "verb": "filter",
            "args": {
                "column": chunk_column_name,
                "criteria": [
                    {
                        "type": "value",
                        "operator": "is not empty",
                    }
                ],
            },
        },
    ]

