# 导入一个叫做 BaseModel 的类，它来自 pydantic 模块，用于创建数据模型
from pydantic import BaseModel, ConfigDict, Field

# 导入一个名为 defaults 的模块，它在 graphrag.config 包里面，可能包含一些默认设置
import graphrag.config.defaults as defs

# 导入 LLMType，它是一个枚举类型，来自 graphrag.config.enums 模块
from graphrag.config.enums import LLMType

# 这一行是版权声明，表示代码由微软公司创作，遵循 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为 "LLM Parameters model" 的文档字符串，描述了这个代码的作用
"""

LLM 参数模型。

"""

# 再次使用 pydantic 的 BaseModel 创建一个新的数据模型，可能用来存储 LLM（可能是“大语言模型”）的参数
class LLMParameters(BaseModel):
    # 在这里，你可以添加属性和它们的规则，比如使用 Field() 来定义特定的参数
    # 但当前的代码没有定义任何属性，所以这部分是空的
    pass

# 定义一个名为LLMParameters的类，它继承自BaseModel
class LLMParameters(BaseModel):
    """这是一个关于LLM（可能是一个语言模型）参数的模型。"""

    # 创建一个ConfigDict对象，用于存储配置信息，允许额外的属性
    model_config = ConfigDict(protected_namespaces=(), extra="allow")

    # 定义一个变量api_key，用来存放访问LLM服务的API密钥，初始值为None
    api_key: str | None = Field(
        description="用来访问LLM服务的API密钥。",
        default=None,
    )

    # 定义变量type，表示要使用的LLM模型类型，初始值为LLMType的默认值
    type: LLMType = Field(
        description="要使用的LLM模型类型。",
        default=defs.LLM_TYPE
    )

    # 定义变量model，表示要使用的具体LLM模型，初始值为defs.LLM_MODEL
    model: str = Field(description="要使用的LLM模型。",
                      default=defs.LLM_MODEL)

    # 定义变量max_tokens，表示生成文本的最大令牌数，默认值为defs.LLM_MAX_TOKENS
    max_tokens: int | None = Field(
        description="生成文本时的最大令牌数。",
        default=defs.LLM_MAX_TOKENS,
    )

    # 定义变量temperature，用于控制生成文本的随机性，默认值为defs.LLM_TEMPERATURE
    temperature: float | None = Field(
        description="用于生成令牌的温度（影响随机性）。",
        default=defs.LLM_TEMPERATURE,
    )

    # 定义变量top_p，用于控制生成文本的选择策略，默认值为defs.LLM_TOP_P
    top_p: float | None = Field(
        description="用于生成令牌的top-p值。",
        default=defs.LLM_TOP_P,
    )

    # 定义变量n，表示要生成的完成文本数量，默认值为defs.LLM_N
    n: int | None = Field(
        description="要生成的完成文本数量。",
        default=defs.LLM_N,
    )

    # 定义变量request_timeout，表示请求超时时间，默认值为defs.LLM_REQUEST_TIMEOUT
    request_timeout: float = Field(
        description="请求超时时间。",
        default=defs.LLM_REQUEST_TIMEOUT
    )

    # 定义变量api_base，表示LLM API的基础URL，默认值为None
    api_base: str | None = Field(
        description="LLM API的基础URL。",
        default=None
    )

    # 定义变量api_version，表示要使用的LLM API版本，默认值为None
    api_version: str | None = Field(
        description="要使用的LLM API版本。",
        default=None
    )

    # 定义变量organization，表示LLM服务的组织名，默认值为None
    organization: str | None = Field(
        description="LLM服务的组织名。",
        default=None
    )

    # 定义变量proxy，表示LLM服务的代理服务器，默认值为None
    proxy: str | None = Field(
        description="LLM服务的代理服务器。",
        default=None
    )

    # 定义变量cognitive_services_endpoint，表示认知服务的端点，默认值为None
    cognitive_services_endpoint: str | None = Field(
        description="用于访问认知服务的端点。",
        default=None
    )

    # 定义变量deployment_name，表示LLM服务的部署名称，默认值为None
    deployment_name: str | None = Field(
        description="LLM服务的部署名称。",
        default=None
    )

    # 定义变量model_supports_json，表示模型是否支持JSON输出模式，默认值为None
    model_supports_json: bool | None = Field(
        description="模型是否支持JSON输出模式。",
        default=None
    )

    # 定义变量tokens_per_minute，表示每分钟允许的令牌数，默认值为defs.LLM_TOKENS_PER_MINUTE
    tokens_per_minute: int = Field(
        description="每分钟允许的令牌数。",
        default=defs.LLM_TOKENS_PER_MINUTE,
    )

    # 定义变量requests_per_minute，表示每分钟允许的请求次数，默认值为defs.LLM_REQUESTS_PER_MINUTE
    requests_per_minute: int = Field(
        description="每分钟允许的请求次数。",
        default=defs.LLM_REQUESTS_PER_MINUTE,
    )

    # 定义变量max_retries，表示请求的最大重试次数，默认值为defs.LLM_MAX_RETRIES
    max_retries: int = Field(
        description="请求的最大重试次数。",
        default=defs.LLM_MAX_RETRIES,
    )

    # 定义变量max_retry_wait，表示最大重试等待时间，默认值为defs.LLM_MAX_RETRY_WAIT
    max_retry_wait: float = Field(
        description="请求最大重试等待时间。",
        default=defs.LLM_MAX_RETRY_WAIT,
    )

    # 定义变量sleep_on_rate_limit_recommendation，表示是否在达到速率限制时暂停，默认值为defs.LLM_SLEEP_ON_RATE_LIMIT_RECOMMENDATION
    sleep_on_rate_limit_recommendation: bool = Field(
        description="是否在遇到速率限制建议时暂停。",
        default=defs.LLM_SLEEP_ON_RATE_LIMIT_RECOMMENDATION,
    )

    # 定义变量concurrent_requests，表示是否使用并发请求，默认值为defs.LLM_CONCURRENT_REQUESTS
    concurrent_requests: int = Field(
        description="是否为LLM服务启用并发请求。",
        default=defs.LLM_CONCURRENT_REQUESTS,
    )

