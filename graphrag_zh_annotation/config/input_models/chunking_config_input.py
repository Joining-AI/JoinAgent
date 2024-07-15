# 导入两个特殊的Python库，用于更精确的数据类型定义
from typing_extensions import NotRequired, TypedDict

# 这是微软公司的版权信息，表示代码由微软创建
# 并遵循MIT许可证，这是一种允许他人自由使用、修改和分享代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对代码功能的简单描述
"""这是一些关于默认配置参数设置的代码。"""

# 再次导入NotRequired和TypedDict，确保它们在类定义中可用
from typing_extensions import NotRequired, TypedDict


# 定义一个名为ChunkingConfigInput的类，它是一个字典类型的特殊版本（TypedDict）
class ChunkingConfigInput(TypedDict):
    # 这个类用于存储有关数据分块的配置信息
    """这是关于数据分块的配置部分。"""

    # 下面是类中定义的键值对，每个键都有一个可选的数据类型
    # size: 可能是整数、字符串或None，但不是必须的（NotRequired）
    size: NotRequired[int | str | None]

    # overlap: 可能是整数、字符串或None，但不是必须的
    overlap: NotRequired[int | str | None]

    # group_by_columns: 可能是一个包含字符串的列表、单个字符串或None，但不是必须的
    group_by_columns: NotRequired[list[str] | str | None]

    # strategy: 可能是一个字典或None，但不是必须的
    strategy: NotRequired[dict | None]

