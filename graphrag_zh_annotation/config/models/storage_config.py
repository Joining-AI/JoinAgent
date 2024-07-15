# 导入一个叫做 BaseModel 和 Field 的工具，它们来自 pydantic 库，帮助我们定义数据模型
from pydantic import BaseModel, Field

# 导入默认设置模块，它在 graphrag.config.defaults 中
import graphrag.config.defaults as defs

# 导入枚举类型 StorageType，它在 graphrag.config.enums 中
from graphrag.config.enums import StorageType

# 这是微软公司的版权声明，告诉我们代码的版权信息和使用的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个配置参数类，用于存储相关设置
class StorageConfig(BaseModel):
    # 这个类是基于 BaseModel 创建的，它有一个名为 'type' 的属性
    # 'type' 是 StorageType 类型的，描述了要使用的存储类型
    type: StorageType = Field(description="存储类型", default=defs.STORAGE_TYPE)

    # 'base_dir' 属性是字符串类型，表示存储的基础目录
    # 默认值来自 graphrag.config.defaults 的 STORAGE_BASE_DIR
    base_dir: str = Field(description="存储的基础目录", default=defs.STORAGE_BASE_DIR)

    # 'connection_string' 可能是字符串，也可能为空，表示存储连接字符串
    # 默认值为 None
    connection_string: str | None = Field(description="存储连接字符串", default=None)

    # 'container_name' 也是可能有或没有的字符串，表示存储容器的名字
    # 默认值也为 None
    container_name: str | None = Field(description="存储容器名称", default=None)

    # 'storage_account_blob_url' 同样可能是字符串或为空，用于存储账户的 Blob URL
    # 默认值同样为 None
    storage_account_blob_url: str | None = Field(description="存储账户 Blob URL", default=None)

