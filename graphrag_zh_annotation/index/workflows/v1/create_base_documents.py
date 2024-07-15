# 导入一个名为DEFAULT_INPUT_NAME的变量，它来自datashaper模块
from datashaper import DEFAULT_INPUT_NAME

# 从graphrag.index.config模块中导入两个类：PipelineWorkflowConfig和PipelineWorkflowStep
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权信息，代码遵循MIT许可证
# 注释中的文字不会被计算机执行，只是给人看的法律声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块的功能
# 在Python中，三引号包围的字符串用于创建多行注释
"""这是一个包含build_steps方法定义的模块。"""

# 重复导入datashaper的DEFAULT_INPUT_NAME，虽然这不是必须的，但保持了代码的一致性
from datashaper import DEFAULT_INPUT_NAME

# 从graphrag.index.config导入PipelineWorkflowConfig和PipelineWorkflowStep类，与上面相同
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个变量，叫做workflow_name，它的值是"create_base_documents"
# 这个变量可能在后续的代码中用来表示某个工作流程的名称
workflow_name = "create_base_documents"

# 定义一个名为 build_steps 的函数，它接受一个名为 config 的参数，这个参数类型是 PipelineWorkflowConfig
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数的作用是创建一个表格，里面有关于文档的信息。

    # 依赖
    * `workflow:create_final_text_units`
    """
    # 从 config 中获取 "document_attribute_columns" 参数，如果不存在则返回一个空列表
    document_attribute_columns = config.get("document_attribute_columns", [])

    # 创建并返回一个步骤列表
    return [
        # 第一步：展开数据，将 "document_ids" 列的内容拆分成单独的行
        {
            "verb": "unroll",
            "args": {"column": "document_ids"},
            "input": {"source": "workflow:create_final_text_units"},
        },
        # 第二步：选择需要的列："id", "document_ids", "text"
        {
            "verb": "select",
            "args": {
                "columns": ["id", "document_ids", "text"]
            },
        },
        # 第三步：重命名列名
        {
            "id": "rename_chunk_doc_id",
            "verb": "rename",
            "args": {
                "columns": {
                    "document_ids": "chunk_doc_id",
                    "id": "chunk_id",
                    "text": "chunk_text",
                }
            },
        },
        # 第四步：将数据表按照 "chunk_doc_id" 和 "id" 进行连接
        {
            "verb": "join",
            "args": {
                "on": ["chunk_doc_id", "id"]
            },
            "input": {"source": "rename_chunk_doc_id", "others": [DEFAULT_INPUT_NAME]},
        },
        # 第五步：按 "id" 分组，收集 "chunk_id" 列的值到 "text_units" 列
        {
            "id": "docs_with_text_units",
            "verb": "aggregate_override",
            "args": {
                "groupby": ["id"],
                "aggregations": [
                    {
                        "column": "chunk_id",
                        "operation": "array_agg",
                        "to": "text_units",
                    }
                ],
            },
        },
        # 第六步：进行右外连接，连接 "docs_with_text_units" 和原始数据表
        {
            "verb": "join",
            "args": {
                "on": ["id", "id"],
                "strategy": "right outer",
            },
            "input": {
                "source": "docs_with_text_units",
                "others": [DEFAULT_INPUT_NAME],
            },
        },
        # 第七步：重命名 "text" 列为 "raw_content"
        {
            "verb": "rename",
            "args": {"columns": {"text": "raw_content"}},
        },
        # 对于每个文档属性列，进行转换，将其类型转为字符串
        *[
            {
                "verb": "convert",
                "args": {
                    "column": column,
                    "to": column,
                    "type": "string",
                },
            }
            for column in document_attribute_columns
        ],
        # 如果有文档属性列，合并这些列到 "attributes" 列，使用 JSON 格式
        {
            "verb": "merge_override",
            "enabled": len(document_attribute_columns) > 0,
            "args": {
                "columns": document_attribute_columns,
                "strategy": "json",
                "to": "attributes",
            },
        },
        # 最后一步：将 "id" 列的类型转为字符串
        {"verb": "convert", "args": {"column": "id", "to": "id", "type": "string"}},
    ]

