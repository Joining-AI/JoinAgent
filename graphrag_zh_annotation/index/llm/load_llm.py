# 这段代码是用Python编写的，它导入了一些库并定义了一个函数，用于加载语言模型（LLM）工具。
# 让我们逐行解释：

# 导入未来的注解特性，允许在Python 3.7及以下版本使用Python 3.7以上的语法
from __future__ import annotations

# 引入异步I/O库，用于处理并发任务
import asyncio

# 引入日志模块，用于记录程序运行时的信息
import logging

# 使用typing库来指定类型，帮助代码检查和理解
from typing import TYPE_CHECKING, Any

# 从graphrag.config.enums模块导入LLMType枚举类，表示不同的LLM类型
from graphrag.config.enums import LLMType

# 从graphrag.llm模块导入多个类和函数，它们与LLM相关
from graphrag.llm import (
    CompletionLLM,
    EmbeddingLLM,
    LLMCache,
    LLMLimiter,
    MockCompletionLLM,
    OpenAIConfiguration,
    create_openai_chat_llm,
    create_openai_client,
    create_openai_completion_llm,
    create_openai_embedding_llm,
    create_tpm_rpm_limiters,
)

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块级别的文档字符串，描述这个文件的作用
"""Load language model utilities."""

# 如果TYPE_CHECKING为真（通常在类型检查时），导入以下库
if TYPE_CHECKING:
    from datashaper import VerbCallbacks

    from graphrag.index.cache import PipelineCache
    from graphrag.index.typing import ErrorHandlerFn

# 初始化一个日志器，用于记录程序的日志信息
log = logging.getLogger(__name__)

# 创建两个字典，分别存储信号量（限制并发访问）和速率限制器
_semaphores: dict[str, asyncio.Semaphore] = {}
_rate_limiters: dict[str, LLMLimiter] = {}

# 定义一个函数，用于加载语言模型
def load_llm(
    # 输入参数：LLM的名称、类型、回调对象、缓存（可选）、LLM配置（可选），以及一个聊天模式标志
    name: str,
    llm_type: LLMType,
    callbacks: VerbCallbacks,
    cache: PipelineCache | None,
    llm_config: dict[str, Any] | None = None,
    chat_only=False,
) -> CompletionLLM:
    # 创建一个错误处理器函数
    on_error = _create_error_handler(callbacks)

    # 检查是否已知LLM类型
    if llm_type in loaders:
        # 如果是聊天模式但该LLM不支持，抛出错误
        if chat_only and not loaders[llm_type]["chat"]:
            msg = f"LLM type {llm_type} does not support chat"
            raise ValueError(msg)
        # 如果有缓存，创建一个新的子缓存
        if cache is not None:
            cache = cache.child(name)

        # 根据LLM类型加载相应的LLM
        loader = loaders[llm_type]
        return loader["load"](on_error, cache, llm_config or {})

    # 如果未知LLM类型，抛出错误
    msg = f"Unknown LLM type {llm_type}"
    raise ValueError(msg)

# 定义一个函数，加载特定类型的大型语言模型（LLM）嵌入
def load_llm_embeddings(
    # 输入的名字，用来识别LLM
    name: str,
    # LLM的类型，比如OpenAI等
    llm_type: LLMType,
    # 回调函数集合，用于处理错误
    callbacks: VerbCallbacks,
    # 缓存对象，可选
    cache: PipelineCache | None,
    # LLM的配置信息，字典形式，可选
    llm_config: dict[str, Any] | None = None,
    # 是否只用于聊天，布尔值，默认False
    chat_only=False,
) -> EmbeddingLLM:
    """加载用于实体提取链的LLM"""
    
    # 创建一个错误处理函数
    on_error = _create_error_handler(callbacks)

    # 检查是否已知LLM类型
    if llm_type在loaders字典里:
        # 如果只用于聊天，但该LLM类型不支持聊天，抛出错误
        if chat_only并且not loaders[llm_type]["chat"]:
            错误信息 = f"LLM类型{llm_type}不支持聊天"
            抛出 ValueError(错误信息)

        # 如果有缓存，创建子级缓存
        if cache 不是 None:
            cache = cache的子级(name)

        # 根据LLM类型加载模型
        返回 loaders[llm_type]["load"](on_error, cache, llm_config 或者 {})

    # 如果LLM类型未知，抛出错误
    错误信息 = f"未知的LLM类型{llm_type}"
    抛出 ValueError(错误信息)


