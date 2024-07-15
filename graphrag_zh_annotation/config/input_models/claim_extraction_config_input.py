# 导入一个叫做NotRequired的特殊类型，它来自typing_extensions库
from typing_extensions import NotRequired

# 从当前文件夹下的llm_config_input模块导入LLMConfigInput类
from .llm_config_input import LLMConfigInput

# 这是微软公司的版权信息，2024年
# 它遵循MIT许可证，这是一种开源软件许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个代码的作用，关于默认配置的参数设置
"""Parameterization settings for the default configuration."""

# 再次导入NotRequired，确保我们有这个类型
from typing_extensions import NotRequired

# 从llm_config_input导入LLMConfigInput类
from .llm_config_input import LLMConfigInput

# 定义一个新类ClaimExtractionConfigInput，它是LLMConfigInput的子类
class ClaimExtractionConfigInput(LLMConfigInput):
    # 这个类是关于"声明提取"的配置部分
    """Configuration section for claim extraction."""

    # 这些是类中的属性，表示配置选项，它们可能不需要（NotRequired）
    # enabled：是否启用，可以是布尔值或None
    enabled: NotRequired[bool | None]

    # prompt：提示信息，可以是字符串或None
    prompt: NotRequired[str | None]

    # description：描述，可以是字符串或None
    description: NotRequired[str | None]

    # max_gleanings：最大收获数量，可以是整数、字符串或None
    max_gleanings: NotRequired[int | str | None]

    # strategy：策略，可以是字典或None
    strategy: NotRequired[dict | None]

