# 导入asyncio模块，它用于编写异步代码
import asyncio

# 导入logging模块，用于记录程序运行日志
import logging

# 从typing模块导入Any类型，它代表任何数据类型
from typing import Any

# 导入numpy库，用于处理数学和科学计算中的数组
import numpy as np

# 从datashaper库导入ProgressTicker和VerbCallbacks，它们是进度条和回调函数的类
from datashaper import ProgressTicker, VerbCallbacks, progress_ticker

# 导入graphrag库的默认配置模块
from graphrag.config.defaults import defs

# 导入PipelineCache类，用于缓存处理管道
from graphrag.index.cache import PipelineCache

# 导入load_llm_embeddings函数，用于加载语言模型嵌入
from graphrag.index.llm import load_llm_embeddings

# 导入TokenTextSplitter类，用于将文本拆分成单词或标记
from graphrag.index.text_splitting import TokenTextSplitter

# 导入is_null函数，用于检查值是否为空
from graphrag.index.utils import is_null

# 导入EmbeddingLLM和OpenAIConfiguration类，与语言模型相关的类
from graphrag.llm import EmbeddingLLM, OpenAIConfiguration

# 从当前模块的typing子模块导入TextEmbeddingResult类型
from .typing import TextEmbeddingResult

# 这一行是版权声明，表示代码由微软公司拥有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含run方法的定义
"""A module containing run method definition."""

# 创建一个日志器对象，用于记录程序运行信息
log = logging.getLogger(__name__)

# 定义一个异步函数run，输入参数包括：文本列表、回调函数、缓存和一个字典
async def run(
    input: list[str],  # 输入的文本列表
    callbacks: VerbCallbacks,  # 用于处理事件的回调函数
    cache: PipelineCache,  # 缓存数据的地方
    args: dict[str, Any],  # 其他配置参数的字典
) -> TextEmbeddingResult:  # 返回的结果类型

    """
    这个函数用来运行一个提取信息的流程。
    """
    # 如果输入的文本列表为空，就返回一个没有嵌入向量的结果
    if is_null(input):
        return TextEmbeddingResult(embeddings=None)

    # 从参数字典中获取语言模型配置，如果没有就用默认值
    llm_config = args.get("llm", {})
    # 获取批次大小，默认16
    batch_size = args.get("batch_size", 16)
    # 获取每个批次的最大令牌数，默认8191
    batch_max_tokens = args.get("batch_max_tokens", 8191)
    # 根据语言模型配置创建OpenAIConfiguration对象
    oai_config = OpenAIConfiguration(llm_config)
    # 根据配置和最大令牌数获取分割器
    splitter = _get_splitter(oai_config, batch_max_tokens)
    # 根据配置、回调函数和缓存获取语言模型
    llm = _get_llm(oai_config, callbacks, cache)
    # 创建一个信号量，限制并发处理的线程数量，默认4
    semaphore: asyncio.Semaphore = asyncio.Semaphore(args.get("num_threads", 4))

    # 准备文本，根据分割器将输入文本拆分成片段，同时记录每个输入文本的片段数量
    texts, input_sizes = _prepare_embed_texts(input, splitter)
    # 创建批次，将文本片段分组
    text_batches = _create_text_batches(
        texts,
        batch_size,
        batch_max_tokens,
        splitter,
    )
    # 打印日志信息，展示要处理的输入、片段、批次数量以及批次和令牌的最大大小
    log.info(
        "embedding %d inputs via %d snippets using %d batches. max_batch_size=%d, max_tokens=%d",
        len(input),
        len(texts),
        len(text_batches),
        batch_size,
        batch_max_tokens,
    )
    # 创建进度条更新器
    ticker = progress_ticker(callbacks.progress, len(text_batches))

    # 异步执行，为每个文本片段批次计算嵌入向量
    embeddings = await _execute(llm, text_batches, ticker, semaphore)
    # 根据原始输入文本的大小重组嵌入向量
    embeddings = _reconstitute_embeddings(embeddings, input_sizes)

    # 返回包含所有嵌入向量的结果
    return TextEmbeddingResult(embeddings=embeddings)

# 内部辅助函数，根据配置和最大令牌数创建分割器
def _get_splitter(
    config: OpenAIConfiguration, batch_max_tokens: int
) -> TokenTextSplitter:
    # 返回一个分割器，用于将文本拆分成适合模型处理的片段
    return TokenTextSplitter(
        encoding_name=config.encoding_model or defs.ENCODING_MODEL,
        chunk_size=batch_max_tokens,
    )

# 内部辅助函数，根据配置、回调函数和缓存获取合适的语言模型
def _get_llm(
    config: OpenAIConfiguration,
    callbacks: VerbCallbacks,
    cache: PipelineCache,
) -> EmbeddingLLM:
    # 获取语言模型的类型
    llm_type = config.lookup("type", "Unknown")
    # 加载并返回对应类型的语言模型
    return load_llm_embeddings(
        "text_embedding",
        llm_type,
        callbacks,
        cache,
        config.raw_config,
    )

