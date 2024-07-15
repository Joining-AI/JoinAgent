# 导入json模块，它帮助我们处理JSON格式的数据
import json

# 从collections.abc导入Hashable，这是一个接口，确保对象可以哈希，用于字典和集合
from collections.abc import Hashable

# 从typing模块导入Any和cast，Any表示任何类型的变量，cast用来安全地转换类型
from typing import Any, cast

# 从graphrag.llm.types导入LLMConfig，这是程序中定义的一个特定配置类
from graphrag.llm.types import LLMConfig

# 这一行是版权声明，告诉我们这个代码是微软公司的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了接下来定义的类是关于OpenAI配置的
"""OpenAI Configuration类的定义。"""

# 定义一个名为_non_blank的函数，接收一个可能是字符串或None的值
def _non_blank(value: str | None) -> str | None:
    # 如果传入的值是None，直接返回None
    if value is None:
        return None
    # 使用strip()方法去除字符串两边的空白字符
    stripped = value.strip()
    # 如果去除空白后的字符串是空的，返回None，否则返回处理过的字符串
    return None if stripped == "" else value

# 这是一个定义OpenAI配置类的代码，用来存储和管理与OpenAI API交互时的参数。

class OpenAIConfiguration(Hashable, LLMConfig):
    # 这个类是用来保存OpenAI API的设置信息的。
    
    # 核心配置
    _api_key: str           # API密钥，用于身份验证
    _model: str             # 使用的模型名称
    
    # 其他配置
    _api_base: str | None   # API的基础URL
    _api_version: str | None  # API的版本号
    _cognitive_services_endpoint: str | None  # 认知服务端点
    _deployment_name: str | None  # 部署名称
    _organization: str | None  # 组织名称
    _proxy: str | None       # 代理服务器地址

    # 操作配置
    _n: int | None          # 生成的回复数量
    _temperature: float | None  # 控制回复随机性的温度值
    _frequency_penalty: float | None  # 频率惩罚，避免重复的单词
    _presence_penalty: float | None  # 存在惩罚，控制某些单词出现的频率
    _top_p: float | None     # 保留概率最高的p个词汇
    _max_tokens: int | None  # 最大输出的令牌数
    _response_format: str | None  # 响应格式
    _logit_bias: dict[str, float] | None  # 用于调整模型预测的字典
    _stop: list[str] | None  # 停止生成的词列表

    # 重试逻辑
    _max_retries: int | None  # 最大重试次数
    _max_retry_wait: float | None  # 最大重试等待时间
    _request_timeout: float | None  # 请求超时时间

    # 原始配置对象
    _raw_config: dict

    # 特性标志
    _model_supports_json: bool | None  # 模型是否支持JSON

    # 自定义配置
    _tokens_per_minute: int | None  # 每分钟允许的令牌数
    _requests_per_minute: int | None  # 每分钟允许的请求数
    _concurrent_requests: int | None  # 同时进行的请求数量
    _encoding_model: str | None  # 编码模型
    _sleep_on_rate_limit_recommendation: bool | None  # 是否在达到速率限制时休眠

    def __init__(self,
                 config: dict,  # 初始化方法，传入一个包含配置信息的字典
                 ):
        # 定义初始化方法，从字典中获取并设置各个属性的值

        # 函数定义，用于从字典中安全地获取不同类型的值
        # lookup_required: 获取必填的字符串
        # lookup_str: 获取可选的字符串
        # lookup_int: 获取可选的整数
        # lookup_float: 获取可选的浮点数
        # lookup_dict: 获取可选的字典
        # lookup_list: 获取可选的列表
        # lookup_bool: 获取可选的布尔值

        # 使用定义的函数设置各个属性的值
        self._api_key = lookup_required("api_key")
        # ...
        self._sleep_on_rate_limit_recommendation = lookup_bool("sleep_on_rate_limit_recommendation")
        self._raw_config = config

    # 属性访问器方法，提供对私有属性的友好访问
    # 例如：api_key, model, n 等等
    # 具体方法定义省略，它们只是返回或设置对应的私有属性值

    # lookup方法：从原始配置字典中查找指定键的值
    # __str__方法：将配置对象转换为美化过的字符串（JSON格式）
    # __repr__方法：返回表示该对象的字符串
    # __eq__方法：比较两个配置对象是否相等
    # __hash__方法：计算配置对象的哈希值，用于比较和存储

