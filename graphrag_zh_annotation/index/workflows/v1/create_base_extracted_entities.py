# 导入一个叫做AsyncType的特殊类型，它用于处理异步（等待结果）的代码
from datashaper import AsyncType

# 从graphrag.index.config模块中导入两个类：PipelineWorkflowConfig和PipelineWorkflowStep
# 这些类可能用来配置和管理数据处理的工作流程
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司的版权声明，告诉我们这个代码受MIT许可证保护
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个文件的作用，包含了一个名为build_steps的方法定义
"""这是一个包含build_steps方法定义的模块。"""

# 继续导入AsyncType，确保我们有两个相同的导入，这在实际编程中通常是不必要的
from datashaper import AsyncType

# 定义一个变量，名叫workflow_name，它的值是字符串"create_base_extracted_entities"
# 这个变量可能用于表示我们要执行的工作流程的名称
workflow_name = "create_base_extracted_entities"

# 定义一个名为 build_steps 的函数，它接受一个名为 config 的参数，类型是 PipelineWorkflowConfig
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:

    # 这个函数的目的是创建一个处理实体（比如文本中的关键词）的基础表格
    """
    创建提取出的实体的基础表格。

    ## 依赖项
    * `workflow:create_base_text_units`
    """

    # 从 config 中获取 "entity_extract" 部分的配置，如果没有就返回一个空字典
    entity_extraction_config = config.get("entity_extract", {})

    # 获取 "graphml_snapshot" 配置，如果为假则设为 False（双重否定表示肯定）
    graphml_snapshot_enabled = config.get("graphml_snapshot", False) or False

    # 获取 "raw_entity_snapshot" 配置，如果为假则设为 False（双重否定表示肯定）
    raw_entity_snapshot_enabled = config.get("raw_entity_snapshot", False) or False

    # 创建并返回一个步骤列表
    return [
        # 第一步：实体提取
        {
            "verb": "entity_extract",  # 操作名
            "args": {  # 参数
                **entity_extraction_config,  # 使用之前获取的配置
                "column": entity_extraction_config.get("text_column", "chunk"),  # 文本列，默认是 "chunk"
                "id_column": entity_extraction_config.get("id_column", "chunk_id"),  # ID 列，默认是 "chunk_id"
                "async_mode": entity_extraction_config.get(  # 异步模式，默认是 AsyncType.AsyncIO
                    "async_mode", AsyncType.AsyncIO
                ),
                "to": "entities",  # 结果存储在 "entities" 中
                "graph_to": "entity_graph",  # 图形数据存储在 "entity_graph" 中
            },
            "input": {"source": "workflow:create_base_text_units"},  # 输入来自 "workflow:create_base_text_units"
        },
        # 第二步（可选）：原始实体快照
        {
            "verb": "snapshot",  # 操作名
            "enabled": raw_entity_snapshot_enabled,  # 如果 raw_entity_snapshot 配置为真，则执行这一步
            "args": {  # 参数
                "name": "raw_extracted_entities",  # 快照名称
                "formats": ["json"],  # 输出格式为 JSON
            },
        },
        # 第三步：合并图形数据
        {
            "verb": "merge_graphs",  # 操作名
            "args": {  # 参数
                "column": "entity_graph",  # 合并的图形数据列
                "to": "entity_graph",  # 合并后的结果存储回 "entity_graph"
                **config.get(  # 使用 config 中的 "graph_merge_operations" 配置
                    "graph_merge_operations",
                    {  # 如果没有该配置，使用以下默认值
                        "nodes": {
                            "source_id": {
                                "operation": "concat",  # 操作：连接
                                "delimiter": ", ",  # 分隔符：逗号和空格
                                "distinct": True,  # 是否只保留不同的节点
                            },
                            "description": ({
                                "operation": "concat",  # 操作：连接
                                "separator": "\n",  # 分隔符：换行
                                "distinct": False,  # 不去重
                            }),
                        },
                        "edges": {
                            "source_id": {
                                "operation": "concat",  # 操作：连接
                                "delimiter": ", ",  # 分隔符：逗号和空格
                                "distinct": True,  # 是否只保留不同的边
                            },
                            "description": ({
                                "operation": "concat",  # 操作：连接
                                "separator": "\n",  # 分隔符：换行
                                "distinct": False,  # 不去重
                            }),
                            "weight": "sum",  # 权重：求和
                        },
                    },
                ),
            },
        },
        # 第四步（可选）：保存图形数据快照
        {
            "verb": "snapshot_rows",  # 操作名
            "enabled": graphml_snapshot_enabled,  # 如果 graphml_snapshot 配置为真，则执行这一步
            "args": {  # 参数
                "base_name": "merged_graph",  # 基础名称
                "column": "entity_graph",  # 数据列
                "formats": [{"format": "text", "extension": "graphml"}],  # 格式为 text 类型的 graphml 文件
            },
        },
    ]

