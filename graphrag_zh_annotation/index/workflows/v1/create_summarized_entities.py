# 导入两个特殊的数据处理工具
from datashaper import AsyncType
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是微软公司的版权信息，表示代码由他们编写
# 并且遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个模块，里面有一个叫做build_steps的函数定义
# 模块的作用是创建步骤来整理提取出的实体信息

# 再次导入AsyncType，确保它在函数中可用
from datashaper import AsyncType

# 从graphrag.index.config中导入配置类和步骤类
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个工作流程的名字，叫"create_summarized_entities"
workflow_name = "create_summarized_entities"

# 定义一个函数，名为build_steps，它需要一个参数：config
# 函数返回值是一个列表，列表里的每个元素都是一个处理步骤
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数是用来创建一个总结了提取出的实体信息的基础表格。

    # 这里列出了函数依赖的其他任务
    * `workflow:create_base_text_units`
    """
    # 从config中获取"summarize_descriptions"的设置，如果没有就用空字典
    summarize_descriptions_config = config.get("summarize_descriptions", {})
    # 从config中获取"graphml_snapshot"的设置，如果为False或不存在，就直接设为False
    graphml_snapshot_enabled = config.get("graphml_snapshot", False) or False

    # 创建并返回一个包含两个步骤的列表
    return [
        # 第一步，总结描述
        {
            "verb": "summarize_descriptions",  # 动作名称
            "args": {  # 参数
                **summarize_descriptions_config,  # 使用之前获取的设置
                "column": "entity_graph",  # 操作的列名
                "to": "entity_graph",  # 结果保存的列名
                "async_mode": summarize_descriptions_config.get(
                    "async_mode", AsyncType.AsyncIO
                ),  # 异步模式，默认是AsyncIO
            },
            "input": {  # 输入来源
                "source": "workflow:create_base_extracted_entities",
            },
        },
        # 第二步，根据条件创建快照
        {
            "verb": "snapshot_rows",  # 动作名称
            "enabled": graphml_snapshot_enabled,  # 如果前面的条件为真，这一步才执行
            "args": {  # 参数
                "base_name": "summarized_graph",  # 快照的基本名字
                "column": "entity_graph",  # 快照的列名
                "formats": [  # 快照的格式
                    {"format": "text", "extension": "graphml"},  # 格式是文本，扩展名是.graphml
                ],
            },
        },
    ]