# 内部辅助函数，创建一个处理错误的回调函数
def _create_error_handler(callbacks: VerbCallbacks) -> ErrorHandlerFn:
    # 定义on_error函数，处理错误
    def on_error(
        # 错误对象，可选
        error: BaseException | None = None,
        # 错误堆栈信息，可选
        stack: str | None = None,
        # 错误详细信息，可选
        details: dict | None = None,
    ) -> None:
        # 调用回调函数，报告错误
        callbacks.error("Error Invoking LLM", error, stack, details)

    # 返回这个错误处理函数
    返回 on_error


# 内部辅助函数，加载OpenAI完成型LLM
def _load_openai_completion_llm(
    # 错误处理函数
    on_error: ErrorHandlerFn,
    # LLM缓存对象
    cache: LLMCache,
    # LLM配置，字典形式
    config: dict[str, Any],
    # 是否使用Azure，布尔值，默认False
    azure=False,
):
    # 使用配置信息创建OpenAI完成型LLM
    返回 _create_openai_completion_llm(
        # 创建OpenAI配置对象
        OpenAIConfiguration({
            # 合并基础配置和用户提供的配置
            **_get_base_config(config),
            # 模型名称，默认"gpt-4-turbo-preview"
            "model": config.get("model", "gpt-4-turbo-preview"),
            # 部署名称，从config获取
            "deployment_name": config.get("deployment_name"),
            # 温度参数，控制生成多样性，从config获取，默认0.0
            "temperature": config.get("temperature", 0.0),
            # 频率惩罚，从config获取，默认0
            "frequency_penalty": config.get("frequency_penalty", 0),
            # 存在惩罚，从config获取，默认0
            "presence_penalty": config.get("presence_penalty", 0),
            # 保留概率，从config获取，默认1
            "top_p": config.get("top_p", 1),
            # 最大生成令牌数，从config获取，默认4000
            "max_tokens": config.get("max_tokens", 4000),
            # 采样次数，从config获取
            "n": config.get("n"),
        }),
        # 错误处理函数
        on_error,
        # 缓存对象
        cache,
        # 是否使用Azure
        azure,
    )

# 定义一个函数，用于加载OpenAI的聊天语言模型
def _load_openai_chat_llm(
    on_error,  # 一个处理错误的函数
    cache,  # 用于存储模型数据的对象
    config,  # 包含模型配置的字典
    azure=False,  # 指示是否使用Azure服务，默认为False
):
    # 创建OpenAI的聊天语言模型，传入配置、错误处理函数、缓存对象和Azure标志
    return _create_openai_chat_llm(
        # 根据给定的配置创建OpenAI配置对象
        OpenAIConfiguration({
            # 合并基础配置和用户提供的配置
            **_get_base_config(config),
            "model": config.get("model", "gpt-4-turbo-preview"),  # 获取或设置默认的模型名称
            "deployment_name": config.get("deployment_name"),  # 获取部署名称
            "temperature": config.get("temperature", 0.0),  # 获取温度参数，默认为0.0
            "frequency_penalty": config.get("frequency_penalty", 0),  # 获取频率惩罚，默认为0
            "presence_penalty": config.get("presence_penalty", 0),  # 获取存在惩罚，默认为0
            "top_p": config.get("top_p", 1),  # 获取top_p参数，默认为1
            "max_tokens": config.get("max_tokens"),  # 获取最大令牌数
            "n": config.get("n"),  # 获取n参数
        }),
        on_error,
        cache,
        azure,
    )

# 定义一个函数，用于加载OpenAI的嵌入式语言模型
def _load_openai_embeddings_llm(
    on_error,
    cache,
    config,
    azure=False,
):
    # TODO: 这里需要注入缓存功能，但目前没有实现
    # 创建OpenAI的嵌入式语言模型，传入配置、错误处理函数、缓存对象和Azure标志
    return _create_openai_embeddings_llm(
        # 根据给定的配置创建OpenAI配置对象
        OpenAIConfiguration({
            # 合并基础配置和用户提供的配置
            **_get_base_config(config),
            "model": config.get(
                "embeddings_model",
                config.get("model", "text-embedding-3-small")
            ),  # 获取或设置默认的嵌入模型名称
            "deployment_name": config.get("deployment_name"),  # 获取部署名称
        }),
        on_error,
        cache,
        azure,
    )

# 定义一个函数，用于加载Azure上的OpenAI完成语言模型
def _load_azure_openai_completion_llm(
    on_error,
    cache,
    config,
):
    # 通过调用_openai_completion_llm函数并传入True作为Azure标志来加载模型
    return _load_openai_completion_llm(on_error, cache, config, True)

