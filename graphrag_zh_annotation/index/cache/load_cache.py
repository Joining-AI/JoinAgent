# 导入未来的注解功能，让Python3.7及以下版本支持一些新特性
from __future__ import annotations

# 导入检查类型的模块，用于类型注解
from typing import TYPE_CHECKING, cast

# 导入自定义的枚举类型，关于缓存类型
from graphrag.config.enums import CacheType

# 从graphrag.index.config.cache模块导入两个缓存配置类
from graphrag.index.config.cache import PipelineBlobCacheConfig, PipelineFileCacheConfig

# 从graphrag.index.storage模块导入两个存储类，分别对应Blob和文件
from graphrag.index.storage import BlobPipelineStorage, FilePipelineStorage

# 导入内部模块，用于JSON格式的缓存
from .json_pipeline_cache import JsonPipelineCache

# 导入内存缓存的创建函数
from .memory_pipeline_cache import create_memory_cache

# 导入无操作缓存类，作为默认或测试使用
from .noop_pipeline_cache import NoopPipelineCache

# 这是版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块的功能
# 定义了一个加载缓存的方法
"""
A module containing load_cache method definition.
"""

# 定义一个函数load_cache，它接受两个参数：config（可能是PipelineCacheConfig类型或者None）和root_dir（可能是字符串类型或者None）
def load_cache(config: PipelineCacheConfig | None, root_dir: str | None):
    """这个函数用来根据给定的配置加载缓存。"""
    
    # 如果config是None，那么返回一个不做任何操作的缓存对象
    if config is None:
        return NoopPipelineCache()

    # 使用Python 3.10的新特性匹配语句，检查config的type属性是什么类型
    match config.type:
        # 如果是CacheType.none，返回一个不做任何操作的缓存对象
        case CacheType.none:
            return NoopPipelineCache()
        # 如果是CacheType.memory，创建并返回一个内存缓存对象
        case CacheType.memory:
            return create_memory_cache()
        # 如果是CacheType.file，将config强制转换为PipelineFileCacheConfig类型
        # 然后创建一个FilePipelineStorage对象，用root_dir和config里的base_dir
        # 最后返回一个JsonPipelineCache对象，使用上面创建的存储对象
        case CacheType.file:
            config = cast(PipelineFileCacheConfig, config)
            storage = FilePipelineStorage(root_dir).child(config.base_dir)
            return JsonPipelineCache(storage)
        # 如果是CacheType.blob，将config强制转换为PipelineBlobCacheConfig类型
        # 创建并返回一个BlobPipelineStorage对象，需要连接字符串、容器名称
        # 可选的storage_account_blob_url参数
        # 最后返回一个JsonPipelineCache对象，使用创建的存储对象
        case CacheType.blob:
            config = cast(PipelineBlobCacheConfig, config)
            storage = BlobPipelineStorage(
                config.connection_string,
                config.container_name,
                storage_account_blob_url=config.storage_account_blob_url,
            ).child(config.base_dir)
            return JsonPipelineCache(storage)
        # 如果匹配不到以上任何一种情况，生成一个错误消息，抛出一个ValueError
        case _:
            msg = f"未知的缓存类型：{config.type}"
            raise ValueError(msg)

