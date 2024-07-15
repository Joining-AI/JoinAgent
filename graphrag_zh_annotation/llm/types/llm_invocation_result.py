# 导入两个库，dataclasses用来创建数据类，typing里的Generic和TypeVar用于定义泛型
from dataclasses import dataclass
from typing import Generic, TypeVar

# 定义一个类型变量T，它代表任何可能的数据类型
T = TypeVar("T")

# 这个是OpenAI DataShaper包的类型定义部分

# 使用dataclass装饰器创建一个类，叫做LLMInvocationResult，它是一个泛型类（Generic）
# 泛型类意味着这个类可以持有任何类型的数据，由T代表
@dataclass
class LLMInvocationResult(Generic[T]):
    # 这个类表示一个大语言模型调用的结果
    # 结果可能是任何类型（由T决定），也可能为None
    result: T | None
    # 注释：这是大语言模型调用的结果

    # 调用结果的操作名称
    name: str
    # 注释：这是结果的操作名

    # 调用尝试的次数
    num_retries: int
    # 注释：这是尝试调用的次数

    # 大语言模型调用的总时间（以秒为单位）
    total_time: float
    # 注释：这是调用总共花费的时间

    # 单次调用的网络时间列表
    call_times: list[float]
    # 注释：这是每次调用的网络时间

    # 输入的令牌（比如单词或字符）数量
    input_tokens: int
    # 注释：这是输入的令牌数

    # 输出的令牌数量
    output_tokens: int
    # 注释：这是输出的令牌数

