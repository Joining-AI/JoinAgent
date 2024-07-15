# 从未来导入一个特性，用于在Python3.7及以下版本支持类型注解的更高级用法
from __future__ import annotations

# 导入一个类型，表示任何类型的值
from typing import Any

# 导入一个用于创建数据模型的库
from pydantic import BaseModel
# 从pydantic库中导入Field类，用于定义模型字段的特殊属性
from pydantic import Field as pydantic_Field

# 这是一个微软公司的版权声明
# Licensed under the MIT License

# 这个模块包含了'PipelineWorkflowReference'模型的定义

# 定义一个字典类型，键是字符串，值可以是任何类型，表示工作流中的一个步骤
PipelineWorkflowStep = dict[str, Any]
# "这是一个表示工作流中一步的数据结构"

# 定义一个字典类型，键是字符串，值可以是任何类型，表示工作流的配置信息
PipelineWorkflowConfig = dict[str, Any]
# "这是一个表示工作流配置的数据结构"

# 创建一个继承自BaseModel的类，表示工作流引用，也可以直接是工作流本身
class PipelineWorkflowReference(BaseModel):
    # 字段：工作流的名称，可以是空字符串，描述是工作流的名字，默认值是None
    name: str | None = pydantic_Field(description="工作流的名称。", default=None)
    
    # 字段：工作流的可选步骤列表，可以是空列表，描述是工作流的步骤，默认值是None
    steps: list[PipelineWorkflowStep] | None = pydantic_Field(
        description="工作流的可选步骤。", default=None
    )
    
    # 字段：工作流的可选配置信息，可以是空字典，描述是工作流的配置，默认值是None
    config: PipelineWorkflowConfig | None = pydantic_Field(
        description="工作流的可选配置。", default=None
    )

