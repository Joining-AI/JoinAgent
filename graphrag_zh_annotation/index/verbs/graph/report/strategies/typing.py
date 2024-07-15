# 这段代码定义了一些数据类型和类，帮助程序理解数据结构。我会用简单易懂的语言解释每一行：

# 导入一些Python库，这些库提供了特殊的功能
from collections.abc import Awaitable, Callable  # 从Python标准库导入可以等待的异步操作（Awaitable）和可调用对象（Callable）
from typing import Any  # 导入Any类型，表示任何类型的值都可以
from datashaper import VerbCallbacks  # 导入自定义的VerbCallbacks类，可能用于处理数据操作
from typing_extensions import TypedDict  # 导入TypedDict，用于创建有特定字段和类型的字典
from graphrag.index.cache import PipelineCache  # 导入PipelineCache，可能用于缓存数据管道的结果

# 这一行是版权信息，表示代码由微软公司拥有，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation. Licensed under the MIT License

# 定义模块的文档字符串，说明这个文件包含什么
"""这是一个包含'Finding'和'CommunityReport'类的模块。"""

# 继续导入库
from collections.abc import Awaitable, Callable
from typing import Any
from datashaper import VerbCallbacks
from typing_extensions import TypedDict
from graphrag.index.cache import PipelineCache

# 定义几个字典类型，它们的键是字符串，值可以是任何类型
ExtractedEntity = dict[str, Any]  # 提取的实体字典
StrategyConfig = dict[str, Any]  # 策略配置字典
RowContext = dict[str, Any]  # 行上下文字典
EntityTypes = list[str]  # 实体类型的列表
Claim = dict[str, Any]  # 声明字典

# 使用TypedDict定义一个名为Finding的类，它是一个字典，包含'summary'和'explanation'两个字段
class Finding(TypedDict):
    summary: str  # 摘要，是一个字符串
    explanation: str  # 解释，也是一个字符串

# 再定义一个名为CommunityReport的类，它也是一个字典，包含多个字段
class CommunityReport(TypedDict):
    community: str | int  # 社区名或ID，可以是字符串或整数
    title: str  # 标题，是一个字符串
    summary: str  # 摘要，是一个字符串
    full_content: str  # 完整内容，是一个字符串
    full_content_json: str  # 完整内容的JSON格式，是一个字符串
    rank: float  # 排名，是一个浮点数
    level: int  # 级别，是一个整数
    rank_explanation: str  # 排名解释，是一个字符串
    findings: list[Finding]  # 发现列表，是一个包含Finding类实例的列表

# 定义一个名为CommunityReportsStrategy的函数类型，它接受多个参数并返回一个可以等待的异步结果（可能是CommunityReport或None）
CommunityReportsStrategy = Callable[
    [  # 函数接受以下参数：
        str | int,  # 社区名或ID
        str,  # 不明确的字符串参数
        int,  # 一个整数参数
        VerbCallbacks,  # VerbCallbacks实例
        PipelineCache,  # PipelineCache实例
        StrategyConfig,  # 策略配置字典
    ],
    Awaitable[CommunityReport | None],  # 返回一个异步结果，可能是CommunityReport类实例或None
]

