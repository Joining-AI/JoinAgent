# 导入两个特殊的东西，它们来自graphrag.index.config这个大箱子里
# PipelineWorkflowConfig和PipelineWorkflowStep是两个工具，帮我们管理工作的流程
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权所有信息
# 并且他们同意让我们用这个代码，只要我们遵守MIT许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这里写了一个描述，告诉我们这个文件是用来干什么的
# 它包含了一个叫做build_steps的方法定义
"""
A module containing build_steps method definition.
"""

# 继续从graphrag.index.config导入我们需要的东西
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 我们要定义一个工作流程的名字，叫做"create_final_communities"
workflow_name = "create_final_communities"

# 定义一个名为 build_steps 的函数，它接收一个名为 _config 的参数
def build_steps(_config: PipelineWorkflowConfig) -> list[PipelineWorkflowStep]:
    """
    这个函数创建最终的社区表格。

    依赖：
    * 'workflow:create_base_entity_graph'
    """
    # 返回一个步骤列表
    return [
        # 第一步：从数据中解包节点信息
        {
            "id": "graph_nodes",  # 步骤ID
            "verb": "unpack_graph",  # 执行的动作
            "args": {  # 参数
                "column": "clustered_graph",  # 解包的列名
                "type": "nodes",  # 类型是节点
            },
            "input": {  # 输入来源
                "source": "workflow:create_base_entity_graph",
            },
        },
        # 第二步：解包边（连接）信息
        {
            "id": "graph_edges",
            "verb": "unpack_graph",
            "args": {
                "column": "clustered_graph",
                "type": "edges",
            },
            "input": {
                "source": "workflow:create_base_entity_graph",
            },
        },
        # 第三步：将节点和边按标签和源连接
        {
            "id": "source_clusters",
            "verb": "join",
            "args": {
                "on": ["label", "source"],
            },
            "input": {
                "source": "graph_nodes",
                "others": ["graph_edges"],
            },
        },
        # 第四步：按标签和目标连接
        {
            "id": "target_clusters",
            "verb": "join",
            "args": {
                "on": ["label", "target"],
            },
            "input": {
                "source": "graph_nodes",
                "others": ["graph_edges"],
            },
        },
        # 第五步：将第三步和第四步的结果合并
        {
            "id": "concatenated_clusters",
            "verb": "concat",
            "input": {
                "source": "source_clusters",
                "others": ["target_clusters"],
            },
        },
        # 第六步：过滤合并后的结果，找到匹配的行
        {
            "id": "combined_clusters",
            "verb": "filter",
            "args": {
                # 检查左右两边的连接是否相等
                "column": "level_1",
                "criteria": [
                    {"type": "column", "operator": "equals", "value": "level_2"}
                ],
            },
            "input": {
                "source": "concatenated_clusters",
            },
        },
        # 第七步：按集群和连接类型聚合，收集关系和文本单元ID
        {
            "id": "cluster_relationships",
            "verb": "aggregate_override",
            "args": {
                "groupby": ["cluster", "level_1"],  # 分组依据
                "aggregations": [
                    # 聚合操作
                    {
                        "column": "id_2",  # 边的ID
                        "to": "relationship_ids",
                        "operation": "array_agg_distinct",
                    },
                    {
                        "column": "source_id_1",
                        "to": "text_unit_ids",
                        "operation": "array_agg_distinct",
                    },
                ],
            },
            "input": {
                "source": "combined_clusters",
            },
        },
        # 第八步：按集群和级别聚合，收集集群ID
        {
            "id": "all_clusters",
            "verb": "aggregate_override",
            "args": {
                "groupby": ["cluster", "level"],
                "aggregations": [
                    {"column": "cluster", "to": "id", "operation": "any"}
                ],
            },
            "input": {
                "source": "graph_nodes",
            },
        },
        # 第九步：将第八步和第七步的结果按ID和集群连接
        {
            "verb": "join",
            "args": {
                "on": ["id", "cluster"],
            },
            "input": {
                "source": "all_clusters",
                "others": ["cluster_relationships"],
            },
        },
        # 第十步：过滤连接结果，确保级别匹配
        {
            "verb": "filter",
            "args": {
                "column": "level",
                "criteria": [
                    {"type": "column", "operator": "equals", "value": "level_1"}
                ],
            },
        },
        # 待办事项：Rodrigo说"raw_community"是临时的
        *create_community_title_wf,  # 这里会调用另一个函数或列表
        {
            "verb": "copy",  # 复制列
            "args": {
                "column": "id",
                "to": "raw_community",
            },
        },
        # 选择最终需要的列
        {
            "verb": "select",
            "args": {
                "columns": [
                    "id",
                    "title",
                    "level",
                    "raw_community",
                    "relationship_ids",
                    "text_unit_ids",
                ],
            },
        },
    ]

# 这段代码是用来创建一个列表，列表里的每个元素都是一个字典，这些字典描述了如何操作数据

create_community_title_wf = [  # 创建一个叫 "create_community_title_wf" 的列表
    # 下面的字典表示一个步骤，它的任务是添加字符串 "Community " 到数据中
    {
        "verb": "fill",  # 行动是 "填充"
        "args": {  # 这里是行动的具体参数
            "to": "__temp",  # 填充的目标是一个临时字段 "__temp"
            "value": "Community ",  # 要填充的值是 "Community "
        },
    },
    # 下面的字典表示另一个步骤，它的任务是将 "Community " 和 "id" 合并成一个新的标题
    {
        "verb": "merge",  # 行动是 "合并"
        "args": {  # 这里是行动的具体参数
            "columns": [  # 要合并的列，一个是 "__temp"，另一个是 "id"
                "__temp",
                "id",
            ],
            "to": "title",  # 合并后的结果保存在新的列 "title" 中
            "strategy": "concat",  # 合并策略是 "连接"（把两个列的内容连在一起）
            "preserveSource": True,  # 保留原始数据，不让它们被删除
        },
    },
]

