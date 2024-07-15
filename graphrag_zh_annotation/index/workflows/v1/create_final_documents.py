# 导入两个类，它们是关于工作流程配置和步骤的定义
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司的版权信息，告诉我们这个代码的使用权
# 并且代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块里有一个方法叫做 build_steps 的定义
# 它用来创建最终的文档

# 再次导入 PipelineWorkflowConfig 和 PipelineWorkflowStep 类
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个工作流程的名字，叫 "create_final_documents"
workflow_name = "create_final_documents"

# 定义一个函数 build_steps，它需要一个参数：config
# 函数会返回一个列表，列表里是 PipelineWorkflowStep 类型的元素
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数用来创建最终的文档表格。

    需要依赖的工作流程：
    * `workflow:create_base_documents`
    * `workflow:create_base_document_nodes`
    """

    # 从 config 中获取 "text_embed" 的值，如果没有就用一个空字典
    base_text_embed = config.get("text_embed", {})

    # 获取 "document_raw_content_embed" 的值，如果不存在就用 "base_text_embed" 的值
    document_raw_content_embed_config = config.get(
        "document_raw_content_embed", base_text_embed
    )

    # 如果 "skip_raw_content_embedding" 存在并且为真，就跳过原始内容嵌入
    skip_raw_content_embedding = config.get("skip_raw_content_embedding", False)

    # 创建并返回一个列表，列表里有两个步骤
    return [
        # 第一步：重命名列，把 "text_units" 列改名为 "text_unit_ids"
        {
            "verb": "rename",  # 表示动作是重命名
            "args": {"columns": {"text_units": "text_unit_ids"}},  # 重命名的具体操作
            "input": {"source": "workflow:create_base_documents"},  # 这个步骤依赖于 "create_base_documents" 工作流程
        },
        # 第二步：根据条件进行文本嵌入
        {
            "verb": "text_embed",  # 动作是文本嵌入
            "enabled": not skip_raw_content_embedding,  # 如果不应跳过嵌入，则这个步骤启用
            "args": {
                "column": "raw_content",  # 要嵌入的列名
                "to": "raw_content_embedding",  # 嵌入后的新列名
                **document_raw_content_embed_config,  # 使用之前获取的嵌入配置
            },
        },
    ]

