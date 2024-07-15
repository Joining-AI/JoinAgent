# 导入两个类：PipelineWorkflowConfig 和 PipelineWorkflowStep，它们来自 graphrag.index.config 模块
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权声明，它说这个代码可以按照MIT许可证的规定使用
# Licensed under the MIT License

# 这是一个模块，里面有一个方法叫做 build_steps 的定义，它是用来创建步骤的
# "A module containing build_steps method definition."

# 从 graphrag.index.config 导入之前提到的两个类（再次导入，虽然通常不会这样写，但这里是必要的）
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个变量 workflow_name，它的值是 "create_final_text_units"
workflow_name = "create_final_text_units"

# 定义一个名为 build_steps 的函数，它接收一个名为 config 的参数，这个参数类型是 PipelineWorkflowConfig
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数用来创建最终的文本单元表。

    这里依赖于几个其他步骤：
    * `workflow:create_base_text_units`
    * `workflow:create_final_entities`
    * `workflow:create_final_communities`
    """
    
    # 从 config 中获取 "text_embed" 配置，如果不存在就用一个空字典代替
    base_text_embed = config.get("text_embed", {})
    
    # 获取 "text_unit_text_embed" 配置，如果不存在就用 "text_embed" 配置（或空字典）代替
    text_unit_text_embed_config = config.get("text_unit_text_embed", base_text_embed)
    
    # 检查 "covariates_enabled" 是否开启，如果配置中没有就默认为 False
    covariates_enabled = config.get("covariates_enabled", False)
    
    # 检查是否跳过文本单元嵌入，如果配置中没有就默认为 False
    skip_text_unit_embedding = config.get("skip_text_unit_embedding", False)
    
    # 检查是否正在使用向量存储，如果 "strategy" 里的 "vector_store" 不为空则为 True
    is_using_vector_store = (
        text_unit_text_embed_config.get("strategy", {}).get("vector_store", None)
        is not None
    )

    # 创建并返回一个包含多个步骤的列表
    return [
        # 第一步：选择 "create_base_text_units" 步骤产生的数据的 "id", "chunk", "document_ids", "n_tokens" 列
        {
            "verb": "select",
            "args": {"columns": ["id", "chunk", "document_ids", "n_tokens"]},
            "input": {"source": "workflow:create_base_text_units"},
        },
        # 第二步：重命名 "chunk" 列为 "text"
        {
            "id": "pre_entity_join",
            "verb": "rename",
            "args": {
                "columns": {
                    "chunk": "text",
                },
            },
        },
        # 第三步：将文本单元与实体ID连接
        {
            "id": "pre_relationship_join",
            "verb": "join",
            "args": {
                "on": ["id", "id"],
                "strategy": "left outer",
            },
            "input": {
                "source": "pre_entity_join",
                "others": ["workflow:join_text_units_to_entity_ids"],
            },
        },
        # 第四步：将文本单元与关系ID连接
        {
            "id": "pre_covariate_join",
            "verb": "join",
            "args": {
                "on": ["id", "id"],
                "strategy": "left outer",
            },
            "input": {
                "source": "pre_relationship_join",
                "others": ["workflow:join_text_units_to_relationship_ids"],
            },
        },
        # 第五步（可选）：如果 "covariates_enabled" 为真，则将文本单元与协变量ID连接
        {
            "enabled": covariates_enabled,
            "verb": "join",
            "args": {
                "on": ["id", "id"],
                "strategy": "left outer",
            },
            "input": {
                "source": "pre_covariate_join",
                "others": ["workflow:join_text_units_to_covariate_ids"],
            },
        },
        # 第六步：将实体和关系组合成数组
        {
            "verb": "aggregate_override",
            "args": {
                "groupby": ["id"],  # 根据之前的连接
                "aggregations": [
                    # 对每个组进行操作，保留每列的第一个值
                    {"column": "text", "operation": "any", "to": "text"},
                    {"column": "n_tokens", "operation": "any", "to": "n_tokens"},
                    {"column": "document_ids", "operation": "any", "to": "document_ids"},
                    {"column": "entity_ids", "operation": "any", "to": "entity_ids"},
                    {"column": "relationship_ids", "operation": "any", "to": "relationship_ids"},
                    # 如果协变量开启，添加协变量ID
                    *(
                        []
                        if not covariates_enabled
                        else [{"column": "covariate_ids", "operation": "any", "to": "covariate_ids"}]
                    ),
                ],
            },
        },
        # 第七步（可选）：如果 "skip_text_unit_embedding" 为假，且不使用向量存储，进行文本嵌入
        {
            "id": "embedded_text_units",
            "verb": "text_embed",
            "enabled": not skip_text_unit_embedding,
            "args": {
                "column": config.get("column", "text"),
                "to": config.get("to", "text_embedding"),
                **text_unit_text_embed_config,
            },
        },
        # 第八步：选择最终输出的列，根据前面的设置决定是否包含 "text_embedding", "covariate_ids"
        {
            "verb": "select",
            "args": {
                "columns": [
                    "id",
                    "text",
                    *(
                        []
                        if (skip_text_unit_embedding or is_using_vector_store)
                        else ["text_embedding"]
                    ),
                    "n_tokens",
                    "document_ids",
                    "entity_ids",
                    "relationship_ids",
                    *([] if not covariates_enabled else ["covariate_ids"]),
                ],
            },
        },
    ]

