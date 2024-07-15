# 这是一段Python代码，它导入了多个库和模块，用于创建OpenAI语言模型（LLMs）的工厂函数。

# 导入异步操作的库
import asyncio

# 从graphrag的llm基础包中导入CachingLLM和RateLimitingLLM
from graphrag.llm.base import CachingLLM, RateLimitingLLM

# 从graphrag的llm限制包中导入LLMLimiter
from graphrag.llm.limiting import LLMLimiter

# 从graphrag.llm.types中导入各种类型定义
from graphrag.llm.types import (
    LLM,  # 基础语言模型类
    CompletionLLM,  # 完成句子的语言模型
    EmbeddingLLM,  # 生成词嵌入的语言模型
    ErrorHandlerFn,  # 错误处理函数类型
    LLMCache,  # 语言模型缓存
    LLMInvocationFn,  # 调用语言模型的函数类型
    OnCacheActionFn,  # 缓存操作回调函数类型
)

# 导入自定义的JSON解析语言模型
from .json_parsing_llm import JsonParsingLLM

# 导入OpenAI聊天语言模型
from .openai_chat_llm import OpenAIChatLLM

# 导入OpenAI完成句子的语言模型
from .openai_completion_llm import OpenAICompletionLLM

# 导入OpenAI配置类
from .openai_configuration import OpenAIConfiguration

# 导入OpenAI词嵌入语言模型
from .openai_embeddings_llm import OpenAIEmbeddingsLLM

# 导入OpenAI历史追踪语言模型
from .openai_history_tracking_llm import OpenAIHistoryTrackingLLM

# 导入OpenAI替换令牌的语言模型
from .openai_token_replacing_llm import OpenAITokenReplacingLLM

# 导入OpenAI客户端类型
from .types import OpenAIClientTypes

# 导入工具函数
from .utils import (
    RATE_LIMIT_ERRORS,  # 与速率限制相关的错误列表
    RETRYABLE_ERRORS,  # 可重试的错误列表
    get_completion_cache_args,  # 获取完成句子缓存参数的函数
    get_sleep_time_from_error,  # 根据错误获取等待时间的函数
    get_token_counter,  # 获取令牌计数器的函数
)

# 以下代码未显示，但通常会包含实际创建和使用这些语言模型的函数。

# 定义一个函数，用于创建与OpenAI聊天功能相关的逻辑
def create_openai_chat_llm(
    # 接收一个OpenAI客户端对象
    client: OpenAIClientTypes,
    # 接收一个OpenAI配置对象
    config: OpenAIConfiguration,
    # 可选的缓存对象，用于存储之前请求的结果
    cache: LLMCache | None = None,
    # 可选的限流器，限制请求频率
    limiter: LLMLimiter | None = None,
    # 可选的信号量，用于同步并发请求
    semaphore: asyncio.Semaphore | None = None,
    # 当调用LLM时执行的函数，可选
    on_invoke: LLMInvocationFn | None = None,
    # 处理错误的函数，可选
    on_error: ErrorHandlerFn | None = None,
    # 缓存命中时执行的函数，可选
    on_cache_hit: OnCacheActionFn | None = None,
    # 缓存未命中时执行的函数，可选
    on_cache_miss: OnCacheActionFn | None = None,
) -> CompletionLLM:
    """创建一个OpenAI聊天逻辑管理器"""
    
    # 设置操作类型为"chat"
    operation = "chat"
    
    # 创建OpenAI聊天逻辑管理器实例
    result = OpenAIChatLLM(client, config)
    
    # 设置错误处理函数
    result.on_error(on_error)
    
    # 如果有设置限流器或信号量，则应用限流逻辑
    if limiter is not None or semaphore is not None:
        result = _rate_limited(result, config, operation, limiter, semaphore, on_invoke)
    
    # 如果有设置缓存，则应用缓存逻辑
    if cache is not None:
        result = _cached(result, config, operation, cache, on_cache_hit, on_cache_miss)
    
    # 添加历史追踪功能
    result = OpenAIHistoryTrackingLLM(result)
    
    # 添加令牌替换功能
    result = OpenAITokenReplacingLLM(result)
    
    # 返回处理后的逻辑管理器
    return JsonParsingLLM(result)

