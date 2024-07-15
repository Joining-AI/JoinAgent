# 导入一个叫做BaseModel和Field的工具，它们帮助我们定义数据结构
from pydantic import BaseModel, Field

# 导入默认设置的模块
import graphrag.config.defaults as defs

# 导入一个枚举类型ReportingType，它包含一些报告类型的选项
from graphrag.config.enums import ReportingType

# 这是一个版权信息，告诉我们这段代码是微软公司的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个类，叫做ReportingConfig，它继承自BaseModel
class ReportingConfig(BaseModel):
    # 这个类是用来存储关于报告的默认配置的

    # 定义一个属性，叫做'type'，它是一个ReportingType，描述了要使用的报告类型
    # 默认值来自defs模块的REPORTING_TYPE
    type: ReportingType = Field(description="要使用的报告类型。", default=defs.REPORTING_TYPE)

    # 定义一个属性，叫做'base_dir'，它是一个字符串，描述了报告的基础目录
    # 默认值来自defs模块的REPORTING_BASE_DIR
    base_dir: str = Field(description="报告的基础目录。", default=defs.REPORTING_BASE_DIR)

    # 定义一个属性，叫做'connection_string'，它可能是一个字符串，也可能为空
    # 描述了报告用到的连接字符串，默认为空
    connection_string: str | None = Field(description="报告用的连接字符串。", default=None)

    # 定义一个属性，叫做'container_name'，它可能是一个字符串，也可能为空
    # 描述了报告用到的容器名称，默认为空
    container_name: str | None = Field(description="报告用的容器名称。", default=None)

    # 定义一个属性，叫做'storage_account_blob_url'，它可能是一个字符串，也可能为空
    # 描述了存储账户的blob网址，默认为空
    storage_account_blob_url: str | None = Field(description="存储账户的blob网址。", default=None)

