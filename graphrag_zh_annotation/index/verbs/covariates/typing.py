# 导入必要的模块，让程序可以使用特定的功能
from collections.abc import Awaitable, Callable, Iterable  # 引入三种抽象基类，用于定义类型
from dataclasses import dataclass  # 引入数据类装饰器，用于创建简单的数据结构
from typing import Any  # 引入Any类型，代表任何类型的数据

from datashaper import VerbCallbacks  # 引入VerbCallbacks，可能是一个处理数据的回调函数集合
from graphrag.index.cache import PipelineCache  # 引入PipelineCache，可能是一个缓存管道的类

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件包含了两个数据类：Covariate和CovariateExtractionResult

# 导入之前提到的模块
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from typing import Any

from datashaper import VerbCallbacks
from graphrag.index.cache import PipelineCache


# 定义一个数据类Covariate，用来存储有关变量的信息
@dataclass
class Covariate:
    # 类中的属性，表示变量类型、主题ID、主题类型等
    covariate_type: str | None = None  # 变量类型，可能是字符串或None
    subject_id: str | None = None  # 主题ID，可能是字符串或None
    subject_type: str | None = None  # 主题类型，可能是字符串或None
    object_id: str | None = None  # 对象ID，可能是字符串或None
    object_type: str | None = None  # 对象类型，可能是字符串或None
    type: str | None = None  # 类型，可能是字符串或None
    status: str | None = None  # 状态，可能是字符串或None
    start_date: str | None = None  # 开始日期，可能是字符串或None
    end_date: str | None = None  # 结束日期，可能是字符串或None
    description: str | None = None  # 描述，可能是字符串或None
    source_text: list[str] | None = None  # 源文本，可能是字符串列表或None
    doc_id: str | None = None  # 文档ID，可能是字符串或None
    record_id: int | None = None  # 记录ID，可能是整数或None
    id: str | None = None  # ID，可能是字符串或None


# 定义另一个数据类CovariateExtractionResult，用于存储提取变量结果
@dataclass
class CovariateExtractionResult:
    # 类中的属性，是一个Covariate对象的列表
    covariate_data: list[Covariate]  # 变量数据，是一个Covariate类型的列表


# 定义一个函数类型CovariateExtractStrategy，它接受多个参数并返回一个等待异步完成的CovariateExtractionResult
# 这个函数可能用于从数据中提取Covariate对象
CovariateExtractStrategy = Callable[
    [
        Iterable[str],  # 字符串的可迭代对象，可能是关键词
        list[str],  # 字符串列表，可能是过滤条件
        dict[str, str],  # 字符串到字符串的字典，可能是其他配置
        VerbCallbacks,  # 之前导入的VerbCallbacks对象
        PipelineCache,  # 缓存管道对象
        dict[str, Any],  # 字符串到任意类型的字典，可能是额外的参数
    ],
    Awaitable[CovariateExtractionResult],  # 返回一个等待的CovariateExtractionResult对象
]

