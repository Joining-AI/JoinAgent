# 导入两个特殊类型的模块，帮助我们定义数据结构
from typing_extensions import NotRequired, TypedDict
# 导入一个枚举类型，它包含报告类型的信息
from graphrag.config.enums import ReportingType

# 这一行是版权信息，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文档字符串描述了这段代码的作用，它是关于默认配置的参数设置
"""
Parameterization settings for the default configuration.
"""

# 再次导入NotRequired和TypedDict，确保它们在类定义时可用
from typing_extensions import NotRequired, TypedDict

# 导入报告类型的枚举类
from graphrag.config.enums import ReportingType

# 定义一个名为ReportingConfigInput的类，它是基于TypedDict的
class ReportingConfigInput(TypedDict):
    # 这个类是用来存储报告相关的配置信息的
    """The default configuration section for Reporting."""
    
    # 下面是类中定义的键值对，每个键都有一个类型
    # type: 可选的ReportingType、字符串或None
    type: NotRequired[ReportingType | str | None]
    
    # base_dir: 可选的字符串或None
    base_dir: NotRequired[str | None]
    
    # connection_string: 可选的字符串或None
    connection_string: NotRequired[str | None]
    
    # container_name: 可选的字符串或None
    container_name: NotRequired[str | None]
    
    # storage_account_blob_url: 可选的字符串或None
    storage_account_blob_url: NotRequired[str | None]

