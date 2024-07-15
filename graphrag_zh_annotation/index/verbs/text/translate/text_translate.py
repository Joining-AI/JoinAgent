# 导入Enum模块，用于创建枚举类型
from enum import Enum
# 导入typing模块中的Any和cast，帮助我们定义和转换类型
from typing import Any, cast
# 导入pandas库，用于数据处理
import pandas as pd
# 导入datashaper库中的一些类和函数，用于数据操作
from datashaper import AsyncType, TableContainer, VerbCallbacks, VerbInput, derive_from_rows, verb
# 导入graphrag.index.cache中的PipelineCache类，可能用于缓存数据管道
from graphrag.index.cache import PipelineCache
# 导入当前目录下strategies.typing模块中的TextTranslationStrategy类
from .strategies.typing import TextTranslationStrategy

# 这一行是版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含文本翻译方法的定义
"""

# 创建一个继承自str和Enum的类，用于表示文本翻译策略的类型
class TextTranslateStrategyType(str, Enum):
    # 枚举值，表示使用OpenAI服务进行翻译
    openai = "openai"
    # 枚举值，表示使用模拟（或假）数据进行翻译
    mock = "mock"

    # 当打印或显示枚举对象时，返回其值的字符串形式
    def __repr__(self):
        return f'"{self.value}"'

# 使用@verb装饰器定义一个名为"text_translate"的操作
@verb(name="text_translate")

# 定义一个异步函数text_translate，它会翻译文本到另一种语言
async def text_translate(
    输入: VerbInput,  # 接收的数据结构
    缓存: PipelineCache,  # 存储中间结果的地方
    回调函数: VerbCallbacks,  # 执行某些操作时调用的函数
    文本列: str,  # 包含要翻译的文本的列名
    到: str,  # 要写入翻译后文本的列名
    策略: dict[str, Any],  # 翻译策略配置
    异步模式: AsyncType = AsyncType.AsyncIO,  # 默认使用异步IO
    **kwargs,  # 其他可能的参数
) -> TableContainer:  # 返回的结果是表格容器

    """
    这个函数用来把文本翻译成其他语言。

    使用方法：
    在YAML中这样写：
    verb: text_translate
    args:
        text_column: <列名>  # 要翻译的文本所在的列名
        to: <列名>  # 写入翻译结果的列名
        strategy: <策略配置>  # 翻译策略，下面有更多细节
    """

    # 获取输入数据框
    输出数据框 = 输入获取输入()

    # 从策略字典中获取策略类型
    策略类型 = 策略["type"]

    # 复制策略字典，删除"type"键
    策略参数 = {**策略}

    # 加载对应的翻译策略
    策略执行器 = _load_strategy(策略类型)

    # 定义一个异步函数，用于对每一行执行翻译策略
    async def 运行策略(当前行):
        # 获取当前行的文本
        文本 = 当前行[文本列]
        # 使用策略执行器翻译文本
        结果 = await 策略执行器(文本, 策略参数, 回调函数, 缓存)
        
        # 如果文本是单个字符串，返回第一个翻译结果
        if isinstance(文本, str):
            return 结果翻译[0]

        # 否则，返回每个输入项的翻译结果列表
        return [翻译 for 翻译 in 结果翻译]

    # 使用derive_from_rows函数，按行运行翻译策略
    结果列表 = await derive_from_rows(
        输出数据框,
        运行策略,
        回调函数,
        异步模式=异步模式,
        并行线程数=kwargs.get("num_threads", 4),  # 默认使用4个线程
    )

    # 把翻译结果放入新列
    输出数据框[到] = 结果列表

    # 返回包含翻译结果的表格容器
    return TableContainer(table=输出数据框)

# 定义一个函数，叫做_load_strategy，它接受一个参数：strategy，类型是TextTranslateStrategyType
def _load_strategy(strategy: TextTranslateStrategyType) -> TextTranslationStrategy:
    # 使用Python的匹配语句，检查strategy的值
    match strategy:
        # 如果strategy的值等于TextTranslateStrategyType.openai
        case TextTranslateStrategyType.openai:
            # 从.strategies.openai模块导入一个名为run的函数，改名为run_openai
            from .strategies.openai import run as run_openai
            # 返回run_openai这个函数
            return run_openai

        # 如果strategy的值等于TextTranslateStrategyType.mock
        case TextTranslateStrategyType.mock:
            # 从.strategies.mock模块导入一个名为run的函数，改名为run_mock
            from .strategies.mock import run as run_mock
            # 返回run_mock这个函数
            return run_mock

        # 如果以上两种情况都不满足，即strategy的值是未知的
        case _:
            # 创建一个消息字符串，内容是"Unknown strategy: "后面跟着strategy的值
            msg = f"Unknown strategy: {strategy}"
            # 抛出一个ValueError，附带上面创建的消息
            raise ValueError(msg)

