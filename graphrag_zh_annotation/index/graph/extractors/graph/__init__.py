# 导入模块，这部分是让Python从当前文件夹下的graph_extractor模块中获取一些东西
from .graph_extractor import (
    # 默认的实体类型列表，这是程序识别信息的类别
    DEFAULT_ENTITY_TYPES,
    # 结果类，用于存储图提取过程的结果
    GraphExtractionResult,
    # 提取器类，帮助我们从文本中提取图形信息
    GraphExtractor,
)

# 导入prompts模块中的GRAPH_EXTRACTION_PROMPT，这可能是一个提示用户输入的文本
from .prompts import GRAPH_EXTRACTION_PROMPT

# 这是一个版权声明，说明代码由微软公司2024年创建，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个包是关于什么的，它是“单部分图”索引引擎的一部分
"""The Indexing Engine unipartite graph package root."""

# 把之前导入的四个名称（列表、提示、结果类和提取器类）都公开，这样其他文件可以使用它们
__all__ = [
    "DEFAULT_ENTITY_TYPES",
    "GRAPH_EXTRACTION_PROMPT",
    "GraphExtractionResult",
    "GraphExtractor",
]

