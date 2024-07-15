# 导入未来的注解功能，这在Python 3.7及以后版本中允许在定义函数时直接添加类型注解
from __future__ import annotations

# 导入cast函数，用于安全地将对象转换为特定类型
from typing import cast

# 导入StorageType枚举，它定义了存储的三种类型：内存、Blob（云存储）和文件
from graphrag.config import StorageType

# 从graphrag.index.config.storage模块导入与存储配置相关的类
from graphrag.index.config.storage import (
    PipelineBlobStorageConfig,
    PipelineFileStorageConfig,
    PipelineStorageConfig,
)

# 从当前模块的子模块导入创建不同类型存储的方法
from .blob_pipeline_storage import create_blob_storage
from .file_pipeline_storage import create_file_storage
from .memory_pipeline_storage import create_memory_storage

# 这是一个由微软公司创作的代码，遵循MIT许可证
# """这是一个包含load_storage方法定义的模块。"""

# 定义load_storage函数，它接收一个PipelineStorageConfig对象作为参数
def load_storage(config: PipelineStorageConfig):
    # 根据传入配置的类型加载相应的存储
    # 使用match...case结构进行类型匹配
    match config.type:
        # 如果类型是内存存储
        case StorageType.memory:
            # 创建并返回内存存储
            return create_memory_storage()
        # 如果类型是Blob存储
        case StorageType.blob:
            # 安全地将config转换为PipelineBlobStorageConfig类型
            config = cast(PipelineBlobStorageConfig, config)
            # 使用Blob存储的配置信息创建并返回Blob存储
            return create_blob_storage(
                config.connection_string,  # 连接字符串
                config.storage_account_blob_url,  # 存储账户的Blob URL
                config.container_name,  # 容器名称
                config.base_dir,  # 基本目录
            )
        # 如果类型是文件存储
        case StorageType.file:
            # 安全地将config转换为PipelineFileStorageConfig类型
            config = cast(PipelineFileStorageConfig, config)
            # 使用文件存储的配置信息创建并返回文件存储
            return create_file_storage(config.base_dir)  # 基本目录
        # 如果遇到未知的存储类型
        case _:
            # 构造错误消息，包括未知的存储类型
            msg = f"Unknown storage type: {config.type}"
            # 抛出一个ValueError异常
            raise ValueError(msg)

