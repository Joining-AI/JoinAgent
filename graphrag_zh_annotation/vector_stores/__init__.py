# 导入一个叫做 AzureAISearch 的东西，它来自 .azure_ai_search 这个地方
from .azure_ai_search import AzureAISearch

# 导入一些基础的东西，比如 BaseVectorStore, VectorStoreDocument 和 VectorStoreSearchResult
# 这些都来自 .base 这个模块
from .base import BaseVectorStore, VectorStoreDocument, VectorStoreSearchResult

# 导入 LanceDBVectorStore，它来自 .lancedb
from .lancedb import LanceDBVectorStore

# 从 .typing 导入两个类型定义：VectorStoreFactory 和 VectorStoreType
from .typing import VectorStoreFactory, VectorStoreType

# 这是一个注释，告诉人们这个代码是微软公司在2024年写的
# 并且它遵循的是 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了一些用于存储和操作向量的实现
"""A package containing vector-storage implementations."""

# 把之前导入的所有东西列出来，这样其他地方就可以直接使用它们了
__all__ = [
    # 列出所有可以公开使用的类和名称
    "AzureAISearch",
    "BaseVectorStore",
    "LanceDBVectorStore",
    "VectorStoreDocument",
    "VectorStoreFactory",
    "VectorStoreSearchResult",
    "VectorStoreType",
]

