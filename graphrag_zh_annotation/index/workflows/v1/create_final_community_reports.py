# 导入两个特殊的东西，它们来自graphrag.index.config这个大箱子里
# PipelineWorkflowConfig是用来设置工作流程配置的类
# PipelineWorkflowStep是用来描述工作流程中的每一步的类
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是一段法律条文，意思是这个代码是微软公司在2024年写的
# 并且它遵循MIT许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这里写了一个描述，告诉我们这个文件里有一个叫做build_steps的方法
# 注释是用来帮助理解代码的
"""A module containing build_steps method definition."""

# 从graphrag.index.config再导入同样的两个类，虽然重复但很重要
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个变量，叫workflow_name
# 它的值是"create_final_community_reports"
# 这个名字可能是某个工作流程的名字
workflow_name = "create_final_community_reports"

# 定义一个名为 build_steps 的函数，它接收一个名为 config 的参数
def build_steps(
    config: PipelineWorkflowConfig,  # 这是一个配置对象，包含了流程中的设置
) -> list[PipelineWorkflowStep]:  # 函数返回值是一个步骤列表，每个步骤都是 PipelineWorkflowStep 类型

    """
    创建最终的社区报告表格。

    这个函数依赖于其他两个步骤：`workflow:create_base_entity_graph`
    """
    
    # 获取 config 中的 "covariates_enabled" 参数，如果不存在则默认为 False
    covariates_enabled = config.get("covariates_enabled", False)
    
    # 获取 config 中的 "create_community_reports" 配置，如果不存在则返回一个空字典
    create_community_reports_config = config.get("create_community_reports", {})

    # 获取 config 中的 "text_embed" 配置，如果不存在则返回一个空字典
    base_text_embed = config.get("text_embed", {})

    # 获取 config 中的 "community_report_full_content_embed" 配置，如果不存在则使用 base_text_embed
    community_report_full_content_embed_config = config.get(
        "community_report_full_content_embed", base_text_embed
    )

    # 获取 config 中的 "community_report_summary_embed" 配置，如果不存在则使用 base_text_embed
    community_report_summary_embed_config = config.get(
        "community_report_summary_embed", base_text_embed
    )

    # 获取 config 中的 "community_report_title_embed" 配置，如果不存在则使用 base_text_embed
    community_report_title_embed_config = config.get(
        "community_report_title_embed", base_text_embed
    )

    # 获取 config 中的 "skip_title_embedding" 参数，如果不存在则默认为 False
    skip_title_embedding = config.get("skip_title_embedding", False)

    # 获取 config 中的 "skip_summary_embedding" 参数，如果不存在则默认为 False
    skip_summary_embedding = config.get("skip_summary_embedding", False)

    # 获取 config 中的 "skip_full_content_embedding" 参数，如果不存在则默认为 False
    skip_full_content_embedding = config.get("skip_full_content_embedding", False)

    # 创建并返回一个包含多个子工作流步骤的列表
    return [
        # 子工作流：准备节点
        {
            "id": "nodes",  # 步骤的唯一标识
            "verb": "prepare_community_reports_nodes",  # 步骤要执行的操作
            "input": {"source": "workflow:create_final_nodes"},  # 输入来源
        },
        # 子工作流：准备边
        {
            "id": "edges",
            "verb": "prepare_community_reports_edges",
            "input": {"source": "workflow:create_final_relationships"},
        },
        # 子工作流：准备声明表（只有当 covariates_enabled 为真时才会执行）
        {
            "id": "claims",
            "enabled": covariates_enabled,
            "verb": "prepare_community_reports_claims",
            "input": {
                "source": "workflow:create_final_covariates",
            } if covariates_enabled else {},
        },
        # 子工作流：获取社区层级结构
        {
            "id": "community_hierarchy",
            "verb": "restore_community_hierarchy",
            "input": {"source": "nodes"},
        },
        # 主工作流：创建社区报告
        {
            "id": "local_contexts",
            "verb": "prepare_community_reports",
            "input": {
                "source": "nodes",
                "nodes": "nodes",
                "edges": "edges",
                **({"claims": "claims"} if covariates_enabled else {}),
            },
        },
        # 创建社区报告
        {
            "verb": "create_community_reports",
            "args": {
                **create_community_reports_config,
            },
            "input": {
                "source": "local_contexts",
                "community_hierarchy": "community_hierarchy",
                "nodes": "nodes",
            },
        },
        # 为每个社区报告生成唯一的 ID，区别于社区 ID
        {
            "verb": "window",
            "args": {"to": "id", "operation": "uuid", "column": "community"},
        },
        # 如果不跳过全文内容嵌入，执行文本嵌入
        {
            "verb": "text_embed",
            "enabled": not skip_full_content_embedding,
            "args": {
                "embedding_name": "community_report_full_content",
                "column": "full_content",
                "to": "full_content_embedding",
                **community_report_full_content_embed_config,
            },
        },
        # 如果不跳过摘要嵌入，执行文本嵌入
        {
            "verb": "text_embed",
            "enabled": not skip_summary_embedding,
            "args": {
                "embedding_name": "community_report_summary",
                "column": "summary",
                "to": "summary_embedding",
                **community_report_summary_embed_config,
            },
        },
        # 如果不跳过标题嵌入，执行文本嵌入
        {
            "verb": "text_embed",
            "enabled": not skip_title_embedding,
            "args": {
                "embedding_name": "community_report_title",
                "column": "title",
                "to": "title_embedding",
                **community_report_title_embed_config,
            },
        },
    ]

