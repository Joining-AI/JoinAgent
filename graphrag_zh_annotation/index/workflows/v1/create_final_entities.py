# 导入两个特殊的东西，它们来自 graphrag.index.config 模块
# PipelineWorkflowConfig 是一个配置类，用来设置工作流程
# PipelineWorkflowStep 是一个步骤类，表示工作流程中的每一步
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司的版权声明，告诉我们代码的版权属于微软，使用的是 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个模块的文档字符串，简单说明了这个文件里有什么
# "A module containing build_steps method definition."
# 大概意思是：这个文件包含了 build_steps 方法的定义

# 再次导入 PipelineWorkflowConfig 和 PipelineWorkflowStep，虽然之前已经导入过，但这里再次强调它们的重要性
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个变量 workflow_name，它的值是 "create_final_entities"
# 这个名字可能是工作流程的名称，用于创建最终的实体（可能是数据库里的条目或者程序里的对象）
workflow_name = "create_final_entities"

# 定义一个函数，叫做 build_steps，它接受一个名为config的参数，这个参数是PipelineWorkflowConfig类型
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数的作用是创建最终的实体表格。

    依赖的步骤：
    * `workflow:create_base_entity_graph`
    """
    # 从config中获取"文本嵌入"配置，如果没有就用一个空字典代替
    base_text_embed = config.get("text_embed", {})

    # 从config中获取"实体名称嵌入"配置，如果没有就用"文本嵌入"的配置
    entity_name_embed_config = config.get("entity_name_embed", base_text_embed)

    # 从config中获取"实体名称描述嵌入"配置，如果没有就用"文本嵌入"的配置
    entity_name_description_embed_config = config.get(
        "entity_name_description_embed", base_text_embed
    )

    # 从config中获取是否跳过名称嵌入的设置，默认为False
    skip_name_embedding = config.get("skip_name_embedding", False)

    # 从config中获取是否跳过描述嵌入的设置，默认为False
    skip_description_embedding = config.get("skip_description_embedding", False)

    # 检查是否正在使用向量存储策略
    is_using_vector_store = (
        entity_name_embed_config.get("strategy", {}).get("vector_store", None)
        is not None
    )

    # 创建并返回一个步骤列表
    return [
        # 解包图数据，输入来源于`workflow:create_base_entity_graph`
        {
            "verb": "unpack_graph",
            "args": {
                "column": "clustered_graph",
                "type": "nodes",
            },
            "input": {"source": "workflow:create_base_entity_graph"},
        },
        # 重命名列"clustered_graph"为"title"
        {"verb": "rename", "args": {"columns": {"label": "title"}}},
        # 选择需要的列
        {
            "verb": "select",
            "args": {
                "columns": [
                    "id",
                    "title",
                    "type",
                    "description",
                    "human_readable_id",
                    "graph_embedding",
                    "source_id",
                ],
            },
        },
        # 去除重复的实体
        {
            "verb": "dedupe",
            "args": {"columns": ["id"]},
        },
        # 重命名列"title"为"name"
        {"verb": "rename", "args": {"columns": {"title": "name"}}},
        # 过滤掉名字为空的行
        {
            "verb": "filter",
            "args": {
                "column": "name",
                "criteria": [
                    {
                        "type": "value",
                        "operator": "is not empty",
                    }
                ],
            },
        },
        # 将"source_id"列按逗号分隔，生成新的列"text_unit_ids"
        {
            "verb": "text_split",
            "args": {"separator": ",", "column": "source_id", "to": "text_unit_ids"},
        },
        # 删除"source_id"列
        {"verb": "drop", "args": {"columns": ["source_id"]}},
        # 如果没有跳过名称嵌入，则进行名称嵌入
        {
            "verb": "text_embed",
            "enabled": not skip_name_embedding,
            "args": {
                "embedding_name": "entity_name",
                "column": "name",
                "to": "name_embedding",
                **entity_name_embed_config,
            },
        },
        # 如果没有跳过描述嵌入，将名称和描述合并
        {
            "verb": "merge",
            "enabled": not skip_description_embedding,
            "args": {
                "strategy": "concat",
                "columns": ["name", "description"],
                "to": "name_description",
                "delimiter": ":",
                "preserveSource": True,
            },
        },
        # 如果没有跳过描述嵌入，对合并后的名称描述进行嵌入
        {
            "verb": "text_embed",
            "enabled": not skip_description_embedding,
            "args": {
                "embedding_name": "entity_name_description",
                "column": "name_description",
                "to": "description_embedding",
                **entity_name_description_embed_config,
            },
        },
        # 如果没有跳过描述嵌入，删除名称描述列
        {
            "verb": "drop",
            "enabled": not skip_description_embedding,
            "args": {
                "columns": ["name_description"],
            },
        },
        # 如果没有跳过描述嵌入且不使用向量存储，过滤掉描述嵌入为空的行
        {
            "verb": "filter",
            "enabled": not skip_description_embedding and not is_using_vector_store,
            "args": {
                "column": "description_embedding",
                "criteria": [
                    {
                        "type": "value",
                        "operator": "is not empty",
                    }
                ],
            },
        },
    ]

