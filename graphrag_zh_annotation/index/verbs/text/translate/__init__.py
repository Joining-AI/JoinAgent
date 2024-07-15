# 导入一个叫做 'text_translate' 的函数，它来自当前模块的子模块 '.text_translate'
from .text_translate import text_translate

# 这是一个版权声明，意味着这段代码是微软公司在2024年或之前写的
# 它受到 MIT 许可证的保护，这意味着你可以自由使用，但需要遵守一些规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个代码包是关于“索引引擎文本翻译”的
# """The Indexing Engine text translate package root."""

# 再次导入 'text_translate' 函数，这样在当前模块中可以直接使用它
from .text_translate import text_translate

# '__all__' 是一个特殊变量，告诉别人这个模块导出的公共部分只有 'text_translate' 函数
# 这样，当其他人使用 'from package_name import *' 时，只会导入 'text_translate'
__all__ = ["text_translate"]

