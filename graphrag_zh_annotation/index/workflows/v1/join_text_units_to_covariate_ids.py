# 导入两个类：PipelineWorkflowConfig 和 PipelineWorkflowStep，它们来自 graphrag.index.config 模块。
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是一个微软公司的代码，遵循 MIT 许可证。
# 注释：这部分是版权信息，表示代码的所有权和使用的许可协议。

# 定义一个模块，里面有一个方法 build_steps。
# 这个模块的目的是创建一个步骤列表，用于处理数据。

# 定义一个工作流程的名称，叫 "join_text_units_to_covariate_ids"。
workflow_name = "join_text_units_to_covariate_ids"

# 定义一个函数 build_steps，它接收一个参数 _config（类型是 PipelineWorkflowConfig）
# 函数返回值是一个列表，列表里的每个元素都是 PipelineWorkflowStep 类型。
def build_steps(
    _config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数的作用是创建最终的文本单元表。

    # 依赖项
    * 需要先运行 'workflow:create_final_covariates' 步骤
    """
    # 创建一个步骤列表，包含两个操作
    steps_list = [
        # 第一步：选择数据
        {
            "verb": "select",  # 表示我们要执行的选择操作
            "args": {"columns": ["id", "text_unit_id"]},  # 选择 "id" 和 "text_unit_id" 列
            "input": {"source": "workflow:create_final_covariates"},  # 输入来源于之前的工作流程步骤
        },
        # 第二步：聚合数据并覆盖
        {
            "verb": "aggregate_override",  # 表示我们要执行的聚合操作
            "args": {
                "groupby": ["text_unit_id"],  # 根据 "text_unit_id" 进行分组
                "aggregations": [  # 聚合操作的列表
                    {
                        "column": "id",  # 对 "id" 列进行操作
                        "operation": "array_agg_distinct",  # 使用数组去重聚合
                        "to": "covariate_ids",  # 结果存储在新的列 "covariate_ids" 中
                    },
                    {
                        "column": "text_unit_id",  # 对 "text_unit_id" 列进行操作
                        "operation": "any",  # 取任何值（通常是最先出现的值）
                        "to": "id",  # 结果存储回 "id" 列
                    },
                ],
            },
        },
    ]
    # 返回步骤列表
    return steps_list

