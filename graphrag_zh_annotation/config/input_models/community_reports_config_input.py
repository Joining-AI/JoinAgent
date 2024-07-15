# 导入一个Python库的特殊类型，叫做NotRequired，它用于表示参数可以不提供
from typing_extensions import NotRequired

# 从当前目录下的llm_config_input模块导入LLMConfigInput类
from .llm_config_input import LLMConfigInput

# 这是微软公司的版权信息，告诉我们代码的归属和使用的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块是用来定义默认配置的一些参数设置
"""Parameterization settings for the default configuration."""

# 再次导入NotRequired，确保我们有这个类型
from typing_extensions import NotRequired

# 从llm_config_input模块导入LLMConfigInput基类
from .llm_config_input import LLMConfigInput

# 定义一个新的类，叫CommunityReportsConfigInput，它是LLMConfigInput的子类
class CommunityReportsConfigInput(LLMConfigInput):
    # 这个类是关于社区报告的配置部分
    """Configuration section for community reports."""

    # 这里定义了一个属性prompt，它可以是字符串或None，但不是必需的
    prompt: NotRequired[str | None]

    # max_length属性可以是整数、字符串或None，同样不是必需的
    max_length: NotRequired[int | str | None]

    # max_input_length属性也是可选的，可以是整数、字符串或None
    max_input_length: NotRequired[int | str | None]

    # strategy属性可以是一个字典或None，也是不强制要求的
    strategy: NotRequired[dict | None]

