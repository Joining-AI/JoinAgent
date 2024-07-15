# 导入两个类：PipelineWorkflowConfig 和 PipelineWorkflowStep，它们来自 graphrag.index.config 模块。
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司2024年的版权信息，它遵循MIT许可证。
# 注释：这是法律声明，告诉别人代码的所有权和使用许可。

# 定义一个模块，里面有一个方法 build_steps。
# 这个模块是用来创建数据处理步骤的。

from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个工作流程的名字，叫 "join_text_units_to_entity_ids"。
workflow_name = "join_text_units_to_entity_ids"

# 定义一个函数 build_steps，它接受一个参数 _config（类型是 PipelineWorkflowConfig）
# 函数会返回一个列表，列表里的每个元素都是 PipelineWorkflowStep 类型。
def build_steps(_config: PipelineWorkflowConfig) -> list[PipelineWorkflowStep]:
    """
    这个函数的作用是创建一个表，把文本单元ID和实体ID连接起来。

    ### 需要依赖的工作流程
    * `workflow:create_final_entities`
    """
    # 返回一系列的操作步骤，这些步骤会按顺序执行：
    return [
        # 第一步：选择数据
        {
            "verb": "select",  # 动作是"选择"
            "args": {"columns": ["id", "text_unit_ids"]},  # 选择"id"和"text_unit_ids"两列
            "input": {"source": "workflow:create_final_entities"},  # 输入数据来源于之前的工作流程"create_final_entities"
        },
        # 第二步：展开数据
        {
            "verb": "unroll",  # 动作是"展开"
            "args": {
                "column": "text_unit_ids",  # 对"text_unit_ids"列进行操作
            },
        },
        # 第三步：聚合并替换数据
        {
            "verb": "aggregate_override",  # 动作是"聚合并替换"
            "args": {
                "groupby": ["text_unit_ids"],  # 根据"text_unit_ids"分组
                "aggregations": [  # 聚合操作列表
                    {
                        "column": "id",  # 对"id"列
                        "operation": "array_agg_distinct",  # 使用"去重数组聚合"操作
                        "to": "entity_ids",  # 结果保存在新列"entity_ids"
                    },
                    {
                        "column": "text_unit_ids",  # 对"text_unit_ids"列
                        "operation": "any",  # 使用"取任意值"操作
                        "to": "id",  # 结果保存在新列"id"
                    },
                ],
            },
        },
    ]

