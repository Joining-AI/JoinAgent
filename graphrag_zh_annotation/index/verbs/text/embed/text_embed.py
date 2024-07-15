# 导入logging模块，用于程序中的日志记录
import logging

# 导入Enum类，用于创建枚举类型
from enum import Enum

# 导入typing模块的Any和cast，用于类型注解和类型转换
from typing import Any, cast

# 导入numpy库，用于处理数值计算和数组操作
import numpy as np

# 导入pandas库，用于数据处理和分析
import pandas as pd

# 导入datashaper库中的TableContainer、VerbCallbacks、VerbInput和verb装饰器
from datashaper import TableContainer, VerbCallbacks, VerbInput, verb

# 从graphrag.index.cache导入PipelineCache类
from graphrag.index.cache import PipelineCache

# 从graphrag.vector_stores导入一些类，用于向量存储和管理
from graphrag.vector_stores import BaseVectorStore, VectorStoreDocument, VectorStoreFactory

# 从当前模块的子模块strategies.typing导入TextEmbeddingStrategy类
from .strategies.typing import TextEmbeddingStrategy

# 版权声明，属于微软公司，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含text_embed、load_strategy和create_row_from_embedding_data方法的定义
# 注意：这里的注释是为了简化理解，实际代码中这部分是空行

# 设置日志记录器，获取当前模块名的日志器实例
log = logging.getLogger(__name__)

# 根据Azure OpenAI服务的限制，设置默认的嵌入向量批量大小
DEFAULT_EMBEDDING_BATCH_SIZE = 500

# 创建一个枚举类TextEmbedStrategyType，表示文本嵌入策略类型
class TextEmbedStrategyType(str, Enum):
    # 枚举值openai表示使用OpenAI服务
    openai = "openai"
    # 枚举值mock表示使用模拟（测试）策略
    mock = "mock"

    # 定义__repr__方法，返回字符串形式的枚举值
    def __repr__(self):
        # 返回引号包围的枚举值字符串
        return f'"{self.value}"'

# 使用verb装饰器定义一个名为"text_embed"的函数，它可能与数据处理有关
@verb(name="text_embed")