# 定义一个与OpenAI完成（如生成文本）功能相关的函数
def create_openai_completion_llm(
    # 同上，接收OpenAI客户端对象
    client: OpenAIClientTypes,
    # 同上，接收OpenAI配置对象
    config: OpenAIConfiguration,
    # 同上，可选的缓存对象
    cache: LLMCache | None = None,
    # 同上，可选的限流器
    limiter: LLMLimiter | None = None,
    # 同上，可选的信号量
    semaphore: asyncio.Semaphore | None = None,
    # 同上，可选的调用时执行函数
    on_invoke: LLMInvocationFn | None = None,
    # 同上，可选的错误处理函数
    on_error: ErrorHandlerFn | None = None,
    # 同上，可选的缓存命中时执行函数
    on_cache_hit: OnCacheActionFn | None = None,
    # 同上，可选的缓存未命中时执行函数
    on_cache_miss: OnCacheActionFn | None = None,
) -> CompletionLLM:
    """创建一个OpenAI完成逻辑管理器"""
    
    # 设置操作类型为"completion"
    operation = "completion"
    
    # 创建OpenAI完成逻辑管理器实例
    result = OpenAICompletionLLM(client, config)
    
    # 设置错误处理函数
    result.on_error(on_error)
    
    # 如果有设置限流器或信号量，则应用限流逻辑
    if limiter is not None or semaphore is not None:
        result = _rate_limited(result, config, operation, limiter, semaphore, on_invoke)
    
    # 如果有设置缓存，则应用缓存逻辑
    if cache is not None:
        result = _cached(result, config, operation, cache, on_cache_hit, on_cache_miss)
    
    # 直接返回添加令牌替换功能的逻辑管理器
    return OpenAITokenReplacingLLM(result)

# 定义一个函数create_openai_embedding_llm，用于创建OpenAI的嵌入式语言模型
def create_openai_embedding_llm(
    # 参数：OpenAI的客户端对象
    client: OpenAIClientTypes,
    # 参数：OpenAI的配置信息
    config: OpenAIConfiguration,
    # 可选参数，缓存对象，用于存储之前的结果
    cache: LLMCache | None = None,
    # 可选参数，限流器，限制请求频率
    limiter: LLMLimiter | None = None,
    # 可选参数，信号量，用于控制并发访问
    semaphore: asyncio.Semaphore | None = None,
    # 可选参数，当调用模型时执行的函数
    on_invoke: LLMInvocationFn | None = None,
    # 可选参数，处理错误的函数
    on_error: ErrorHandlerFn | None = None,
    # 可选参数，缓存命中时执行的函数
    on_cache_hit: OnCacheActionFn | None = None,
    # 可选参数，缓存未命中时执行的函数
    on_cache_miss: OnCacheActionFn | None = None,
) -> EmbeddingLLM:
    """创建一个OpenAI的嵌入式语言模型对象"""
    # 设置操作类型为"embedding"
    operation = "embedding"
    # 初始化OpenAIEmbeddingsLLM对象
    result = OpenAIEmbeddingsLLM(client, config)
    # 设置错误处理函数
    result.on_error(on_error)
    # 如果有限流器或信号量，应用限流
    if limiter is not None or semaphore is not None:
        result = _rate_limited(result, config, operation, limiter, semaphore, on_invoke)
    # 如果有缓存，添加缓存功能
    if cache is not None:
        result = _cached(result, config, operation, cache, on_cache_hit, on_cache_miss)
    # 返回最终处理后的对象
    return result

# 内部辅助函数_rate_limited，用于添加限流功能
def _rate_limited(
    # 参数：原始的LLM对象
    delegate: LLM,
    # 参数：OpenAI的配置信息
    config: OpenAIConfiguration,
    # 参数：操作类型
    operation: str,
    # 可选参数，限流器
    limiter: LLMLimiter | None,
    # 可选参数，信号量
    semaphore: asyncio.Semaphore | None,
    # 可选参数，调用模型时执行的函数
    on_invoke: LLMInvocationFn | None,
):
    # 初始化RateLimitingLLM对象，用于限流
    result = RateLimitingLLM(
        delegate,
        config,
        operation,
        RETRYABLE_ERRORS,  # 可重试的错误列表
        RATE_LIMIT_ERRORS,  # 限流错误列表
        limiter,
        semaphore,
        get_token_counter(config),  # 获取令牌计数器
        get_sleep_time_from_error,  # 根据错误获取睡眠时间
    )
    # 设置调用模型时执行的函数
    result.on_invoke(on_invoke)
    # 返回限流处理后的对象
    return result

# 内部辅助函数_cached，用于添加缓存功能
def _cached(
    # 参数：原始的LLM对象
    delegate: LLM,
    # 参数：OpenAI的配置信息
    config: OpenAIConfiguration,
    # 参数：操作类型
    operation: str,
    # 参数：缓存对象
    cache: LLMCache,
    # 可选参数，缓存命中时执行的函数
    on_cache_hit: OnCacheActionFn | None,
    # 可选参数，缓存未命中时执行的函数
    on_cache_miss: OnCacheActionFn | None,
):
    # 获取缓存相关的参数
    cache_args = get_completion_cache_args(config)
    # 初始化CachingLLM对象，用于缓存
    result = CachingLLM(delegate, cache_args, operation, cache)
    # 设置缓存命中和未命中时执行的函数
    result.on_cache_hit(on_cache_hit)
    result.on_cache_miss(on_cache_miss)
    # 返回带有缓存功能的对象
    return result

