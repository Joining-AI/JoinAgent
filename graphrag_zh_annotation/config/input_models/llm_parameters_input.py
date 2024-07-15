# 导入一些特殊的类型定义，帮助Python检查代码的类型正确性
from typing_extensions import NotRequired, TypedDict
# 导入自定义的枚举类型 LLMType，可能用于设置模型的类型
from graphrag.config.enums import LLMType

# 这是微软公司的版权信息，表示代码由微软创建
# 并遵循MIT许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为"LLM Parameters model"的注释，说明下面的代码是用来做什么的
"""LLM 参数模型。"""

# 使用 TypedDict 创建一个字典类，这个类的键值对有特定的类型
class LLMParametersInput(TypedDict):
    # 类内部的注释，说明这是一个 LLM 参数模型
    """LLM 参数模型。"""

    # 下面是这个字典类的键值对，每个键都有一个可选的类型（NotRequired表示可以为空）
    # api_key: 可能是字符串或空，但不是必须的
    api_key: NotRequired[str | None]

    # type: 可以是 LLMType 枚举、字符串或空，但不是必须的
    type: NotRequired[LLMType | str | None]

    # model: 可能是字符串或空，但不是必须的
    model: NotRequired[str | None]

    # max_tokens: 可能是整数、字符串或空，但不是必须的
    max_tokens: NotRequired[int | str | None]

    # request_timeout: 可能是浮点数、字符串或空，但不是必须的
    request_timeout: NotRequired[float | str | None]

    # api_base: 可能是字符串或空，但不是必须的
    api_base: NotRequired[str | None]

    # api_version: 可能是字符串或空，但不是必须的
    api_version: NotRequired[str | None]

    # organization: 可能是字符串或空，但不是必须的
    organization: NotRequired[str | None]

    # proxy: 可能是字符串或空，但不是必须的
    proxy: NotRequired[str | None]

    # cognitive_services_endpoint: 可能是字符串或空，但不是必须的
    cognitive_services_endpoint: NotRequired[str | None]

    # deployment_name: 可能是字符串或空，但不是必须的
    deployment_name: NotRequired[str | None]

    # model_supports_json: 可能是布尔值、字符串或空，但不是必须的
    model_supports_json: NotRequired[bool | str | None]

    # tokens_per_minute: 可能是整数、字符串或空，但不是必须的
    tokens_per_minute: NotRequired[int | str | None]

    # requests_per_minute: 可能是整数、字符串或空，但不是必须的
    requests_per_minute: NotRequired[int | str | None]

    # max_retries: 可能是整数、字符串或空，但不是必须的
    max_retries: NotRequired[int | str | None]

    # max_retry_wait: 可能是浮点数、字符串或空，但不是必须的
    max_retry_wait: NotRequired[float | str | None]

    # sleep_on_rate_limit_recommendation: 可能是布尔值、字符串或空，但不是必须的
    sleep_on_rate_limit_recommendation: NotRequired[bool | str | None]

    # concurrent_requests: 可能是整数、字符串或空，但不是必须的
    concurrent_requests: NotRequired[int | str | None]

