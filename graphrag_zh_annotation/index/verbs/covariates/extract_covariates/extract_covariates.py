# 导入logging模块，用于记录程序运行中的信息
import logging

# 导入asdict函数，将数据类对象转换为字典
from dataclasses import asdict

# 导入Enum类，用于创建枚举类型
from enum import Enum

# 导入Any和cast，它们是类型提示（typing）模块的一部分，帮助我们定义和转换变量类型
from typing import Any, cast

# 导入pandas库，用于处理表格数据
import pandas as pd

# 导入datashaper库的一些组件，用于数据操作
from datashaper import (
    AsyncType,
    TableContainer,
    VerbCallbacks,
    VerbInput,
    derive_from_rows,
    verb,
)

# 导入graphrag.index.cache中的PipelineCache，可能用于缓存数据管道
from graphrag.index.cache import PipelineCache

# 导入graphrag.index.verbs.covariates.typing中的Covariate和CovariateExtractStrategy，它们可能是定义变量策略的类
from graphrag.index.verbs.covariates.typing import Covariate, CovariateExtractStrategy

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含提取协变量（covariates）的谓词（verb）定义

# 再次导入logging，获取日志记录器
log = logging.getLogger(__name__)

# 定义一个枚举类ExtractClaimsStrategyType，表示不同的提取策略
class ExtractClaimsStrategyType(str, Enum):
    # 枚举成员：graph_intelligence，表示使用图智能的策略
    graph_intelligence = "graph_intelligence"

    # 返回枚举成员的字符串表示形式
    def __repr__(self):
        return f'"{self.value}"'

# 定义默认的实体类型列表
DEFAULT_ENTITY_TYPES = ["organization", "person", "geo", "event"]

# 使用@verb装饰器定义一个名为"extract_covariates"的谓词，它可能用于从数据中提取协变量
@verb(name="extract_covariates")

# 定义一个异步函数，用于从文本中提取信息
async def extract_covariates(
    # 输入数据
    input: VerbInput,
    # 管道缓存
    cache: PipelineCache,
    # 回调函数
    callbacks: VerbCallbacks,
    # 要分析的列名
    column: str,
    # 变量类型
    covariate_type: str,
    # 提取策略（字典或None）
    strategy: dict[str, Any] | None,
    # 异步模式，默认是AsyncIO
    async_mode: AsyncType = AsyncType.AsyncIO,
    # 实体类型列表（可选）
    entity_types: list[str] | None = None,
    # 其他参数
    **kwargs,
) -> TableContainer:
    """
    这个函数从一段文字中提取信息。

    使用方法：
    待补充
    """
    # 记录日志，显示提取策略
    log.debug("extract_covariates strategy=%s", strategy)
    
    # 如果没有指定实体类型，则使用默认值
    if entity_types is None:
        entity_types = DEFAULT_ENTITY_TYPES

    # 获取输入数据的DataFrame格式
    output = cast(pd.DataFrame, input.get_input())

    # 初始化解析后的实体映射
    resolved_entities_map = {}

    # 策略可以是空的，如果为空则使用默认值
    strategy = strategy or {}
    # 根据策略类型加载相应的提取方法
    strategy_exec = load_strategy(
        strategy.get("type", ExtractClaimsStrategyType.graph_intelligence)
    )
    # 复制策略配置，用于后续使用
    strategy_config = {**strategy}

    # 定义一个异步函数，用于处理每一行数据
    async def run_strategy(row):
        # 获取当前行的文本
        text = row[column]
        # 使用加载的策略执行方法处理文本
        result = await strategy_exec(
            text, entity_types, resolved_entities_map, callbacks, cache, strategy_config
        )
        # 从结果中创建新的行数据
        return [
            create_row_from_claim_data(row, item, covariate_type)
            for item in result.covariate_data
        ]

    # 对DataFrame中的每一行运行策略函数
    results = await derive_from_rows(
        output,
        run_strategy,
        callbacks,
        # 指定异步模式和并行线程数
        scheduling_type=async_mode,
        num_threads=kwargs.get("num_threads", 4),
    )

    # 将所有结果合并成一个新的DataFrame
    output = pd.DataFrame([item for row in results for item in row or []])

    # 返回包含结果的TableContainer对象
    return TableContainer(table=output)

# 定义一个函数，根据策略类型加载相应的提取策略方法
def load_strategy(strategy_type: ExtractClaimsStrategyType) -> CovariateExtractStrategy:
    """加载策略方法定义"""
    # 匹配策略类型并返回对应的方法
    match strategy_type:
        # 如果是图智能策略
        case ExtractClaimsStrategyType.graph_intelligence:
            # 从特定模块导入并返回运行方法
            from .strategies.graph_intelligence import run as run_gi
            return run_gi
        # 其他未知策略
        case _:
            # 抛出错误，因为策略类型未知
            msg = f"未知策略：{strategy_type}"
            raise ValueError(msg)

# 定义一个函数，叫做 create_row_from_claim_data，它需要三个参数：row（一行数据），covariate_data（保险变量数据），和 covariate_type（变量类型）
def create_row_from_claim_data(row, covariate_data: Covariate, covariate_type: str):
    """这个函数用来从保险索赔数据和输入的数据行创建新的一行数据。"""
    
    # 使用字典解包操作符（**）将输入的 'row' 和 'covariate_data' 合并到一个新的字典 'item' 中
    # asdict(covariate_data) 是把 covariate_data 转换成字典
    item = {**row, **asdict(covariate_data), "covariate_type": covariate_type}

    # 这里有一个待办事项（TODO），说明“doc_id”字段在提取时是不需要的
    # 因为在这之前已经进行了数据分块处理
    # 所以，我们删除 'item' 字典中的 "doc_id" 键值对
    del item["doc_id"]

    # 最后，返回处理后的 'item' 字典
    return item

