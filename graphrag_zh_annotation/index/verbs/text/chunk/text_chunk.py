# 导入一些有用的工具库
from enum import Enum  # 用于创建枚举类型
from typing import Any, cast  # 用于类型注解和类型转换
import pandas as pd  # 用于处理数据的库
from datashaper import (  # 用于数据操作的库
    ProgressTicker,  # 进度条工具
    TableContainer,  # 数据容器
    VerbCallbacks,  # 用于回调函数的类
    VerbInput,  # 用于verb输入的类
    progress_ticker,  # 进度条函数
    verb,  # 定义verb的装饰器
)
from .strategies.typing import ChunkStrategy as ChunkStrategy  # 引入自定义的分块策略
from .typing import ChunkInput  # 引入分块输入的类型定义

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了_get_num_total, chunk, run_strategy 和 load_strategy 函数的定义

# 导入需要的库
from enum import Enum
from typing import Any, cast

import pandas as pd
from datashaper import (
    ProgressTicker,
    TableContainer,
    VerbCallbacks,
    VerbInput,
    progress_ticker,
    verb,
)

from .strategies.typing import ChunkStrategy as ChunkStrategy
from .typing import ChunkInput


# 定义一个函数，计算数据框中某一列的元素总数
def _get_num_total(output: pd.DataFrame, column: str) -> int:
    # 初始化总数为0
    num_total = 0
    # 遍历数据框中指定列的所有行
    for row in output[column]:
        # 如果行是字符串类型，直接加1
        if isinstance(row, str):
            num_total += 1
        # 如果行不是字符串，可能是列表等可迭代对象，计算其长度并累加
        else:
            num_total += len(row)
    # 返回总数
    return num_total


# 定义一个枚举类ChunkStrategyType，表示两种分块策略
class ChunkStrategyType(str, Enum):
    # 策略：按单词分块
    tokens = "tokens"
    # 策略：按句子分块
    sentence = "sentence"

    # 自定义枚举类型的字符串表示方法
    def __repr__(self):
        # 返回带有引号的策略值
        return f'"{self.value}"'


# 使用verb装饰器定义一个名为"chunk"的操作
@verb(name="chunk")

# 定义一个名为chunk的函数，接收几个参数
def chunk(
    input: VerbInput,  # 输入的数据，类型是VerbInput
    column: str,  # 指定包含文本的列名
    to: str,  # 输出分块后文本的新列名
    callbacks: VerbCallbacks,  # 回调函数，用于处理进度更新
    strategy: dict[str, Any] | None = None,  # 分块策略配置，可选，默认为None
    **_kwargs,  # 其他任意关键字参数，这里不做使用
) -> TableContainer:  # 函数返回一个TableContainer对象

    """
    这个函数的作用是将一大段文本分成小块。

    使用方法：
    在yaml格式的配置中这样写：
    verb: text_chunk
    args:
        column: <列名>   # 包含文本的列名
        to: <列名>       # 存放分块后文本的新列名
        strategy: <策略配置>  # 分块策略，后面有更多细节
    """

    # 如果没有提供策略，就用一个空字典作为默认策略
    if strategy is None:
        strategy = {}

    # 获取输入数据，将其转换成DataFrame类型
    output = cast(pd.DataFrame, input.get_input())

    # 确定使用的策略类型，如果没有指定，则默认使用"tokens"策略
    strategy_name = strategy.get("type", ChunkStrategyType.tokens)

    # 复制策略配置，以便稍后修改
    strategy_config = {**strategy}

    # 加载选定的分块策略
    strategy_exec = load_strategy(strategy_name)

    # 计算需要处理的总行数
    num_total = _get_num_total(output, column)

    # 创建一个进度条更新器
    tick = progress_ticker(callbacks.progress, num_total)

    # 遍历DataFrame的每一行，使用策略执行函数处理文本并存入新列
    output[to] = output.apply(
        cast(
            Any,
            lambda x: run_strategy(strategy_exec, x[column], strategy_config, tick),  # 对每一行应用策略
        ),
        axis=1,  # 按行操作
    )

    # 返回处理后的数据
    return TableContainer(table=output)

# 定义一个名为run_strategy的函数，它接受四个参数：
# strategy：一个策略，用于处理文本块
# input：输入数据，可以是字符串或包含文本内容的列表或元组
# strategy_args：一个字典，存储策略需要的额外参数
# tick：一个进度指示器对象

def run_strategy(
    strategy: ChunkStrategy,
    input: ChunkInput,
    strategy_args: dict[str, Any],
    tick: ProgressTicker,
) -> list[str | tuple[list[str] | None, str, int]]:
    """运行策略方法的定义"""
    
    # 如果输入是一个字符串，用策略处理并返回结果
    if isinstance(input, str):
        return [item.text_chunk for item in strategy([input], {**strategy_args}, tick)]

    # 我们可以处理文本内容的列表，或者文档ID和文本内容的元组列表
    # 首先创建一个空列表来存储文本
    texts = []

    # 遍历输入数据，如果元素是字符串，添加到texts列表；如果元素是元组，只取第二个（文本内容）部分添加
    for item in input:
        if isinstance(item, str):
            texts.append(item)
        else:
            texts.append(item[1])

    # 使用策略处理texts列表，得到结果
    strategy_results = strategy(texts, {**strategy_args}, tick)

    # 创建一个空列表来存储最终结果
    results = []

    # 遍历策略处理的结果
    for strategy_result in strategy_results:
        # 获取结果对应的原始文档索引
        doc_indices = strategy_result.source_doc_indices

        # 如果输入的原始数据是字符串，只保留文本块
        if isinstance(input[doc_indices[0]], str):
            results.append(strategy_result.text_chunk)
        # 如果输入的原始数据是元组，将文档ID、文本块和词数一起保存为元组
        else:
            doc_ids = [input[doc_idx][0] for doc_idx in doc_indices]
            results.append((
                doc_ids,
                strategy_result.text_chunk,
                strategy_result.n_tokens,
            ))

    # 返回处理后的结果列表
    return results


# 定义一个名为load_strategy的函数，它接受一个参数：策略类型
def load_strategy(strategy: ChunkStrategyType) -> ChunkStrategy:
    """加载策略方法的定义"""

    # 根据策略类型，选择合适的处理方法
    # 如果策略类型是tokens，从特定模块导入并返回run_tokens方法
    match strategy:
        case ChunkStrategyType.tokens:
            from .strategies.tokens import run as run_tokens
            return run_tokens

        # 如果策略类型是sentence，先执行初始化，然后从特定模块导入并返回run_sentence方法
        case ChunkStrategyType.sentence:
            from graphrag.index.bootstrap import bootstrap
            bootstrap()
            from .strategies.sentence import run as run_sentence
            return run_sentence

        # 如果策略类型未知，抛出一个错误
        case _:
            msg = f"未知策略：{strategy}"
            raise ValueError(msg)

