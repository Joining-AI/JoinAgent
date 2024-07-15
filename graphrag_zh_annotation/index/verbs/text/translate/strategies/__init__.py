# 导入名为'run'的函数，它来自当前模块的'mock'子模块。
from .mock import run as run_mock

# 同样导入名为'run'的函数，这次它来自当前模块的'openai'子模块。
from .openai import run as run_openai

# 这是一个版权声明，说明代码的版权归2024年的微软公司所有。
# 并且代码遵循MIT许可证的规定。

# 这个模块的文档字符串，描述了这是一个关于索引引擎翻译策略包的根目录。
"""The Indexing Engine translate strategies package root."""

# 这一行告诉Python，当我们从这个包中导入时，公开'run_mock'和'run_openai'两个函数供外部使用。
__all__ = ["run_mock", "run_openai"]