# 定义一个函数，用于加载Azure上的OpenAI聊天语言模型
def _load_azure_openai_chat_llm(
    on_error,
    cache,
    config,
):
    # 通过调用_load_openai_chat_llm函数并传入True作为Azure标志来加载模型
    return _load_openai_chat_llm(on_error, cache, config, True)

# 定义一个函数，用于加载Azure上的OpenAI嵌入式语言模型
def _load_azure_openai_embeddings_llm(
    on_error,
    cache,
    config,
):
    # 通过调用_load_openai_embeddings_llm函数并传入True作为Azure标志来加载模型
    return _load_openai_embeddings_llm(on_error, cache, config, True)

# 定义一个函数_get_base_config，接收一个字典config作为参数
def _get_base_config(config: dict[str, Any]) -> dict[str, Any]:
    # 从config中获取"api_key"的值，如果没有就返回None
    api_key = config.get("api_key")

    # 创建一个新的字典
    return {
        # 把config中的所有键值对复制到新字典中
        **config,
        # 设置默认值
        "api_key": api_key,       # 如果有api_key就用它，没有就用上面获取的值
        "api_base": config.get("api_base"),   # 获取"api_base"的值
        "api_version": config.get("api_version"),  # 获取"api_version"的值
        "organization": config.get("organization"),  # 获取"organization"的值
        "proxy": config.get("proxy"),  # 获取"proxy"的值
        "max_retries": config.get("max_retries", 10),  # 获取"max_retries"，如果没有就设为10
        "request_timeout": config.get("request_timeout", 60.0),  # 获取"request_timeout"，如果没有就设为60秒
        "model_supports_json": config.get("model_supports_json"),  # 获取"model_supports_json"的值
        "concurrent_requests": config.get("concurrent_requests", 4),  # 获取"concurrent_requests"，如果没有就设为4
        "encoding_model": config.get("encoding_model", "cl100k_base"),  # 获取"encoding_model"，如果没有就设为"cl100k_base"
        "cognitive_services_endpoint": config.get("cognitive_services_endpoint"),  # 获取"cognitive_services_endpoint"的值
    }

# 定义一个函数_load_static_response，接收错误处理函数_on_error、缓存对象_cache和配置字典config作为参数
def _load_static_response(
    _on_error: ErrorHandlerFn, _cache: PipelineCache, config: dict[str, Any]
) -> CompletionLLM:
    # 使用config中的"responses"键的值（如果存在的话，否则为空列表）创建一个MockCompletionLLM对象并返回
    return MockCompletionLLM(config.get("responses", []))

# 创建一个名为loaders的字典，用来根据不同的LLMType加载不同的函数和聊天功能状态
loaders = {
    # LLMType.OpenAI: 加载_openai_completion_llm函数，不支持聊天
    LLMType.OpenAI: {
        "load": _load_openai_completion_llm,
        "chat": False,
    },
    # LLMType.AzureOpenAI: 加载_azure_openai_completion_llm函数，不支持聊天
    LLMType.AzureOpenAI: {
        "load": _load_azure_openai_completion_llm,
        "chat": False,
    },
    # LLMType.OpenAIChat: 加载_openai_chat_llm函数，支持聊天
    LLMType.OpenAIChat: {
        "load": _load_openai_chat_llm,
        "chat": True,
    },
    # LLMType.AzureOpenAIChat: 加载_azure_openai_chat_llm函数，支持聊天
    LLMType.AzureOpenAIChat: {
        "load": _load_azure_openai_chat_llm,
        "chat": True,
    },
    # LLMType.OpenAIEmbedding: 加载_openai_embeddings_llm函数，不支持聊天
    LLMType.OpenAIEmbedding: {
        "load": _load_openai_embeddings_llm,
        "chat": False,
    },
    # LLMType.AzureOpenAIEmbedding: 加载_azure_openai_embeddings_llm函数，不支持聊天
    LLMType.AzureOpenAIEmbedding: {
        "load": _load_azure_openai_embeddings_llm,
        "chat": False,
    },
    # LLMType.StaticResponse: 加载_load_static_response函数，不支持聊天
    LLMType.StaticResponse: {
        "load": _load_static_response,
        "chat": False,
    },
}

