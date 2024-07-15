# 导入正则表达式模块，用于处理和匹配文本模式
import re

# 导入抽象基类元类（ABCMeta）和抽象方法（abstractmethod），用于定义接口
from abc import ABCMeta, abstractmethod

# 导入迭代器的抽象基类，确保我们的类可以像迭代器一样工作
from collections.abc import Iterator

# 导入Python的类型注解库，定义变量和函数的类型
from typing import Any

# 导入进度报告器，用于跟踪和显示执行过程中的进度
from graphrag.index.progress import ProgressReporter

# 这个注释是版权声明，告诉我们这个代码的版权属于微软公司，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个模块的文档字符串，描述了包含的内容
"""这是一个包含'PipelineStorage'模型的模块。"""

# 接下来是一些导入的库，它们提供了编写代码所需的功能

# 这是一个Python类，叫做PipelineStorage，它是一个抽象基类（ABCMeta），意味着它定义了一些基本功能，但不会直接被实例化。
class PipelineStorage(metaclass=ABCMeta):
    """这个类提供了一个接口，用来存储管道（pipeline）的输出数据。"""

    # 这是一个方法，叫做find，它寻找符合特定模式的文件。
    # 参数：
    # - file_pattern: 一个正则表达式，用于匹配文件名。
    # - base_dir: 可选的起点目录。
    # - progress: 可选的进度报告器。
    # - file_filter: 可选的自定义过滤函数。
    # - max_count: 默认为-1，表示无限数量的文件。
    # 返回值：一个迭代器，返回文件名和相关信息的元组。
    @abstractmethod
    def find(
        self,
        file_pattern: re.Pattern[str],
        base_dir: str | None = None,
        progress: ProgressReporter | None = None,
        file_filter: dict[str, Any] | None = None,
        max_count=-1,
    ) -> Iterator[tuple[str, dict[str, Any]]]:
        """根据文件模式和自定义过滤器在存储中查找文件。"""

    # 这个方法是get，用于获取给定键的值。
    # 参数：
    # - key: 要获取的键。
    # - as_bytes: 是否以字节形式返回值，默认可选。
    # - encoding: 如果值是文本，使用的编码，默认可选。
    # 返回值：给定键的值。
    @abstractmethod
    async def get(
        self, key: str, as_bytes: bool | None = None, encoding: str | None = None
    ) -> Any:
        """获取指定键的值。可以决定是否以字节形式返回。"""

    # 这个方法是set，用于设置给定键的值。
    # 参数：
    # - key: 要设置的键。
    # - value: 要设置的值。
    # - encoding: 如果value是文本，使用的编码，默认可选。
    # 没有返回值。
    @abstractmethod
    async def set(
        self, key: str, value: str | bytes | None, encoding: str | None = None
    ) -> None:
        """为给定的键设置值。"""

    # 这个方法是has，检查给定键是否存在于存储中。
    # 参数：
    # - key: 要检查的键。
    # 返回值：如果键存在，返回True，否则返回False。
    @abstractmethod
    async def has(self, key: str) -> bool:
        """检查存储中是否存在指定的键。"""

    # 这个方法是delete，从存储中删除给定的键。
    # 参数：
    # - key: 要删除的键。
    # 没有返回值。
    @abstractmethod
    async def delete(self, key: str) -> None:
        """从存储中删除指定的键。"""

    # 这个方法是clear，清空整个存储。
    # 没有返回值。
    @abstractmethod
    async def clear(self) -> None:
        """清除存储中的所有内容。"""

    # 这个方法是child，创建一个新的子存储实例。
    # 参数：
    # - name: 子存储的名称，可选。
    # 返回值：一个新的PipelineStorage实例，作为当前实例的子级。
    @abstractmethod
    def child(self, name: str | None) -> "PipelineStorage":
        """创建一个子级存储实例。"""

