# 导入json模块，用于处理数据的序列化和反序列化
import json

# 导入Python的类型注解模块，帮助我们定义和理解代码中的数据类型
from typing import Any, Generic, TypeVar

# 从typing_extensions库导入Unpack，用于元组解包
from typing_extensions import Unpack

# 从graphrag.llm.types模块中导入一些自定义的数据类型
from graphrag.llm.types import LLM, LLMCache, LLMInput, LLMOutput, OnCacheActionFn

# 导入私有函数create_hash_key，用于创建缓存键的哈希值
from ._create_cache_key import create_hash_key

# 版权声明，这个代码由微软公司创作，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个类，用于与缓存进行交互
class CacheManager:
    # 这个版本号用来跟踪缓存策略的变化，如果缓存内容格式改变，应增加此版本号以清空旧缓存
    _cache_strategy_version = 2

    # 定义两个类型变量TIn和TOut，用于表示输入和输出的数据类型
    TIn = TypeVar("TIn")
    TOut = TypeVar("TOut")

    # 定义一个名为_noop_cache_fn的内部函数，它接收一个键和一个可能为None的值，然后不做任何操作
    def _noop_cache_fn(_k: str, _v: str | None):
        pass

# 这是一个名为CachingLLM的类，它用于与缓存交互，并且继承自LLM类
class CachingLLM(LLM[TIn, TOut], Generic[TIn, TOut]):
    # 定义了一些变量，用来存储缓存、代理对象、操作名、LLM参数、缓存命中和未命中的回调函数
    _cache: LLMCache
    _delegate: LLM[TIn, TOut]
    _operation: str
    _llm_paramaters: dict
    _on_cache_hit: OnCacheActionFn
    _on_cache_miss: OnCacheActionFn

    # 初始化方法，设置代理对象、LLM参数、操作名和缓存
    def __init__(
        self,
        delegate: LLM[TIn, TOut],
        llm_parameters: dict,
        operation: str,
        cache: LLMCache,
    ):
        self._delegate = delegate
        self._llm_paramaters = llm_parameters
        self._cache = cache
        self._operation = operation
        # 设置默认的缓存命中和未命中回调函数为无操作函数
        self._on_cache_hit = _noop_cache_fn
        self._on_cache_miss = _noop_cache_fn

    # 设置缓存命中时要调用的函数
    def on_cache_hit(self, fn: OnCacheActionFn | None) -> None:
        self._on_cache_hit = fn or _noop_cache_fn

    # 设置缓存未命中时要调用的函数
    def on_cache_miss(self, fn: OnCacheActionFn | None) -> None:
        self._on_cache_miss = fn or _noop_cache_fn

    # 计算缓存键，基于输入、名称（如果有的话）和参数
    def _cache_key(self, input: TIn, name: str | None, args: dict) -> str:
        json_input = json.dumps(input)
        tag = f"{name}-{self._operation}-v{_cache_strategy_version}" if name is not None else self._operation
        return create_hash_key(tag, json_input, args)

    # 从缓存中读取值
    async def _cache_read(self, key: str) -> Any | None:
        return await self._cache.get(key)

    # 将值写入缓存
    async def _cache_write(
        self, key: str, input: TIn, result: TOut | None, args: dict
    ) -> None:
        if result:  # 如果有结果
            await self._cache.set(  # 写入缓存
                key,
                result,
                {"input": input, "parameters": args},
            )

    # 执行LLM操作
    async def __call__(
        self,
        input: TIn,
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[TOut]:
        # 检查缓存中是否有已存在的项
        name = kwargs.get("name")
        llm_args = {**self._llm_paramaters, **(kwargs.get("model_parameters") or {})}
        cache_key = self._cache_key(input, name, llm_args)
        cached_result = await self._cache_read(cache_key)

        if cached_result:  # 缓存命中
            self._on_cache_hit(cache_key, name)
            return LLMOutput(output=cached_result)

        # 报告缓存未命中
        self._on_cache_miss(cache_key, name)

        # 计算新结果
        result = await self._delegate(input, **kwargs)
        # 将新结果存入缓存
        await self._cache_write(cache_key, input, result.output, llm_args)
        return result

