# 导入logging模块，用于记录程序运行时的信息
import logging

# 导入typing模块，它帮助我们更好地定义函数参数和返回值的类型
from typing import Any

# 导入tenacity库的一些组件，它们是处理重试逻辑的工具
from tenacity import (
    AsyncRetrying,  # 异步重试类
    RetryError,  # 重试错误类
    Retrying,  # 同步重试类
    retry_if_exception_type,  # 如果异常类型匹配则重试的装饰器
    stop_after_attempt,  # 在尝试一定次数后停止的策略
    wait_exponential_jitter,  # 指数增长并带有随机抖动的等待时间策略
)

# 从graphrag查询库的llm（语言模型）基础部分导入基类
from graphrag.query.llm.base import BaseLLMCallback

# 从graphrag查询库的OAI（OpenAI）基础部分导入实现类
from graphrag.query.llm.oai.base import OpenAILLMImpl

# 从graphrag查询库的OAI类型部分导入特定的类型定义
from graphrag.query.llm.oai.typing import (
    OPENAI_RETRY_ERROR_TYPES,  # OpenAI重试错误类型的列表
    OpenaiApiType,  # OpenAI API的类型
)

# 这一行是版权信息，表示代码由微软公司2024年创作，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块级别的日志器，用于记录这个文件中产生的日志信息
log = logging.getLogger(__name__)

# 这是一个Python类，叫做OpenAI，它是一个OpenAI完成模型的包装器。
class OpenAI(OpenAILLMImpl):
    """这是一个用来与OpenAI的完成模型交互的工具。"""

    # 类的初始化方法，当创建一个新的OpenAI对象时会调用
    def __init__(self,
                 api_key: str,           # 你的API密钥，用于连接OpenAI服务
                 model: str,             # 要使用的模型名称
                 deployment_name: str | None = None,  # 可选的部署名称
                 api_base: str | None = None,     # 可选的基础API地址
                 api_version: str | None = None,  # 可选的API版本
                 api_type: OpenaiApiType = OpenaiApiType.OpenAI,  # API类型，默认为OpenAI
                 organization: str | None = None,  # 可选的组织名
                 max_retries: int = 10,          # 在请求失败时的最大重试次数
                 retry_error_types: tuple[type[BaseException]] = OPENAI_RETRY_ERROR_TYPES,  # 可重试的错误类型
    ):
        # 将传入的参数存储为对象的属性
        self.api_key = api_key
        self.model = model
        self.deployment_name = deployment_name
        self.api_base = api_base
        self.api_version = api_version
        self.api_type = api_type
        self.organization = organization
        self.max_retries = max_retries
        self.retry_error_types = retry_error_types

    # 生成文本的方法
    def generate(self,
                 messages: str | list[str],   # 要处理的消息，可以是单个字符串或列表
                 streaming: bool = True,       # 是否实时流式处理
                 callbacks: list[BaseLLMCallback] | None = None,  # 可选的回调函数列表
                 **kwargs: Any,                # 其他任意参数
    ) -> str:
        """根据输入的消息生成文本。"""
        # 尝试多次（最多max_retries次）直到成功，如果遇到特定错误则重试
        try:
            # 设置重试策略
            retryer = Retrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),  # 等待时间逐渐增加，最大10秒
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),
            )
            # 遍历重试过程
            for attempt in retryer:
                with attempt:
                    # 实际生成文本的内部方法
                    return self._generate(
                        messages=messages,
                        streaming=streaming,
                        callbacks=callbacks,
                        **kwargs,
                    )
        except RetryError:  # 如果所有重试都失败了
            log.exception("在generate()中遇到了重试错误：%s")
            return ""  # 返回空字符串
        else:
            # TODO: 为什么这里不直接抛出异常？
            return ""  # 如果一切顺利，返回生成的文本

    # 异步生成文本的方法
    async def agenerate(self,
                        messages: str | list[str],
                        streaming: bool = True,
                        callbacks: list[BaseLLMCallback] | None = None,
                        **kwargs: Any,
    ) -> str:
        """异步方式生成文本。"""
        # 类似于同步方法，但使用异步重试策略
        try:
            retryer = AsyncRetrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),
            )
            async for attempt in retryer:
                with attempt:
                    # 异步版本的内部生成方法
                    return await self._agenerate(
                        messages=messages,
                        streaming=streaming,
                        callbacks=callbacks,
                        **kwargs,
                    )
        except RetryError:
            log.exception("在agenerate()中遇到了错误")
            return ""  # 返回空字符串
        else:
            # TODO: 同上，为什么这里不直接抛出异常？
            return ""  # 如果一切顺利，返回生成的文本

    # 同步生成文本的内部方法
    def _generate(self,
                  messages: str | list[str],
                  streaming: bool = True,
                  callbacks: list[BaseLLMCallback] | None = None,
                  **kwargs: Any,
    ) -> str:
        # 使用OpenAI API创建完成请求
        response = self.sync_client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=streaming,
            **kwargs,
        )
        # 如果是流式处理
        if streaming:
            # 拼接所有响应片段
            full_response = ""
            while True:
                try:
                    # 获取下一个响应片段
                    chunk = response.__next__()
                    if not chunk or not chunk.choices:
                        continue

                    # 获取片段中的内容
                    delta = chunk.choices[0].delta.content if chunk.choices[0].delta and chunk.choices[0].delta.content else ""

                    # 添加到完整响应中
                    full_response += delta
                    # 如果有回调函数，调用它们
                    if callbacks:
                        for callback in callbacks:
                            callback.on_llm_new_token(delta)
                    # 如果片段表示已完成
                    if chunk.choices[0].finish_reason == "stop":
                        break
                except StopIteration:
                    break
            # 返回完整响应
            return full_response
        else:
            # 如果不是流式处理，直接返回第一个选择的内容
            return response.choices[0].message.content or ""

    # 异步生成文本的内部方法
    async def _agenerate(self,
                         messages: str | list[str],
                         streaming: bool = True,
                         callbacks: list[BaseLLMCallback] | None = None,
                         **kwargs: Any,
    ) -> str:
        # 异步版本的创建完成请求
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=streaming,
            **kwargs,
        )
        # 流式处理逻辑与同步方法相同
        if streaming:
            full_response = ""
            while True:
                try:
                    chunk = await response.__anext__()
                    if not chunk or not chunk.choices:
                        continue

                    delta = chunk.choices[0].delta.content if chunk.choices[0].delta and chunk.choices[0].delta.content else ""

                    full_response += delta
                    if callbacks:
                        for callback in callbacks:
                            callback.on_llm_new_token(delta)
                    if chunk.choices[0].finish_reason == "stop":
                        break
                except StopIteration:
                    break
            return full_response
        else:
            return response.choices[0].message.content or ""

