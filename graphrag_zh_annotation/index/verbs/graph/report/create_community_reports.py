# 导入logging模块，用于记录程序运行日志
import logging

# 导入Enum类，用于创建枚举类型
from enum import Enum

# 导入typing模块的cast函数，用于类型转换
from typing import cast

# 导入pandas库，用于处理数据
import pandas as pd

# 导入datashaper库中的相关类和函数
from datashaper import (
    AsyncType,  # 异步类型
    NoopVerbCallbacks,  # 无操作的动词回调
    TableContainer,  # 表容器类
    VerbCallbacks,  # 动词回调接口
    VerbInput,  # 动词输入类
    derive_from_rows,  # 从行中推断数据结构
    progress_ticker,  # 进度指示器
    verb,  # 定义动词装饰器
)

# 导入默认配置
import graphrag.config.defaults as defaults

# 导入社区报告的模式定义
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 导入缓存类
from graphrag.index.cache import PipelineCache

# 导入社区报告相关的函数
from graphrag.index.graph.extractors.community_reports import (
    get_levels,  # 获取层次
    prep_community_report_context,  # 准备社区报告上下文
)

# 导入数据处理工具
from graphrag.index.utils.ds_util import get_required_input_table

# 导入策略中的类型定义
from .strategies.typing import CommunityReport, CommunityReportsStrategy

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 模块描述
"""包含create_community_reports和load_strategy方法定义的模块。"""

# 使用logging模块获取当前模块的日志记录器
log = logging.getLogger(__name__)

# 创建一个枚举类，表示创建社区报告的策略类型
class CreateCommunityReportsStrategyType(str, Enum):
    """创建社区报告策略类型的枚举类定义。"""

    # 枚举值：图智能
    graph_intelligence = "graph_intelligence"

    # 返回枚举值的字符串表示形式
    def __repr__(self):
        """返回一个字符串表示当前枚举值"""
        return f'"{self.value}"'

# 使用verb装饰器定义一个名为"create_community_reports"的动词
@verb(name="create_community_reports")

# 定义一个异步函数，用于创建社区报告
async def create_community_reports(
    # 输入参数，包括动词输入、回调函数、缓存、策略字典，以及异步模式和线程数
    input: VerbInput,
    callbacks: VerbCallbacks,
    cache: PipelineCache,
    strategy: dict,
    async_mode: AsyncType = AsyncType.AsyncIO,
    num_threads: int = 4,
    **_kwargs,
) -> TableContainer:

    # 打印日志，显示所用的策略
    log.debug("create_community_reports strategy=%s", strategy)

    # 获取输入数据
    local_contexts = 输入数据转换成 DataFrame 类型
    nodes = 获取名为 "nodes" 的输入表并转换成 DataFrame
    community_hierarchy = 获取名为 "community_hierarchy" 的输入表并转换成 DataFrame

    # 获取节点的级别列表
    levels = 从 nodes 中获取级别信息

    # 初始化报告列表
    reports = 一个可能包含 CommunityReport 或 None 的列表

    # 创建进度条更新器
    tick = 创建一个用于更新进度条的函数

    # 加载策略类型
    runner = 根据策略字典加载对应的策略执行器

    # 遍历每个级别
    for level in levels:
        # 准备报告上下文
        level_contexts = 准备这个级别的社区报告上下文

        # 定义一个异步函数，用于生成单个报告
        async def run_generate(record):
            # 使用 runner 生成报告
            result = 等待生成报告的结果
            # 更新进度条
            tick()
            # 返回报告结果
            return result

        # 对 level_contexts 中的每一行运行 run_generate 函数，异步生成报告
        local_reports = 从 level_contexts 行数据中异步生成报告
        # 将非空的报告添加到总报告列表中
        reports.extend([lr for lr in local_reports if lr is not None])

    # 将报告列表转换成 DataFrame 并返回
    return TableContainer(table=pd.DataFrame(reports))

# 这是一个异步函数，用于生成一个社区的报告。
async def _generate_report(
    # runner 是一个策略类，用来处理报告的生成
    runner: CommunityReportsStrategy,
    # cache 是一个缓存对象，保存了数据
    cache: PipelineCache,
    # callbacks 是一组回调函数，用于在报告生成过程中做一些操作
    callbacks: VerbCallbacks,
    # strategy 是一个字典，包含了生成报告的具体方法信息
    strategy: dict,
    # community_id 是社区的唯一标识，可以是数字或字符串
    community_id: int | str,
    # community_level 是社区的等级
    community_level: int,
    # community_context 是社区的上下文信息
    community_context: str,
) -> CommunityReport | None:
    """这个函数会为一个社区生成一份报告，如果成功返回报告，否则返回 None."""
    # 使用 runner 对象，根据给定的参数（社区 ID、上下文、等级、回调和策略）来异步生成报告
    return await runner(
        community_id, community_context, community_level, callbacks, cache, strategy
    )

# 这个函数用来加载报告生成的策略方法
def load_strategy(
    # strategy 是一个枚举类型，表示报告生成的策略
    strategy: CreateCommunityReportsStrategyType,
) -> CommunityReportsStrategy:
    """根据给定的策略类型，加载对应的报告生成方法."""
    # 使用匹配表达式来判断策略类型
    match strategy:
        # 如果策略类型是 "graph_intelligence"
        case CreateCommunityReportsStrategyType.graph_intelligence:
            # 从 .strategies.graph_intelligence 模块导入 run 函数
            from .strategies.graph_intelligence import run

            # 返回 run 函数作为报告生成策略
            return run
        # 如果策略类型不是已知的
        case _:
            # 创建一个错误消息，包含未知策略的名称
            msg = f"Unknown strategy: {strategy}"
            # 抛出一个 ValueError，因为遇到了未知的策略
            raise ValueError(msg)

