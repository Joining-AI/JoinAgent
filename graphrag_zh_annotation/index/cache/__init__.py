# 导入一个叫做JsonPipelineCache的模块，它可能用来存储和处理JSON格式的数据
from .json_pipeline_cache import JsonPipelineCache

# 导入load_cache模块，这个可能用于加载保存的缓存数据
from .load_cache import load_cache

# 导入InMemoryCache模块，它可能是一个在内存中存储数据的缓存工具
from .memory_pipeline_cache import InMemoryCache

# 导入NoopPipelineCache模块，"Noop"通常代表无操作，所以这可能是一个不做任何缓存的工具
from .noop_pipeline_cache import NoopPipelineCache

# 导入PipelineCache模块，这是缓存系统的核心部分
from .pipeline_cache import PipelineCache

# 这是微软公司的版权声明，告诉我们代码的版权归属和使用的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个字符串表示当前包的根目录描述
"""The Indexing Engine cache package root."""

# 再次导入相同的四个缓存模块和load_cache，这是为了让外部知道这些是这个包公开提供的功能
from .json_pipeline_cache import JsonPipelineCache
from .load_cache import load_cache
from .memory_pipeline_cache import InMemoryCache
from .noop_pipeline_cache import NoopPipelineCache
from .pipeline_cache import PipelineCache

# 这是一个列表，列出了这个包对外提供的所有主要功能（公共接口）
__all__ = [
    "InMemoryCache",  # 内存中的缓存
    "JsonPipelineCache",  # JSON格式的缓存
    "NoopPipelineCache",  # 无操作的缓存
    "PipelineCache",  # 缓存管理器
    "load_cache",  # 加载缓存的函数
]

