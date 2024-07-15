# 这个代码是关于加载数据和处理数据块的模块。

# 导入cast函数，它帮助我们安全地转换数据类型
from typing import cast

# 导入pandas库，它用于处理表格数据
import pandas as pd

# 导入datashaper库的一些组件
# NoopVerbCallbacks：不做任何操作的回调函数
# TableContainer：存储表格数据的容器
# VerbInput：处理数据的动词输入
from datashaper import NoopVerbCallbacks, TableContainer, VerbInput

# 导入graphrag配置模型
from graphrag.config.models.graph_rag_config import GraphRagConfig

# 导入graphrag库中的输入加载函数
from graphrag.index.input import load_input

# 导入进度报告器的类型
from graphrag.index.progress.types import ProgressReporter

# 导入数据分块处理的动词
from graphrag.index.verbs import chunk

# 这是代码的作者和许可证信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义两个常量：
# MIN_CHUNK_SIZE：最小数据块大小，设为200
MIN_CHUNK_SIZE = 200
# MIN_CHUNK_OVERLAP：最小数据块重叠部分，设为0
MIN_CHUNK_OVERLAP = 0

# 定义一个异步函数load_docs_in_chunks，接收5个参数：根目录、配置对象、选择方法、限制数量、进度报告器和块大小（默认是最小块大小）
async def load_docs_in_chunks(
    root: str,
    config: GraphRagConfig,
    select_method: str,
    limit: int,
    reporter: ProgressReporter,
    chunk_size: int = MIN_CHUNK_SIZE,
) -> list[str]:
    """这个函数用于分块加载文档，生成提示信息"""
    
    # 加载输入数据集，根据配置和进度报告器
    dataset = await load_input(config.input, reporter, root)

    # 创建一个VerbInput对象，将数据集转换为文本单元
    input = VerbInput(input=TableContainer(table=dataset))

    # 获取配置中关于分块的策略
    chunk_strategy = config.chunks.resolved_strategy()

    # 设置较小的块大小，以避免创建过大的提示
    chunk_strategy["chunk_size"] = chunk_size
    chunk_strategy["chunk_overlap"] = MIN_CHUNK_OVERLAP

    # 使用指定策略将输入数据分块
    dataset_chunks_table_container = chunk(
        input,
        column="text",
        to="chunks",
        callbacks=NoopVerbCallbacks(),  # 使用空回调函数
        strategy=chunk_strategy,
    )

    # 将分块后的数据转换为pandas DataFrame
    dataset_chunks = cast(pd.DataFrame, dataset_chunks_table_container.table)

    # 创建一个新的DataFrame，只保留"chunks"列并将其展开
    chunks_df = pd.DataFrame(dataset_chunks["chunks"].explode())  # 忽略类型检查

    # 根据选择方法调整限制数量
    if limit <= 0 or limit > len(chunks_df):
        limit = len(chunks_df)

    # 如果选择方法是"top"，取前limit个块
    if select_method == "top":
        chunks_df = chunks_df[:limit]
    # 如果选择方法是"random"，随机选取limit个块
    elif select_method == "random":
        chunks_df = chunks_df.sample(n=limit)

    # 将DataFrame的"chunks"列转换为列表，得到文档列表
    return chunks_df["chunks"].tolist()

