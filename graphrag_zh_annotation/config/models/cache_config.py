# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们定义数据结构
from pydantic import BaseModel, Field

# 导入一些默认设置，它们在graphrag.config.defaults模块中
import graphrag.config.defaults as defs

# 从graphrag.config.enums导入一个叫做CacheType的枚举类型，它包含关于缓存类型的选项
from graphrag.config.enums import CacheType

# 这是一个版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为"参数化设置"的文档字符串，描述了这个配置文件的作用
"""参数化设置，用于默认配置。"""

# 创建一个继承自BaseModel的类，叫做CacheConfig，用来存储有关缓存的配置信息
class CacheConfig(BaseModel):

    # 定义一个属性，类型是CacheType，描述是“要使用的缓存类型”，默认值在defs.CACHE_TYPE中找到
    type: CacheType = Field(description="要使用的缓存类型。", default=defs.CACHE_TYPE)

    # 定义一个属性，类型是字符串，描述是“缓存的基础目录”，默认值在defs.CACHE_BASE_DIR中找到
    base_dir: str = Field(description="缓存的基础目录。", default=defs.CACHE_BASE_DIR)

    # 定义一个属性，类型可以是字符串或None，描述是“缓存的连接字符串”，默认值是None
    connection_string: str | None = Field(description="要使用的缓存连接字符串。", default=None)

    # 定义一个属性，类型可以是字符串或None，描述是“缓存容器的名字”，默认值是None
    container_name: str | None = Field(description="要使用的缓存容器名。", default=None)

    # 定义一个属性，类型可以是字符串或None，描述是“存储账户的Blob URL”，默认值是None
    storage_account_blob_url: str | None = Field(description="要使用的存储账户Blob URL。", default=None)