# 这个函数创建了一个用于OpenAI聊天的llm（可能是一种语言模型）
def _create_openai_chat_llm(
    configuration: OpenAIConfiguration,  # 输入的配置信息
    on_error: ErrorHandlerFn,  # 错误处理函数
    cache: LLMCache,  # 缓存对象
    azure=False,  # 是否使用Azure服务，默认为False
) -> CompletionLLM:  # 返回的结果是一个CompletionLLM对象
    """创建OpenAI聊天llm"""
    # 创建OpenAI客户端
    client = create_openai_client(configuration=configuration, azure=azure)
    # 创建限流器，限制请求速度
    limiter = _create_limiter(configuration)
    # 创建信号量，用于同步多线程访问
    semaphore = _create_semaphore(configuration)
    # 使用上面创建的对象创建OpenAI聊天llm
    return create_openai_chat_llm(
        client, configuration, cache, limiter, semaphore, on_error=on_error
    )

# 这个函数创建了一个用于OpenAI完成的llm
def _create_openai_completion_llm(
    configuration: OpenAIConfiguration,  # 输入的配置信息
    on_error: ErrorHandlerFn,  # 错误处理函数
    cache: LLMCache,  # 缓存对象
    azure=False,  # 是否使用Azure服务，默认为False
) -> CompletionLLM:  # 返回的结果是一个CompletionLLM对象
    """创建OpenAI完成llm"""
    # 同上，创建OpenAI客户端、限流器和信号量
    client = create_openai_client(configuration=configuration, azure=azure)
    limiter = _create_limiter(configuration)
    semaphore = _create_semaphore(configuration)
    # 使用创建的对象创建OpenAI完成llm
    return create_openai_completion_llm(
        client, configuration, cache, limiter, semaphore, on_error=on_error
    )

# 这个函数创建了一个用于OpenAI嵌入式的llm
def _create_openai_embeddings_llm(
    configuration: OpenAIConfiguration,  # 输入的配置信息
    on_error: ErrorHandlerFn,  # 错误处理函数
    cache: LLMCache,  # 缓存对象
    azure=False,  # 是否使用Azure服务，默认为False
) -> EmbeddingLLM:  # 返回的结果是一个EmbeddingLLM对象
    """创建OpenAI嵌入式llm"""
    # 同上，创建OpenAI客户端、限流器和信号量
    client = create_openai_client(configuration=configuration, azure=azure)
    limiter = _create_limiter(configuration)
    semaphore = _create_semaphore(configuration)
    # 使用创建的对象创建OpenAI嵌入式llm
    return create_openai_embedding_llm(
        client, configuration, cache, limiter, semaphore, on_error=on_error
    )

# 这个函数创建了一个限流器，用于控制请求速率
def _create_limiter(configuration: OpenAIConfiguration) -> LLMLimiter:
    # 获取限速名称，如果没有设置，则用"default"代替
    limit_name = configuration.model or configuration.deployment_name or "default"
    # 检查是否已经创建过该限流器
    if limit_name not in _rate_limiters:
        # 从配置中获取每分钟令牌数和每分钟请求数
        tpm = configuration.tokens_per_minute
        rpm = configuration.requests_per_minute
        # 打印日志，记录创建的限流器信息
        log.info("创建TPM/RPM限流器，名称：%s, TPM：%s, RPM：%s", limit_name, tpm, rpm)
        # 创建限流器
        _rate_limiters[limit_name] = create_tpm_rpm_limiters(configuration)
    # 返回对应的限流器
    return _rate_limiters[limit_name]

# 定义一个函数_create_semaphore，它接收一个名为configuration的参数，这个参数类型是OpenAIConfiguration
def _create_semaphore(configuration: OpenAIConfiguration) -> asyncio.Semaphore | None:

    # 获取配置中的模型名称（如果有的话），如果没有则尝试获取部署名称，如果都没有就用"default"代替
    limit_name = configuration.model or configuration.deployment_name or "default"

    # 从配置中获取并发请求的数量
    concurrency = configuration.concurrent_requests

    # 如果并发数量为零，跳过信号量设置，因为不需要限制
    if not concurrency:
        # 打印日志信息，表示对limit_name没有并发限制
        log.info("no concurrency limiter for %s", limit_name)
        return None  # 返回None，表示没有信号量

    # 检查信号量字典中是否已经存在limit_name对应的信号量
    if limit_name not in _semaphores:

        # 打印日志信息，记录创建了对limit_name的并发限制，限制值为concurrency
        log.info("create concurrency limiter for %s: %s", limit_name, concurrency)

        # 创建一个新的信号量，并存入字典，键是limit_name，值是信号量对象
        _semaphores[limit_name] = asyncio.Semaphore(concurrency)

    # 返回信号量字典中limit_name对应的信号量对象
    return _semaphores[limit_name]

