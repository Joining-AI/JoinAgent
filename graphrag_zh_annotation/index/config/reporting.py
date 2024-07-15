# 导入一些Python库，这些库帮助我们定义和管理数据类型
from __future__ import annotations  # 让Python支持未来的注解语法
from typing import Generic, Literal, TypeVar  # 用于定义泛型类和特定类型的常量
from pydantic import BaseModel, Field as pydantic_Field  # 用于创建数据模型的库

# 导入自定义的枚举类型，它定义了报告类型
from graphrag.config.enums import ReportingType

# 这是微软公司的版权信息，表示代码由他们所有
# 并且遵循MIT许可证

# 这个模块包含关于报告配置的类
"""一个模块，里面包含了'PipelineReportingConfig', 'PipelineFileReportingConfig' 和 'PipelineConsoleReportingConfig' 类。"""

# 定义一个通用类型变量T，可以在多个类中使用
T = TypeVar("T")

# 定义一个基类，代表管道（pipeline）的报告配置
class PipelineReportingConfig(BaseModel, Generic[T]):
    """这个类描述了管道的报告配置设置。"""

    # 类中的一个属性，表示报告的类型，可以是任何类型T
    type: T

# 定义一个派生类，专门用于文件报告配置
class PipelineFileReportingConfig(PipelineReportingConfig[Literal[ReportingType.file]]):
    """这个类表示管道的文件报告配置。"""

    # 类属性，报告类型必须是'file'
    type: Literal[ReportingType.file] = ReportingType.file
    """报告的类型是文件报告。"""

    # 类属性，指定报告的基础目录，可以是字符串或None
    base_dir: str | None = pydantic_Field(
        description="用于报告的根目录，默认为None。",
        default=None
    )
    """报告的基础目录，如果没有设置，则默认为None。"""

# 定义另一个派生类，专门用于控制台报告配置
class PipelineConsoleReportingConfig(
    PipelineReportingConfig[Literal[ReportingType.console]]
):
    """这个类表示管道的控制台报告配置。"""

    # 类属性，报告类型必须是'console'
    type: Literal[ReportingType.console] = ReportingType.console
    """报告的类型是控制台报告。"""

# 定义一个名为PipelineBlobReportingConfig的类，它是PipelineReportingConfig的子类，其中ReportingType.blob是类型参数
class PipelineBlobReportingConfig(PipelineReportingConfig[Literal[ReportingType.blob]]):
    # 这个类是用来表示管道的blob（存储块）报告配置
    """Represents the blob reporting configuration for the pipeline."""

    # 定义一个变量type，它的值是ReportingType.blob，表示报告的类型
    type: Literal[ReportingType.blob] = ReportingType.blob
    # 这个变量说明了报告的类型

    # 定义一个变量connection_string，它可能是字符串或None，用于存储报告的blob连接字符串
    connection_string: str | None = pydantic_Field(
        description="The blob reporting connection string for the reporting.",
        default=None,
    )
    # 这个变量是报告用的blob连接字符串

    # 定义一个变量container_name，它是个字符串，用于存储报告的容器名称
    container_name: str = pydantic_Field(
        description="The container name for reporting", default=None
    )
    # 这个变量是报告用的容器名称

    # 定义一个变量storage_account_blob_url，它可能是字符串或None，用于存储报告的存储账户blob URL
    storage_account_blob_url: str | None = pydantic_Field(
        description="The storage account blob url for reporting", default=None
    )
    # 这个变量是报告用的存储账户blob URL

    # 定义一个变量base_dir，它可能是字符串或None，用于存储报告的基础目录
    base_dir: str | None = pydantic_Field(
        description="The base directory for the reporting.", default=None
    )
    # 这个变量是报告的基础目录

# 定义一个名为PipelineReportingConfigTypes的变量，它是一个联合类型，包含PipelineFileReportingConfig, PipelineConsoleReportingConfig和PipelineBlobReportingConfig
PipelineReportingConfigTypes = (
    PipelineFileReportingConfig
    | PipelineConsoleReportingConfig
    | PipelineBlobReportingConfig
)

