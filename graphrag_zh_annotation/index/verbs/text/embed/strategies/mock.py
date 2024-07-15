# 导入随机数模块，用于生成随机数
import random

# 导入Iterable，它是Python中可迭代对象的基类
from collections.abc import Iterable

# 导入Any，这是Python类型注解中的一个类型，代表任何类型的数据
from typing import Any

# 导入datashaper库中的进度条工具
from datashaper import ProgressTicker, VerbCallbacks, progress_ticker

# 导入graphrag.index.cache模块中的PipelineCache，可能用于存储和检索数据
from graphrag.index.cache import PipelineCache

# 导入自定义的TextEmbeddingResult类型
from .typing import TextEmbeddingResult

# 这是微软公司的版权信息和许可声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了run和.Embed_text两个函数的定义

# 定义一个异步函数run，它需要一个字符串列表、回调函数、缓存对象和一个字典作为参数
async def run(  # noqa RUF029：忽略某些代码检查规则，因为异步函数是必要的
    input: list[str],  # 输入的文本列表
    callbacks: VerbCallbacks,  # 回调函数，用来更新进度
    cache: PipelineCache,  # 缓存对象
    _args: dict[str, Any],  # 其他参数，用字典形式传递
) -> TextEmbeddingResult:  # 返回TextEmbeddingResult类型的对象

    # 检查输入是否为可迭代对象，如果不是，将其转换为单元素的列表
    input = input if isinstance(input, Iterable) else [input]

    # 创建一个进度条，根据输入文本数量设置总步数
    ticker = progress_ticker(callbacks.progress, len(input))

    # 使用列表推导式，对每个文本调用._embed_text函数，将结果保存在结果列表中
    # 最后返回一个TextEmbeddingResult对象，包含所有文本的嵌入向量
    return TextEmbeddingResult(embeddings=[_embed_text(cache, text, ticker) for text in input])

# 定义一个内部函数._embed_text，接受缓存对象、文本字符串和进度条对象作为参数
def _embed_text(_cache: PipelineCache, _text: str, tick: ProgressTicker) -> list[float]:

    # 更新进度条，表示开始处理文本
    tick(1)

    # 生成一个随机的三维向量（为了简单起见，这里只模拟了随机过程，实际中会有所不同）
    # 忽略S311规则，可能是因为在生产环境中不应使用随机数
    return [random.random(), random.random(), random.random()]

