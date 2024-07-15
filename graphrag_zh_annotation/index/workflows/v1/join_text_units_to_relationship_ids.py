# 导入两个来自graphrag.index.config的类：PipelineWorkflowConfig和PipelineWorkflowStep
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这个代码是微软公司写的，并遵循MIT许可证
# 注释：这是一个包含build_steps方法定义的模块

# 定义一个工作流程的名称，叫做"join_text_units_to_relationship_ids"
workflow_name = "join_text_units_to_relationship_ids"

# 定义一个函数，名为build_steps，它接受一个PipelineWorkflowConfig类型的参数，并返回一个PipelineWorkflowStep类型的列表
def build_steps(_config: PipelineWorkflowConfig) -> list[PipelineWorkflowStep]:
    """
    创建一个表格，将文本单位ID与关系ID连接起来。

    ### 依赖项
    * 需要先运行的工作流程："workflow:create_final_relationships"
    """
    # 返回一系列步骤，每个步骤都是一个字典，描述了要执行的操作
    return [
        # 第一步：选择数据，只保留"id"和"text_unit_ids"两列
        {
            "verb": "select",  # 表示我们要进行选择操作
            "args": {"columns": ["id", "text_unit_ids"]},  # 选择的列
            "input": {"source": "workflow:create_final_relationships"},  # 输入数据来自哪个工作流程
        },
        # 第二步：展开数据，把"text_unit_ids"列中的列表拆分成多行
        {
            "verb": "unroll",  # 表示我们要进行展开操作
            "args": {
                "column": "text_unit_ids",  # 要展开的列
            },
        },
        # 第三步：聚合数据，按"text_unit_ids"分组，创建新的列"relationship_ids"和"id"
        {
            "verb": "aggregate_override",  # 表示我们要进行聚合操作
            "args": {
                "groupby": ["text_unit_ids"],  # 按哪一列分组
                "aggregations": [  # 聚合操作的规则
                    {
                        "column": "id",  # 原始列
                        "operation": "array_agg_distinct",  # 操作：获取唯一值的数组
                        "to": "relationship_ids",  # 新列名
                    },
                    {
                        "column": "text_unit_ids",  # 原始列
                        "operation": "any",  # 操作：取任何值（用于创建新"id"列）
                        "to": "id",  # 新列名
                    },
                ],
            },
        },
        # 第四步：再次选择数据，只保留"id"和"relationship_ids"两列
        {
            "id": "text_unit_id_to_relationship_ids",  # 步骤的唯一标识
            "verb": "select",
            "args": {"columns": ["id", "relationship_ids"]},
        },
    ]

