# 导入名为text_replace的函数，这个函数可能用于替换文本中的某些内容
from .replace import text_replace

# 这一行是版权声明，告诉我们这段代码的版权属于2024年的微软公司
# Licensed under the MIT License 表示这个代码遵循MIT许可证，允许他人在一定条件下使用和修改

# 这个模块的文档字符串，描述了"Indexing Engine text replace package"的基础
"""这是一个用于文本替换的程序包的主文件。"""

# 再次导入replace模块的text_replace函数，这看起来是为了确保它被暴露给外部使用
from .replace import text_replace

# 这一行定义了一个列表，告诉其他程序这个模块里可以公开使用的部分只有"text_replace"函数
__all__ = ["text_replace"]

