# 导入json模块，用于处理JSON格式的数据
import json

# 导入logging模块，用于记录程序运行日志
import logging

# 从collections.abc导入Callable，表示可以调用的对象
from collections.abc import Callable

# 从typing模块导入Any，表示任何类型的变量
from typing import Any

# 导入tiktoken模块，用于处理编码相关功能
import tiktoken

# 从openai模块导入错误类型，用于处理API错误
from openai import APIConnectionError, InternalServerError, RateLimitError

# 导入自定义配置类OpenAIConfiguration
from .openai_configuration import OpenAIConfiguration

# 版权声明（2024年微软公司，MIT许可证）
# """这是OpenAI API的实用函数。"""

# 定义默认编码模型名称
DEFAULT_ENCODING = "cl100k_base"

# 初始化一个字典，存储编码模型和对应的tiktoken.Encoding对象
_encoders: dict[str, tiktoken.Encoding] = {}

# 定义可重试的错误类型列表
RETRYABLE_ERRORS: list[type[Exception]] = [
    RateLimitError,  # 速率限制错误
    APIConnectionError,  # API连接错误
    InternalServerError,  # 内部服务器错误
]

# 定义速率限制错误类型列表
RATE_LIMIT_ERRORS: list[type[Exception]] = [RateLimitError]

# 获取日志记录器，用于记录程序信息
log = logging.getLogger(__name__)

# 定义一个函数，返回计算字符串中令牌数量的函数
def get_token_counter(config: OpenAIConfiguration) -> Callable[[str], int]:
    # 获取配置中的编码模型，如果没有则使用默认值
    model = config.encoding_model or DEFAULT_ENCODING
    # 从缓存中获取编码对象，如果不存在则创建并存储
    enc = _encoders.get(model)
    if enc is None:
        enc = tiktoken.get_encoding(model)
        _encoders[model] = enc

    # 返回一个函数，计算字符串中的令牌数
    return lambda s: len(enc.encode(s))

# 定义一个函数，进行变量替换操作
def perform_variable_replacements(
    input: str, history: list[dict], variables: dict | None
) -> str:
    # 初始化结果字符串
    result = input

    # 定义一个内部函数，用于替换所有变量
    def replace_all(input: str) -> str:
        result = input
        # 如果有变量字典，遍历并替换输入字符串中的变量
        if variables:
            for entry in variables:
                result = result.replace(f"{{{entry}}}", variables[entry])
        return result

    # 对输入字符串进行变量替换
    result = replace_all(result)
    # 遍历聊天历史记录
    for i in range(len(history)):
        entry = history[i]
        # 如果条目是系统消息，替换其中的变量
        if entry.get("role") == "system":
            entry_content = entry.get("content") or ""
            entry["content"] = replace_all(entry_content)

    # 返回替换后的新字符串
    return result

# 定义一个函数，获取用于完成语言模型的缓存参数
def get_completion_cache_args(configuration: OpenAIConfiguration) -> dict:
    """这个函数用来获取让语言模型完成任务时需要的缓存设置"""
    # 返回一个字典，包含以下参数：
    return {
        # 模型的名字
        "model": configuration.model,
        # 决定生成结果多样性的温度值
        "temperature": configuration.temperature,
        # 防止重复词汇的频率惩罚值
        "frequency_penalty": configuration.frequency_penalty,
        # 控制某个词是否出现的概率
        "presence_penalty": configuration.presence_penalty,
        # 保留概率最高的p个词汇
        "top_p": configuration.top_p,
        # 最大生成的令牌（单词）数
        "max_tokens": configuration.max_tokens,
        # 生成的样本数量
        "n": configuration.n,
    }

# 定义另一个函数，获取用于完成语言模型的全部参数
def get_completion_llm_args(
    parameters: dict | None, configuration: OpenAIConfiguration
) -> dict:
    """这个函数用来获取让语言模型完成任务的所有参数"""
    # 先获取缓存参数
    cache_args = get_completion_cache_args(configuration)
    # 如果有额外的参数，合并到一起
    extra_params = parameters or {}
    # 返回合并后的完整参数字典
    return {
        **cache_args,  # 缓存参数
        **extra_params,  # 额外参数
    }

# 定义一个函数，尝试将输入的字符串解析成JSON对象
def try_parse_json_object(input: str) -> dict:
    """尝试用最好的方式把输入的字符串转化为JSON对象"""
    # 尝试将输入的字符串转换为JSON格式
    try:
        result = json.loads(input)
    # 如果转换失败，捕获错误并打印日志
    except json.JSONDecodeError:
        log.exception("加载JSON出错，输入的JSON=%s", input)
        raise  # 抛出错误
    # 如果转换成功，检查结果是否为字典
    else:
        if not isinstance(result, dict):
            raise TypeError  # 如果不是字典，抛出错误
        # 如果是字典，返回结果
        return result

# 定义一个函数，从错误中提取重试前应等待的时间
def get_sleep_time_from_error(e: Any) -> float:
    """从RateLimitError错误中获取需要等待的时间（通常在Azure中）"""
    sleep_time = 0.0  # 初始化等待时间为0
    # 如果错误是RateLimitError类型，并且错误信息包含特定字符串
    if isinstance(e, RateLimitError) and _please_retry_after in str(e):
        # 从错误信息中提取等待时间
        # 分割字符串，取第一部分，再分割"second"前面的部分
        sleep_time = int(str(e).split(_please_retry_after)[1].split(" second")[0])
    # 返回等待时间
    return sleep_time

# 定义一个常量，用于匹配错误信息中的重试提示
_please_retry_after = "Please retry after "