# 这个函数叫做 text_embed，它会把一段文字转换成一个向量。新生成的向量会被放在一个表格的新列里。
async def text_embed(
    输入: VerbInput,  # 接收的输入数据类型是 VerbInput
    回调函数: VerbCallbacks,  # 用于处理完成任务后的回调函数
    缓存: PipelineCache,  # 用于存储中间结果的缓存对象
    列名: str,  # 文本所在的列的名字
    策略: dict,  # 定义如何转换文本的配置
    **其他参数,  # 其他可能需要的额外参数
) -> TableContainer:  # 返回一个包含表格的新容器

    """
    文本嵌入功能，将文本转换为向量。输出新列包含文档ID和向量的对应关系。

    **使用方法**

# 这个函数是用来处理文本数据的，它会在内存中完成任务
async def _text_embed_in_memory(
    # input: 从外部传入的数据，包含一些动词信息
    input: VerbInput,
    # callbacks: 用于回调的函数集合
    callbacks: VerbCallbacks,
    # cache: 用来存储中间结果的缓存
    cache: PipelineCache,
    # column: 我们要处理的文本所在的列名
    column: str,
    # strategy: 描述如何处理文本的策略字典
    strategy: dict,
    # to: 处理后结果要放入的列名
    to: str,
):

    # 将输入数据转换成 pandas 数据框（一种表格形式的数据结构）
    output_df = cast(pd.DataFrame, input.get_input())

    # 获取策略的类型（比如是哪种文本处理方法）
    strategy_type = strategy["type"]

    # 加载对应策略类型的执行函数
    strategy_exec = load_strategy(strategy_type)

    # 保留策略字典中的其他参数
    strategy_args = {**strategy}

    # 再次获取原始输入数据（可能为了确保是最新的）
    input_table = input.get_input()

    # 提取指定列的所有文本，转化为列表
    texts: list[str] = input_table[column].to_numpy().tolist()

    # 使用加载的策略函数处理文本，同时传入回调和缓存
    result = await strategy_exec(texts, callbacks, cache, strategy_args)

    # 将处理后的嵌入结果放入新列
    output_df[to] = result.embeddings

    # 返回一个包含处理后数据的表格容器
    return TableContainer(table=output_df)

# 定义一个异步函数_text_embed_with_vector_store，接收多个参数
async def _text_embed_with_vector_store(
    input: VerbInput,          # 输入数据
    callbacks: VerbCallbacks,  # 回调函数
    cache: PipelineCache,      # 缓存对象
    column: str,               # 指定的列名
    strategy: dict,            # 策略字典
    vector_store: BaseVectorStore,  # 向量存储对象
    vector_store_config: dict,  # 向量存储配置
    store_in_table: bool = False,  # 是否将结果存储到表格中，默认为False
    to: str = "",              # 存储结果的列名，默认为空字符串
):

    # 将输入数据转换为Pandas DataFrame
    output_df = cast(pd.DataFrame, input.get_input())

    # 获取策略类型并加载对应的执行方法
    strategy_type = strategy["type"]
    strategy_exec = load_strategy(strategy_type)

    # 复制策略参数字典，以便稍后使用
    strategy_args = {**strategy}

    # 获取向量存储的配置信息
    insert_batch_size = vector_store_config.get("batch_size", DEFAULT_EMBEDDING_BATCH_SIZE)  # 批次大小
    title_column = vector_store_config.get("title_column", "title")  # 标题列名
    id_column = vector_store_config.get("id_column", "id")  # ID列名
    overwrite = vector_store_config.get("overwrite", True)  # 是否覆盖已有的向量

    # 检查输入DataFrame中是否存在指定的列
    if column not in output_df.columns:
        提示错误：列"{column}"在输入数据中未找到
    if title_column not in output_df.columns:
        提示错误：列"{title_column}"在输入数据中未找到
    if id_column not in output_df.columns:
        提示错误：列"{id_column}"在输入数据中未找到

    # 计算需要处理的总行数
    total_rows = 0
    for row in output_df[column]:
        if isinstance(row, list):
            total_rows += len(row)
        else:
            total_rows += 1

    # 初始化计数器和起始索引
    i = 0
    starting_index = 0

    # 创建一个空列表，用于存储结果
    all_results = []

    # 使用批次处理数据，直到处理完所有行
    while insert_batch_size * i < input.get_input().shape[0]:
        # 获取当前批次的数据
        batch = input.get_input().iloc[
            insert_batch_size * i : insert_batch_size * (i + 1)
        ]

        # 提取当前批次的文本、标题和ID
        texts = batch[column].to_numpy().tolist()
        titles = batch[title_column].to_numpy().tolist()
        ids = batch[id_column].to_numpy().tolist()

        # 使用策略执行方法处理文本
        result = await strategy_exec(
            texts,
            callbacks,
            cache,
            strategy_args,
        )

        # 如果需要存储结果到表格，并且有嵌入向量
        if store_in_table and result.embeddings:
            # 过滤掉None的嵌入向量
            embeddings = [embedding for embedding in result.embeddings if embedding is not None]
            # 将过滤后的嵌入向量添加到结果列表
            all_results.extend(embeddings)

        # 获取嵌入向量列表或空列表
        vectors = result.embeddings or []

        # 创建一个文档列表，每个文档包含ID、文本、标题和向量
        documents = []
        for id, text, title, vector in zip(ids, texts, titles, vectors, strict=True):
            # 将numpy数组转换为列表
            if type(vector) == np.ndarray:
                vector = vector.tolist()
            # 创建VectorStoreDocument对象
            document = VectorStoreDocument(
                id=id,
                text=text,
                vector=vector,
                attributes={"title": title},
            )
            # 将文档添加到列表
            documents.append(document)

        # 将文档加载到向量存储，根据是否覆盖决定是否替换现有向量
        vector_store.load_documents(documents, overwrite and i == 0)

        # 更新起始索引和计数器
        starting_index += len(documents)
        i += 1

    # 如果需要存储结果到表格，将结果列表添加到指定列
    if store_in_table:
        output_df[to] = all_results

    # 返回处理后的DataFrame
    return TableContainer(table=output_df)

# 定义一个函数，创建向量存储
def _create_vector_store(
    vector_store_config: dict,  # 传入一个关于向量存储的配置字典
    collection_name: str  # 传入一个集合名称（可能用于存储）
) -> BaseVectorStore:  # 返回一个基础的向量存储对象
    # 从配置字典中获取存储类型，转化为字符串
    vector_store_type: str = str(vector_store_config.get("type"))
    
    # 如果有集合名称，就更新配置字典
    if collection_name:
        vector_store_config.update({"collection_name": collection_name})

    # 根据存储类型和配置字典，创建向量存储对象
    vector_store = VectorStoreFactory.get_vector_store(
        vector_store_type, kwargs=vector_store_config
    )

    # 使用配置字典连接向量存储
    vector_store.connect(**vector_store_config)
    
    # 返回创建好的向量存储对象
    return vector_store


# 定义一个函数，获取集合名称
def _get_collection_name(vector_store_config: dict, embedding_name: str) -> str:
    # 从配置字典中尝试获取集合名称
    collection_name = vector_store_config.get("collection_name")
    
    # 如果没有集合名称，再从"collection_names"中查找对应嵌入名称的集合
    if not collection_name:
        collection_names = vector_store_config.get("collection_names", {})  # 获取或设置默认为空字典的"collection_names"
        collection_name = collection_names.get(embedding_name, embedding_name)  # 获取嵌入名称对应的集合，如果没有则用嵌入名称本身

    # 打印信息日志，说明正在使用的集合名称和嵌入名称
    msg = f"using {vector_store_config.get('type')} collection_name {collection_name} for embedding {embedding_name}"
    log.info(msg)
    
    # 返回最终的集合名称
    return collection_name


# 定义一个函数，根据策略类型加载相应的文本嵌入策略
def load_strategy(strategy: TextEmbedStrategyType) -> TextEmbeddingStrategy:
    """加载策略方法的定义。"""
    # 使用匹配表达式判断策略类型
    match strategy:
        # 如果策略是OpenAI类型
        case TextEmbedStrategyType.openai:
            # 从特定模块导入并运行OpenAI策略
            from .strategies.openai import run as run_openai
            return run_openai
        # 如果策略是Mock类型
        case TextEmbedStrategyType.mock:
            # 从特定模块导入并运行Mock策略
            from .strategies.mock import run as run_mock
            return run_mock
        # 其他情况（未知策略类型）
        case _:
            # 创建错误消息，抛出ValueError
            msg = f"Unknown strategy: {strategy}"
            raise ValueError(msg)

