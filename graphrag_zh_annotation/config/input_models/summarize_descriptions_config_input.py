# 导入一个叫做NotRequired的特殊类型，它来自typing_extensions库
from typing_extensions import NotRequired

# 导入一个名为LLMConfigInput的类，它来自当前文件所在目录下的llm_config_input模块
from .llm_config_input import LLMConfigInput

# 这是微软公司的版权信息，表示代码由他们编写
# 并且代码遵循MIT许可证，这是一种允许他人自由使用、修改和分享代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个部分是关于默认配置参数的说明
# 我们要创建一个新的配置类

# 再次导入NotRequired，确保我们有这个类型
from typing_extensions import NotRequired

# 从llm_config_input模块导入LLMConfigInput类
from .llm_config_input import LLMConfigInput


# 定义一个名为SummarizeDescriptionsConfigInput的新类
# 它继承自LLMConfigInput类
class SummarizeDescriptionsConfigInput(LLMConfigInput):
    # 这个类是关于描述摘要的配置部分
    """Configuration section for description summarization."""

    # 定义一个属性prompt，它的类型可以是NotRequired的字符串或None
    prompt: NotRequired[str | None]

    # 定义一个属性max_length，它可以是NotRequired的整数、字符串或None
    max_length: NotRequired[int | str | None]

    # 定义一个属性strategy，它可以是NotRequired的字典或None
    strategy: NotRequired[dict | None]

