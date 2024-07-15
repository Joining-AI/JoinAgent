# 导入.text_chunk模块中的三个东西：ChunkStrategy类、ChunkStrategyType枚举和chunk函数
from .text_chunk import ChunkStrategy, ChunkStrategyType, chunk

# 这是微软公司的版权声明，告诉我们代码的版权归属和使用许可
# Copyright (c) 2024 Microsoft Corporation. # 2024年微软公司的代码
# Licensed under the MIT License # 使用的是MIT许可证，允许他人在遵守一定规则下使用这个代码

# 这个模块对外公开的内容，告诉其他程序可以使用 ChunkStrategy, ChunkStrategyType, chunk 这三个
"""The Indexing Engine text chunk package root.""" # 这是一个关于这个代码包的文字描述，它是一个索引引擎的文本块包的根目录

# 再次导入.text_chunk模块中的三个元素，确保它们被导出并可供其他文件使用
from .text_chunk import ChunkStrategy, ChunkStrategyType, chunk

# 这一行告诉Python，这个模块中我们希望其他程序能直接使用的变量或函数有哪些
__all__ = ["ChunkStrategy", "ChunkStrategyType", "chunk"]