# 定义一个异步函数 _execute，用于执行嵌入操作
async def _execute(
    llm: EmbeddingLLM,  # 输入是一个EmbeddingLLM类型的对象，用于处理文本
    chunks: list[list[str]],  # 一个列表，里面包含多个字符串列表
    tick: ProgressTicker,  # 进度指示器，用来更新进度
    semaphore: asyncio.Semaphore,  # 信号量，用于控制并发数量
) -> list[list[float]]:  # 函数返回值是一个浮点数列表的列表

    # 定义一个内部异步函数 embed，用于处理单个字符串列表
    async def embed(chunk: list[str]):  
        # 使用信号量，确保同一时间只有一个任务在运行
        async with semaphore:
            # 使用llm对象处理chunk中的文本
            chunk_embeddings = await llm(chunk)
            # 提取输出结果并转换为numpy数组
            result = np.array(chunk_embeddings.output)
            # 更新进度指示器
            tick(1)
        # 返回处理后的结果
        return result

    # 对每个文本块调用embed函数，生成一个异步任务列表
    futures = [embed(chunk) for chunk in chunks]
    # 等待所有异步任务完成，并收集结果
    results = await asyncio.gather(*futures)
    # 将嵌入结果展平成一个单一的列表
    return [item for sublist in results for item in sublist]

# 定义一个函数 _create_text_batches，用于创建文本批次
def _create_text_batches(
    texts: list[str],  # 输入是一个字符串列表
    max_batch_size: int,  # 每个批次的最大文本数量
    max_batch_tokens: int,  # 每个批次的最大字符数
    splitter: TokenTextSplitter,  # 用于分割文本的工具
) -> list[list[str]]:  # 函数返回值是一个字符串列表的列表

    # 初始化结果列表、当前批次列表和当前批次字符数
    result = []
    current_batch = []
    current_batch_tokens = 0

    # 遍历所有文本
    for text in texts:
        # 计算文本的字符数
        token_count = splitter.num_tokens(text)
        # 如果当前批次达到最大大小或字符数超出限制
        if (
            len(current_batch) >= max_batch_size
            or current_batch_tokens + token_count > max_batch_tokens
        ):
            # 添加当前批次到结果列表，清空当前批次和字符数
            result.append(current_batch)
            current_batch = []
            current_batch_tokens = 0

        # 将文本添加到当前批次，并累加字符数
        current_batch.append(text)
        current_batch_tokens += token_count

    # 处理最后可能剩下的文本批次
    if len(current_batch) > 0:
        result.append(current_batch)

    # 返回创建的文本批次列表
    return result

# 定义一个函数，它的任务是准备文本嵌入（一种将文本转换成数字表示的方法）
def _prepare_embed_texts(
    输入: list[str],  # 这是一个包含多个字符串的列表，每个字符串都是一个输入文本
    分割器: TokenTextSplitter  # 这是一个工具，用来分割文本成更小的部分
) -> tuple[list[str], list[int]]:  # 函数会返回两个列表，一个是分割后的文本片段，另一个是每个输入文本的片段数量

    大小: list[int] = []  # 创建一个空列表，用于存储每个输入文本的片段数量
    片段: list[str] = []  # 创建一个空列表，用于存储分割后的文本片段

    # 遍历输入的每一个文本
    for 文本 in 输入:
        # 使用分割器将文本分割
        分割的文本 = 分割器.split_text(文本)
        # 如果分割结果为空，跳过这个文本
        if 分割的文本 is None:
            continue
        # 过滤掉长度为0的片段
        分割的文本 = [text for text in 分割的文本 if len(text) > 0]

        # 记录这个文本有多少个片段
        大小.append(len(分割的文本))
        # 将这些片段添加到片段列表中
        片段.extend(分割的文本)

    # 返回分割后的文本片段和它们的大小列表
    return 片段, 大小


# 另一个函数，用于将原始嵌入（数字表示）重组回输入文本的形式
def _reconstitute_embeddings(
    原始嵌入: list[list[float]],  # 这是一个嵌入值的列表，每个嵌入值也是一个浮点数列表
    大小: list[int],  # 上一个函数返回的每个输入文本的片段数量
) -> list[list[float] | None]:  # 返回一个列表，每个元素可能是浮点数列表（嵌入值）或None（表示没有嵌入）
    嵌入: list[list[float] | None] = []  # 创建一个空列表，用于存储重组后的嵌入值

    # 初始化一个指针，用于遍历原始嵌入列表
    指针 = 0

    # 遍历每个输入文本的片段数量
    for 数量 in 大小:
        # 如果片段数量为0，添加None到嵌入列表
        if 数量 == 0:
            嵌入.append(None)
        # 如果片段数量为1，直接添加原始嵌入中的值
        elif 数量 == 1:
            单个嵌入 = 原始嵌入[指针]
            嵌入.append(单个嵌入)
            指针 += 1
        # 如果片段数量大于1，计算平均嵌入并归一化
        else:
            # 获取当前片段的嵌入值子列表
            块 = 原始嵌入[指针 : 指针 + 数量]
            # 计算平均值
            平均值 = np.average(块, axis=0)
            # 归一化平均值
            归一化 = 平均值 / np.linalg.norm(平均值)
            # 将归一化的平均值转换为列表并添加到嵌入列表中
            嵌入.append(归一化.tolist())
            # 更新指针
            指针 += 数量

    # 返回重组后的嵌入列表
    return 嵌入

