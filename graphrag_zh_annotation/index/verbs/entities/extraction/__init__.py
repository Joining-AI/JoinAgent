# 导入一个名为"entity_extract"的模块，里面有两个东西：ExtractEntityStrategyType和entity_extract
from .entity_extract import ExtractEntityStrategyType, entity_extract

# 这是版权信息，意思是2024年微软公司拥有这个代码，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个Python文件是关于索引引擎中实体提取包的根目录
"""The Indexing Engine entities extraction package root."""

# 再次导入"entity_extract"模块中的"ExtractEntityStrategyType"和"entity_extract"
from .entity_extract import ExtractEntityStrategyType, entity_extract

# 这里的 "__all__" 是一个特殊列表，告诉别人这个模块导出哪些内容，这里有两个：ExtractEntityStrategyType 和 entity_extract
__all__ = ["ExtractEntityStrategyType", "entity_extract"]

