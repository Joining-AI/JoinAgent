# 导入一些特殊的功能，让代码在未来版本的Python中也能正常工作
from __future__ import annotations

# 导入不同类型的工具，帮助我们定义数据模型
from typing import Generic, Literal, TypeVar

# 导入一个用于创建数据模型的库
from pydantic import BaseModel
# 从pydantic库中导入一个特殊字段，用于设置模型的属性
from pydantic import Field as pydantic_Field

# 导入一个包含缓存类型枚举的模块
from graphrag.config.enums import CacheType

# 定义一个通用类型变量T，可以代表任何类型的数据
T = TypeVar("T")

# 这个文件包含了关于管道（pipeline）缓存配置的类

# 定义一个基类，它是一个数据模型，可以存储任何类型T的缓存配置信息
class PipelineCacheConfig(BaseModel, Generic[T]):
    # 存储缓存类型的属性
    type: T
    # 这个类表示管道的缓存配置

# 定义一个子类，专门用于文件缓存配置
class PipelineFileCacheConfig(PipelineCacheConfig[Literal[CacheType.file]]):
    # 文件缓存的类型，固定为'file'
    type: Literal[CacheType.file] = CacheType.file
    # 描述：这是哪种类型的缓存

    # 缓存的根目录，可能为空
    base_dir: str | None = pydantic_Field(
        description="缓存的根目录。", default=None
    )
    # 描述：这是缓存的根目录

# 定义一个子类，专门用于内存缓存配置
class PipelineMemoryCacheConfig(PipelineCacheConfig[Literal[CacheType.memory]]):
    # 内存缓存的类型，固定为'memory'
    type: Literal[CacheType.memory] = CacheType.memory
    # 描述：这是哪种类型的缓存

# 定义一个子类，专门用于无缓存配置
class PipelineNoneCacheConfig(PipelineCacheConfig[Literal[CacheType.none]]):
    # 无缓存的类型，固定为'none'
    type: Literal[CacheType.none] = CacheType.none
    # 描述：这是哪种类型的缓存

# 定义一个名为PipelineBlobCacheConfig的类，它是PipelineCacheConfig类的一个子类，参数类型是Literal[CacheType.blob]
class PipelineBlobCacheConfig(PipelineCacheConfig[Literal[CacheType.blob]]):
    # 这个类代表的是管道（pipeline）的blob缓存配置
    """Represents the blob cache configuration for the pipeline."""

    # 定义一个变量type，它的值是CacheType.blob，表示缓存的类型
    type: Literal[CacheType.blob] = CacheType.blob
    # 对这个变量的注释，说明它表示的是缓存的类型
    """The type of cache."""

    # 定义一个变量base_dir，它的类型是字符串或者None，初始值是None
    base_dir: str | None = pydantic_Field(
        # 这个变量描述的是缓存的基目录
        description="The base directory for the cache.", default=None
    )
    # 对这个变量的注释，说明它是缓存的基目录
    """The base directory for the cache."""

    # 定义一个变量connection_string，它的类型是字符串或者None，初始值是None
    connection_string: str | None = pydantic_Field(
        # 这个变量描述的是用于缓存的blob连接字符串
        description="The blob cache connection string for the cache.", default=None
    )
    # 对这个变量的注释，说明它是缓存的blob连接字符串
    """The blob cache connection string for the cache."""

    # 定义一个变量container_name，它的类型是字符串，初始值是None
    container_name: str = pydantic_Field(
        # 这个变量描述的是缓存的容器名称
        description="The container name for cache", default=None
    )
    # 对这个变量的注释，说明它是缓存的容器名称
    """The container name for cache"""

    # 定义一个变量storage_account_blob_url，它的类型是字符串或者None，初始值是None
    storage_account_blob_url: str | None = pydantic_Field(
        # 这个变量描述的是用于缓存的存储账户blob URL
        description="The storage account blob url for cache", default=None
    )
    # 对这个变量的注释，说明它是缓存的存储账户blob URL
    """The storage account blob url for cache"""


# 定义一个元组PipelineCacheConfigTypes，包含四种不同的缓存配置类型
PipelineCacheConfigTypes = (
    PipelineFileCacheConfig  # 文件缓存配置
    | PipelineMemoryCacheConfig  # 内存缓存配置
    | PipelineBlobCacheConfig  # Blob缓存配置
    | PipelineNoneCacheConfig  # 无缓存配置
)

