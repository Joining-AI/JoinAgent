# 导入一个叫做NotRequired的特殊类型，它来自typing_extensions库
from typing_extensions import NotRequired

# 从当前文件夹下的llm_config_input模块导入LLMConfigInput类
from .llm_config_input import LLMConfigInput

# 这段文字是版权信息，表示代码由微软公司2024年创建，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个描述性字符串，说明下面的代码是关于默认配置的参数设置
"""Parameterization settings for the default configuration."""

# 再次导入NotRequired，可能是为了确保它被正确地引入
from typing_extensions import NotRequired

# 从llm_config_input模块导入LLMConfigInput类（这里和上面一行相同，可能是一种编程习惯）
from .llm_config_input import LLMConfigInput


# 定义一个名为EntityExtractionConfigInput的新类，它继承自LLMConfigInput
class EntityExtractionConfigInput(LLMConfigInput):
    # 这个类是关于实体提取配置的
    """Configuration section for entity extraction."""

    # 定义一个属性prompt，它的类型可以是NotRequired的str或None
    prompt: NotRequired[str | None]

    # 定义一个属性entity_types，它的类型可以是NotRequired的list of str, str或None
    entity_types: NotRequired[list[str] | str | None]

    # 定义一个属性max_gleanings，它的类型可以是NotRequired的int, str或None
    max_gleanings: NotRequired[int | str | None]

    # 定义一个属性strategy，它的类型可以是NotRequired的字典或None
    strategy: NotRequired[dict | None]

