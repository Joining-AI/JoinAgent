# 导入必要的工具包，这些工具包帮助我们定义和处理数据
from collections.abc import Awaitable, Callable  # 从abc模块导入可以等待的结果类和可调用对象的接口
from dataclasses import dataclass  # 从dataclasses模块导入数据类，用来创建简单的类
from typing import Any  # 从typing模块导入Any类型，表示可以是任何类型的数据

# 导入额外的库，用于数据操作和缓存
from datashaper import VerbCallbacks  # 从datashaper库导入VerbCallbacks，可能用于数据操作的回调函数
from graphrag.index.cache import PipelineCache  # 从graphrag库的index.cache模块导入PipelineCache，可能是一个数据处理管道的缓存

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.  # 这是代码的所有权信息
# Licensed under the MIT License  # 代码使用MIT许可证授权

# 这个模块包含了'TextTranslationResult'模型的定义

# 使用dataclass创建一个类，表示文本翻译的结果
@dataclass
class TextTranslationResult:
    """这是一个用于存储文本翻译结果的类。"""
    # 翻译后的文本列表
    translations: list[str]  # 类的属性，是一个字符串列表

# 定义一个类型，表示一个函数，这个函数接受特定参数并返回一个等待的结果（翻译结果）
TextTranslationStrategy = Callable[
    [list[str], dict[str, Any], VerbCallbacks, PipelineCache],  # 函数的输入参数
    Awaitable[TextTranslationResult],  # 函数返回一个可以等待的TextTranslationResult对象
]

