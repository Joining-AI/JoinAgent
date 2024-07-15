# 导入Callable模块，这个模块里的Callable是一个特殊类型，代表可以被调用的对象，比如函数
from collections.abc import Callable

# 这是代码的版权信息，告诉我们这段代码属于微软公司，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对这个代码文件的简单描述，它说这是图知识模型GraphRAG中常用的数据类型
"""Common types for the GraphRAG knowledge model."""

# 从collections.abc模块再次导入Callable，确保我们有这个类型
from collections.abc import Callable

# 定义一个名为TextEmbedder的东西，它是一个Callable类型
# 这意味着TextEmbedder是一个接受字符串（str）作为输入，然后返回浮点数列表（list[float]）的函数
TextEmbedder = Callable[[str], list[float]]

