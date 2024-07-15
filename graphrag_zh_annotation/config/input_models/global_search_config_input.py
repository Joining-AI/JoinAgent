# 导入两个特殊类型的类，NotRequired 和 TypedDict，它们帮助我们定义更严格的字典类型
from typing_extensions import NotRequired, TypedDict

# 这是微软公司的一个代码，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段代码定义了一些参数设置，用于默认配置

# 从typing_extensions导入NotRequired和TypedDict模块

# 定义一个名为GlobalSearchConfigInput的类，它是TypedDict的子类
class GlobalSearchConfigInput(TypedDict):
    # 这个类代表的是缓存的默认配置部分

    # 下面是类中定义的字典键值对，每个键都有一个可选的类型（int, str或None）
    # "max_tokens" 键，值可以是NotRequired的int, str或None，表示这不是必需的参数
    max_tokens: NotRequired[int | str | None]

    # "data_max_tokens" 键，同上
    data_max_tokens: NotRequired[int | str | None]

    # "map_max_tokens" 键，同上
    map_max_tokens: NotRequired[int | str | None]

    # "reduce_max_tokens" 键，同上
    reduce_max_tokens: NotRequired[int | str | None]

    # "concurrency" 键，同上，表示并行度
    concurrency: NotRequired[int | str | None]

