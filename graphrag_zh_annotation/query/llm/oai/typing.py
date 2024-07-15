# 导入一个叫做Enum的特殊类，用于创建枚举类型
from enum import Enum
# 导入Any和cast，它们是关于数据类型的工具，帮助确保代码的正确性
from typing import Any, cast
# 导入openai库，这个库让我们能和OpenAI的API进行交互
import openai

# 这是一个版权声明，告诉我们这段代码是微软公司的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块级别的文档字符串，描述了这是一个OpenAI包装器的选项
"""OpenAI wrapper options."""

# 再次导入Enum和Any，确保代码的清晰
from enum import Enum
from typing import Any, cast

# 再次导入openai库
import openai

# 定义一个常量列表，里面包含了OpenAI API可能抛出的错误类型
# 我们用了一个待办事项（TODO）来提醒以后更新这些错误类型
OPENAI_RETRY_ERROR_TYPES = (
    # 待办事项：当我们更新到OpenAI 1+库时，更新这些错误类型
    cast(Any, openai).RateLimitError,  # 当调用次数超过限制时会发生的错误
    cast(Any, openai).APIConnectionError,  # 如果连接到API有问题时会发生的错误
    # 待办事项：用OpenAI 1+中相似的错误类型替换这个
)

# 创建一个名为OpenaiApiType的枚举类，它继承自str（字符串）和Enum
# 枚举类用来定义两种OpenAI服务的类型
class OpenaiApiType(str, Enum):
    """OpenAI服务的种类."""

    # 枚举成员：普通OpenAI服务
    OpenAI = "openai"
    # 枚举成员：Azure上的OpenAI服务
    AzureOpenAI = "azure"

