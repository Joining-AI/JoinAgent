# 导入logging模块，用于记录程序运行日志
import logging

# 导入traceback模块，帮助我们追踪程序中的错误
import traceback

# 从typing模块导入Any类型，用于表示任何类型的变量
from typing import Any

# 导入VerbCallbacks类，它可能是一个处理数据的工具
from datashaper import VerbCallbacks

# 导入graphrag配置的默认值
from graphrag.config.defaults import defs

# 从graphrag的枚举模块导入LLMType，它定义了语言模型的类型
from graphrag.config.enums import LLMType

# 导入PipelineCache类，它可能用于存储和检索处理管道
from graphrag.index.cache import PipelineCache

# 导入load_llm函数，用于加载语言模型
from graphrag.index.llm import load_llm

# 导入TokenTextSplitter类，用于将文本拆分成单词或标记
from graphrag.index.text_splitting import TokenTextSplitter

# 导入CompletionLLM类，它可能是完成或生成文本的语言模型
from graphrag.llm import CompletionLLM

# 从当前模块的默认值中导入TRANSLATION_PROMPT，作为翻译提示的默认值
from .defaults import TRANSLATION_PROMPT as DEFAULT_TRANSLATION_PROMPT

# 从当前模块的typing中导入TextTranslationResult，这是翻译结果的数据结构
from .typing import TextTranslationResult

# 这一行是版权声明，表示代码由微软公司拥有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块包含的方法
"""一个模块，里面定义了run、_translate_text和_create_translation_prompt方法。"""

# 创建一个日志器，用于记录与这个模块相关的日志信息
log = logging.getLogger(__name__)

# 定义一个异步函数run，输入包括字符串或字符串列表、字典、回调函数和管道缓存
async def run(
    input: str | list[str],  # 输入可以是单个字符串或字符串列表
    args: dict[str, Any],  # 参数字典，包含各种设置
    callbacks: VerbCallbacks,  # 回调函数，用于处理事件
    pipeline_cache: PipelineCache,  # 管道缓存，存储中间结果
) -> TextTranslationResult:  # 返回值是一个翻译结果对象

    # 从参数中获取语言模型配置，如果没有就设为默认
    llm_config = args.get("llm", {"type": LLMType.StaticResponse})

    # 从配置中获取语言模型类型，如果没有就设为默认
    llm_type = llm_config.get("type", LLMType.StaticResponse)

    # 根据类型加载语言模型，只用于聊天
    llm = load_llm(
        "text_translation",  # 模块名
        llm_type,  # 语言模型类型
        callbacks,  # 回调函数
        pipeline_cache,  # 管道缓存
        llm_config,  # 语言模型配置
        chat_only=True,
    )

    # 获取目标语言，默认为英语
    language = args.get("language", "English")

    # 获取提示文本，可能为空
    prompt = args.get("prompt")

    # 获取分块大小，默认值
    chunk_size = args.get("chunk_size", defs.CHUNK_SIZE)

    # 获取分块重叠量，默认值
    chunk_overlap = args.get("chunk_overlap", defs.CHUNK_OVERLAP)

    # 如果输入是字符串，将其转换为单元素列表
    input = [input] if isinstance(input, str) else input

    # 对输入中的每个文本进行翻译，返回翻译结果列表
    return TextTranslationResult(
        translations=[
            await _translate_text(  # 异步调用单个文本翻译函数
                text,  # 当前文本
                language,  # 目标语言
                prompt,  # 提示文本
                llm,  # 语言模型
                chunk_size,  # 分块大小
                chunk_overlap,  # 分块重叠量
                callbacks,  # 回调函数
            )
            for text in input
        ]
    )

# 定义一个异步辅助函数_translate_text，用于翻译单个文本
async def _translate_text(
    text: str,  # 要翻译的文本
    language: str,  # 目标语言
    prompt: str | None,  # 提示文本，可能为空
    llm: CompletionLLM,  # 语言模型
    chunk_size: int,  # 分块大小
    chunk_overlap: int,  # 分块重叠量
    callbacks: VerbCallbacks,  # 回调函数
) -> str:  # 返回翻译后的文本

    # 使用分块器将文本切分为小块
    splitter = TokenTextSplitter(chunk_size, chunk_overlap)

    # 初始化输出字符串
    out = ""

    # 分割得到的文本块
    chunks = splitter.split_text(text)

    # 遍历每个文本块进行翻译
    for chunk in chunks:
        try:
            # 使用语言模型翻译当前块
            result = await llm(
                chunk,  # 当前块
                history=[  # 历史记录，包含提示
                    {
                        "role": "system",
                        "content": (prompt or DEFAULT_TRANSLATION_PROMPT),
                    }
                ],
                variables={"language": language},  # 变量，包含目标语言
            )

            # 将翻译结果添加到输出字符串
            out += result.output or ""  # 如果无输出则为空字符串
        except Exception as e:  # 处理翻译过程中可能出现的错误
            # 记录错误日志
            log.exception("error translating text")

            # 调用回调函数报告错误
            callbacks.error("Error translating text", e, traceback.format_exc())

            # 添加空字符串到输出，以确保输出始终为字符串
            out += ""

    # 返回翻译后的完整文本
    return out

