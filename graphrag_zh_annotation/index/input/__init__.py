# 导入一个叫做 load_input 的函数，它来自同一目录下的 load_input 模块。
from .load_input import load_input

# 这是一个版权声明，表示这段代码由微软公司创作，时间是2024年。
# 它遵循的是 MIT 许可证的规定。
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对这个代码包的描述，它说这是“索引引擎输入包”的根目录。
"""The Indexing Engine input package root."""

# 再次导入 load_input，这次是把它包含在这个模块对外提供的所有功能列表中。
# 这样其他地方就可以通过 "from indexing_engine_input import load_input" 来使用这个函数了。
from .load_input import load_input

# '__all__' 是一个特殊变量，它告诉 Python 当别人使用 "from indexing_engine_input import *" 时，
# 应该导出哪些名字。这里只导出 "load_input"。
__all__ = ["load_input"]

