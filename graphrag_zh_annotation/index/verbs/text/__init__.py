# 这段代码是从一个叫做"Indexing Engine text package"的软件包中导入一些功能。
# 它会让电脑能处理和改变文字。

# 第一行：从.chunk.text_chunk模块导入一个叫做'chunk'的工具，它可能能把一大段文字分成小块。
from .chunk.text_chunk import chunk

# 第二行：从.embed模块导入'text_embed'，这个工具可以给文字赋予数字（嵌入），让电脑更容易理解。
from .embed import text_embed

# 第三行：从.replace模块导入'replace'，这是一个用来替换文字中的某些内容的工具。
from .replace import replace

# 第四行：从.split模块导入'text_split'，可以将文字分割成几部分。
from .split import text_split

# 第五行：从.translate模块导入'text_translate'，这个工具能翻译文字。
from .translate import text_translate

# 下面这一段是版权声明，告诉我们这个代码由微软公司创建，而且遵循MIT许可证。
# Copyright (c) 2024 Microsoft Corporation.  # 2024年微软公司的版权
# Licensed under the MIT License  # 使用MIT许可证授权

# 这个文档字符串描述了这个软件包是什么。
"""The Indexing Engine text package root."""

# 最后这部分告诉程序，这些是这个包中可以公开使用的功能。
# 别人可以用这些名字来调用这些功能。
__all__ = [  # 公开的（导出的）所有功能列表
    "chunk",
    "replace",
    "text_embed",
    "text_split",
    "text_translate",
]

