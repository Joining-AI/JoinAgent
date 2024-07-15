# 这段代码是用来定义一个叫做 'PipelineConfig' 的模型的。让我们一步步看它是怎么工作的。

# 第一行导入了一个未来的特性，叫做 "annotations"，它帮助我们更好地处理函数和类的注解。
from __future__ import annotations

# 导入了一个叫做 'pformat' 的工具，它来自 'devtools' 模块，用于格式化（美化）输出的 Python 对象。
from devtools import pformat

# 导入了 'BaseModel' 和 'Field'，它们来自 'pydantic' 模块，用于创建数据模型和定义模型字段。
from pydantic import BaseModel, Field as pydantic_Field

# 这里从不同的模块导入了一些配置类型，比如缓存、输入、报告和存储，这些都是用来设置管道（pipeline）的。
from .cache import PipelineCacheConfigTypes
from .input import PipelineInputConfigTypes
from .reporting import PipelineReportingConfigTypes
from .storage import PipelineStorageConfigTypes

# 最后，从 '.workflow' 模块中导入了 'PipelineWorkflowReference'，这可能是用来引用工作流的部分。
from .workflow import PipelineWorkflowReference

# 这是版权声明，告诉我们这个代码是由微软公司在2024年写的，并且遵循 MIT 许可证。
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块包含的是 'PipelineConfig' 模型。
# 注意：文档字符串是用三对引号包围的，可以用来解释代码的作用。
"""
A module containing 'PipelineConfig' model.
"""

# 定义一个名为PipelineConfig的类，它继承自BaseModel
class PipelineConfig(BaseModel):
    # 这个类是用来表示管道（pipeline）的配置信息
    """Represent the configuration for a pipeline."""

    # 当打印这个类的对象时，返回一个格式化的字符串表示
    def __repr__(self) -> str:
        """获取一个字符串表示形式。"""
        return pformat(self, highlight=False)

    # 当使用str()函数转换这个类的对象时，返回一个易于阅读的字符串
    def __str__(self):
        """获取一个字符串表示形式。"""
        return str(self.model_dump_json(indent=4))

    # 声明一个变量'extends'，它可以是一个字符串列表、单个字符串或None
    # 这个变量用来表示当前管道配置是否扩展了其他配置
    extends: list[str] | str | None = pydantic_Field(
        description="扩展另一个管道配置", default=None
    )
    """扩展另一个管道配置"""

    # 声明一个变量'input'，它可以是PipelineInputConfigTypes类型或None
    # 这个变量表示管道的输入配置
    input: PipelineInputConfigTypes | None = pydantic_Field(
        default=None, discriminator="file_type"
    )
    """管道的输入配置"""

    # 声明一个变量'reporting'，它可以是PipelineReportingConfigTypes类型或None
    # 这个变量表示管道的报告配置
    reporting: PipelineReportingConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """管道的报告配置"""

    # 声明一个变量'storage'，它可以是PipelineStorageConfigTypes类型或None
    # 这个变量表示管道的存储配置
    storage: PipelineStorageConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """管道的存储配置"""

    # 声明一个变量'cache'，它可以是PipelineCacheConfigTypes类型或None
    # 这个变量表示管道的缓存配置
    cache: PipelineCacheConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """管道的缓存配置"""

    # 声明一个变量'root_dir'，它可以是一个字符串或None
    # 这个变量表示管道的根目录，其他路径都基于这个根目录
    root_dir: str | None = pydantic_Field(
        description="管道的根目录，所有其他路径都基于此根目录。",
        default=None,
    )
    """管道的根目录"""

    # 声明一个变量'workflows'，它是一个PipelineWorkflowReference类型的列表
    # 使用default_factory=list确保它总是列表，即使没有初始值
    # 这个变量表示管道的工作流程
    workflows: list[PipelineWorkflowReference] = pydantic_Field(
        description="管道的工作流程。",
        default_factory=list
    )
    """管道的工作流程"""

