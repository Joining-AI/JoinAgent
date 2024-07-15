# 导入一个叫做AsyncType的特殊类型，它用于处理异步操作
from datashaper import AsyncType

# 从graphrag.index.config模块中导入两个类：PipelineWorkflowConfig和PipelineWorkflowStep
# 这两个类可能与数据处理流程有关
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权信息，告诉你这个代码受MIT许可证保护
# 注释中的"Copyright (c) 2024 Microsoft Corporation. Licensed under the MIT License"

# 这个是文档字符串，描述了这个模块的作用
# 它包含了一个名为build_steps的方法定义
"""

A module containing build_steps method definition.
"""

# 定义一个变量workflow_name，它的值是字符串"create_final_covariates"
# 这个变量可能表示一个数据处理工作流的名称
workflow_name = "create_final_covariates"

# 定义一个名为build_steps的函数，它接受一个名为config的参数，类型是PipelineWorkflowConfig
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数用来创建最终的协变量表。
    
    它需要依赖两个步骤：
    1. `workflow:create_base_text_units`
    2. `workflow:create_base_extracted_entities`
    """
    
    # 从config中获取"claim_extract"部分，如果没有就返回一个空字典
    claim_extract_config = config.get("claim_extract", {})

    # 创建一个字典，表示输入数据来源于"workflow:create_base_text_units"
    input = {"source": "workflow:create_base_text_units"}

    # 返回一个列表，包含多个步骤
    return [
        # 第一步：提取协变量
        {
            "verb": "extract_covariates",  # 动作是"提取协变量"
            "args": {  # 参数设置
                "column": config.get("chunk_column", "chunk"),  # 用config中的"chunk_column"或默认的"chunk"
                "id_column": config.get("chunk_id_column", "chunk_id"),  # 用config中的"chunk_id_column"或默认的"chunk_id"
                "resolved_entities_column": "resolved_entities",  # 协变量列名
                "covariate_type": "claim",  # 协变量类型是"claim"
                "async_mode": config.get("async_mode", AsyncType.AsyncIO),  # 异步模式，使用config中的"async_mode"或默认的AsyncType.AsyncIO
                **claim_extract_config,  # 添加"claim_extract"配置中的所有键值对
            },
            "input": input,  # 使用上面定义的输入
        },
        # 第二步：窗口操作
        {
            "verb": "window",  # 动作是"窗口"
            "args": {  # 参数设置
                "to": "id",  # 依据"id"进行操作
                "operation": "uuid",  # 操作是生成唯一标识符
                "column": "covariate_type",  # 根据"covariate_type"列
            },
        },
        # 第三步：生成人类可读的ID
        {
            "verb": "genid",  # 动作是"生成ID"
            "args": {  # 参数设置
                "to": "human_readable_id",  # 目标列名
                "method": "increment",  # 方法是递增
            },
        },
        # 第四步：转换ID类型
        {
            "verb": "convert",  # 动作是"转换"
            "args": {  # 参数设置
                "column": "human_readable_id",  # 转换的列名
                "type": "string",  # 转换为字符串类型
                "to": "human_readable_id",  # 目标列名
            },
        },
        # 第五步：重命名列
        {
            "verb": "rename",  # 动作是"重命名"
            "args": {  # 参数设置
                "columns": {  # 需要重命名的列和新名称
                    "chunk_id": "text_unit_id",  # 将"chunk_id"改为"text_unit_id"
                }
            },
        },
        # 第六步：选择特定列
        {
            "verb": "select",  # 动作是"选择"
            "args": {  # 参数设置
                "columns": [  # 列表中的列将被保留
                    "id",
                    "human_readable_id",
                    "covariate_type",
                    "type",
                    "description",
                    "subject_id",
                    "subject_type",
                    "object_id",
                    "object_type",
                    "status",
                    "start_date",
                    "end_date",
                    "source_text",
                    "text_unit_id",
                    "document_ids",
                    "n_tokens",
                ]
            },
        },
    ]

