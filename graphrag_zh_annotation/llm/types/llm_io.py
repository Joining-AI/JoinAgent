# 这是一个 Python 程序，它定义了两个类：LLMInput 和 LLMOutput。这些类用于处理与语言模型交互的数据。

# 导入必要的模块，让程序能够使用数据类、泛型和类型注解
from dataclasses import dataclass, field  # 数据类和字段
from typing import Generic, TypeVar  # 泛型和类型变量
from typing_extensions import NotRequired, TypedDict  # 更多类型的注解选项
from .llm_callbacks import IsResponseValidFn  # 从 llm_callbacks 模块导入一个检查函数

# 版权声明
# ...

# 定义一个字典类型 LLMInput，用于存储调用 LLM 时的输入信息
class LLMInput(TypedDict):
    # LLM 调用的名称，可能不需要
    name: NotRequired[str]  # 名称，如果有的话

    # 是否尝试获取 JSON 输出
    json: NotRequired[bool]  # 如果是真，要获取 JSON

    # 验证 LLM 响应的函数
    is_response_valid: NotRequired[IsResponseValidFn]  # 用于验证响应的函数

    # 提示中用到的变量替换
    variables: NotRequired[dict]  # 变量替换字典

    # LLM 调用的历史记录
    history: NotRequired[list[dict]]  # 聊天模式的历史记录

    # 附加的模型参数
    model_parameters: NotRequired[dict]  # 用于 LLM 调用的额外参数


# 定义一个泛型类 LLMOutput，表示 LLM 调用的输出结果
T = TypeVar("T")  # 定义一个类型变量 T

@dataclass
class LLMOutput(Generic[T]):
    # LLM 的输出结果
    output: T | None  # 输出结果，可能是任何类型或 None

    # LLM 的 JSON 输出，如果有的话
    json: dict | None = field(default=None)  # JSON 输出，如果没有则为 None

    # LLM 调用的历史记录，如果有的话
    history: list[dict] | None = field(default=None)  # 聊天模式的历史记录，如果没有则为 None

