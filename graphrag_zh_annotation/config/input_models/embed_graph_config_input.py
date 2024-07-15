# 导入两个特殊类型的类，它们来自"typing_extensions"库
from typing_extensions import NotRequired, TypedDict

# 这是微软公司的版权信息，告诉我们代码的归属和许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段代码定义了一些参数设置，用于默认配置
"""Parameterization settings for the default configuration."""

# 再次导入NotRequired和TypedDict，确保它们在下面的代码中可用
from typing_extensions import NotRequired, TypedDict


# 定义一个名为EmbedGraphConfigInput的类，它是一个特殊的字典（TypedDict）
class EmbedGraphConfigInput(TypedDict):
    # 这个类是关于Node2Vec的默认配置部分
    """The default configuration section for Node2Vec."""

    # 下面是这个类中的键值对，每个键都是一个可能的配置选项
    # "enabled"选项可以是不需要的布尔值、字符串或None
    enabled: NotRequired[bool | str | None]

    # "num_walks"选项可以是不需要的整数、字符串或None
    num_walks: NotRequired[int | str | None]

    # "walk_length"选项可以是不需要的整数、字符串或None
    walk_length: NotRequired[int | str | None]

    # "window_size"选项可以是不需要的整数、字符串或None
    window_size: NotRequired[int | str | None]

    # "iterations"选项可以是不需要的整数、字符串或None
    iterations: NotRequired[int | str | None]

    # "random_seed"选项可以是不需要的整数、字符串或None
    random_seed: NotRequired[int | str | None]

    # "strategy"选项可以是不需要的字典或None
    strategy: NotRequired[dict | None]

