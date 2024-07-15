# 导入两个特殊的东西，它们来自graphrag.index.config模块
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权信息，用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这里写了一个文档字符串，它描述了这个模块是干什么的
"""这是一个包含build_steps方法定义的模块。"""

# 再次导入PipelineWorkflowConfig和PipelineWorkflowStep，虽然之前已经导入过，但这里可能是为了强调或者避免名字冲突
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个变量，叫workflow_name，它的值是"create_final_relationships"
workflow_name = "create_final_relationships"

# 定义一个名为 build_steps 的函数，它需要一个名为 config 的参数
def build_steps(
    config: PipelineWorkflowConfig,  # 这个参数是一个特定类型的配置对象
) -> list[PipelineWorkflowStep]:  # 函数会返回一个步骤列表，每个步骤都是 PipelineWorkflowStep 类型

    """
    创建最终的关系表。

    这个函数依赖于另一个步骤：`workflow:create_base_entity_graph`
    """
    
    # 从配置中获取“text_embed”键的值，如果没有则返回一个空字典
    base_text_embed = config.get("text_embed", {})

    # 从配置中获取“relationship_description_embed”键的值，如果不存在则使用“text_embed”的值
    relationship_description_embed_config = config.get(
        "relationship_description_embed", base_text_embed
    )

    # 从配置中获取“skip_description_embedding”键的值，如果不存在则设为 False
    skip_description_embedding = config.get("skip_description_embedding", False)

    # 创建并返回一个包含多个步骤的列表
    return [
        # 第一步：解包图数据
        {
            "verb": "unpack_graph",  # 动作是“解包图”
            "args": {  # 参数设置
                "column": "clustered_graph",  # 解包的列名
                "type": "edges",  # 图的类型是边
            },
            "input": {"source": "workflow:create_base_entity_graph"},  # 输入来自另一个步骤
        },
        # 第二步：重命名列
        {
            "verb": "rename",  # 动作是“重命名”
            "args": {  # 参数设置
                "columns": {"source_id": "text_unit_ids"},  # 将"source_id"改名为"text_unit_ids"
            },
        },
        # 第三步：过滤数据
        {
            "verb": "filter",  # 动作是“过滤”
            "args": {  # 参数设置
                "column": "level",  # 过滤的列是"level"
                "criteria": [{"type": "value", "operator": "equals", "value": 0}],  # 只保留 level 等于 0 的行
            },
        },
        # 第四步：根据条件生成文本嵌入（如果未跳过描述嵌入）
        {
            "verb": "text_embed",  # 动作是“文本嵌入”
            "enabled": not skip_description_embedding,  # 如果不跳过描述嵌入，则启用此步骤
            "args": {  # 参数设置
                "embedding_name": "relationship_description",  # 嵌入名称
                "column": "description",  # 嵌入的列是"description"
                "to": "description_embedding",  # 新列名
                **relationship_description_embed_config,  # 使用之前获取的嵌入配置
            },
        },
        # 第五步：删除列
        {
            "id": "pruned_edges",  # 步骤 ID
            "verb": "drop",  # 动作是“删除”
            "args": {"columns": ["level"]},  # 删除的列是"level"
        },
        # 第六步：过滤数据（第二个过滤步骤）
        {
            "id": "filtered_nodes",  # 步骤 ID
            "verb": "filter",  # 动作是“过滤”
            "args": {  # 参数设置
                "column": "level",  # 过滤的列是"level"
                "criteria": [{"type": "value", "operator": "equals", "value": 0}],  # 只保留 level 等于 0 的行
            },
            "input": "workflow:create_final_nodes",  # 输入来自另一个步骤
        },
        # 第七步：计算边的综合度
        {
            "verb": "compute_edge_combined_degree",  # 动作是“计算边的综合度”
            "args": {"to": "rank"},  # 结果存储在新列"rank"中
            "input": {
                "source": "pruned_edges",  # 输入数据来自之前步骤
                "nodes": "filtered_nodes",  # 节点数据来自之前步骤
            },
        },
        # 第八步：转换列的数据类型
        {
            "verb": "convert",  # 动作是“转换”
            "args": {  # 参数设置
                "column": "human_readable_id",  # 要转换的列是"human_readable_id"
                "type": "string",  # 转换为字符串类型
                "to": "human_readable_id",  # 新列名与原列名相同
            },
        },
        # 第九步：转换列的数据类型（第二个转换步骤）
        {
            "verb": "convert",  # 动作是“转换”
            "args": {  # 参数设置
                "column": "text_unit_ids",  # 要转换的列是"text_unit_ids"
                "type": "array",  # 转换为数组类型
                "to": "text_unit_ids",  # 新列名与原列名相同
            },
        },
    ]

