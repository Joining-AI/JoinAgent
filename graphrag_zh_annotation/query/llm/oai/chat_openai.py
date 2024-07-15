# 导入必要的模块，让代码能处理函数、任意类型和其他工具
from collections.abc import Callable  # 从Python标准库导入Callable，表示可以调用的对象
from typing import Any  # 从Python标准库导入Any，表示任何类型的变量

# 导入用于重试机制的库，以处理网络等问题
from tenacity import (
    AsyncRetrying,  # 异步重试工具
    RetryError,  # 重试时出错的异常类
    Retrying,  # 同步重试工具
    retry_if_exception_type,  # 判断是否因特定异常类型需要重试
    stop_after_attempt,  # 设置最大重试次数后停止
    wait_exponential_jitter,  # 指数增长并带有随机抖动的等待时间
)

# 导入自定义的基类和实现
from graphrag.query.llm.base import BaseLLM, BaseLLMCallback  # 基础语言模型和回调函数的基类
from graphrag.query.llm.oai.base import OpenAILLMImpl  # OpenAI语言模型的实现类
from graphrag.query.llm.oai.typing import (  # OpenAI相关的类型定义
    OPENAI_RETRY_ERROR_TYPES,  # 可以重试的OpenAI错误类型
    OpenaiApiType,  # OpenAI API的类型
)
from graphrag.query.progress import StatusReporter  # 进度报告器，显示任务状态

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个聊天式OpenAI语言模型的实现
# 使用了上述导入的工具和类

# 定义一个常量，表示"模型是必需的"，用于提示错误信息
_MODEL_REQUIRED_MSG = "model is required"

# 定义一个名为ChatOpenAI的类，它继承自BaseLLM和OpenAILLMImpl两个类
class ChatOpenAI(BaseLLM, OpenAILLMImpl):
    # 这个类是为了包装OpenAI的ChatCompletion模型
    """Wrapper for OpenAI ChatCompletion models."""

    # 初始化方法，用于创建ChatOpenAI对象
    def __init__(self,
                 # API密钥，可选
                 api_key: str | None = None,
                 # 指定模型名称，可选
                 model: str | None = None,
                 # Azure AD令牌提供者，可选
                 azure_ad_token_provider: Callable | None = None,
                 # 部署名称，可选
                 deployment_name: str | None = None,
                 # API基础地址，可选
                 api_base: str | None = None,
                 # API版本，可选
                 api_version: str | None = None,
                 # API类型，默认OpenAI
                 api_type: OpenaiApiType = OpenaiApiType.OpenAI,
                 # 组织名称，可选
                 organization: str | None = None,
                 # 最大重试次数，默认10次
                 max_retries: int = 10,
                 # 请求超时时间，默认180秒
                 request_timeout: float = 180.0,
                 # 可重试的错误类型，预设了一些类型
                 retry_error_types: tuple[type[BaseException]] = OPENAI_RETRY_ERROR_TYPES,  # type: ignore
                 # 状态报告器，可选
                 reporter: StatusReporter | None = None,
    ):
        # 调用OpenAILLMImpl的初始化方法
        OpenAILLMImpl.__init__(
            self=self,
            # 传入相同的参数
            api_key=api_key,
            azure_ad_token_provider=azure_ad_token_provider,
            deployment_name=deployment_name,
            api_base=api_base,
            api_version=api_version,
            api_type=api_type,  # type: ignore
            organization=organization,
            max_retries=max_retries,
            request_timeout=request_timeout,
            reporter=reporter,
        )
        # 存储模型名称
        self.model = model
        # 存储可重试的错误类型
        self.retry_error_types = retry_error_types

    # 生成文本的方法
    def generate(
        self,
        # 输入的消息，可以是字符串或列表
        messages: str | list[Any],
        # 是否启用流式处理，默认True
        streaming: bool = True,
        # 回调函数列表，可选
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        """生成文本."""
        # 尝试使用重试机制来执行生成操作
        try:
            # 设置重试策略
            retryer = Retrying(
                # 停止在最大重试次数后
                stop=stop_after_attempt(self.max_retries),
                # 等待时间以指数级增长，最大10秒
                wait=wait_exponential_jitter(max=10),
                # 抛出异常并重试
                reraise=True,
                # 根据错误类型决定是否重试
                retry=retry_if_exception_type(self.retry_error_types),
            )
            # 对每个重试尝试
            for attempt in retryer:
                with attempt:
                    # 执行实际的生成操作
                    return self._generate(
                        messages=messages,
                        streaming=streaming,
                        callbacks=callbacks,
                        **kwargs,
                    )
        # 如果所有尝试都失败，报告错误
        except RetryError as e:
            self._reporter.error(
                message="在生成()时出错", details={self.__class__.__name__: str(e)}
            )
            # 返回空字符串
            return ""
        # 如果没有异常，返回结果
        else:
            # TODO: 为什么这里不直接抛出异常？
            return ""

    # 异步生成文本的方法
    async def agenerate(
        self,
        messages: str | list[Any],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        """异步生成文本."""
        # 类似于同步版本，但使用异步重试机制
        try:
            retryer = AsyncRetrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),  # type: ignore
            )
            # 对每个重试尝试
            async for attempt in retryer:
                with attempt:
                    # 执行实际的异步生成操作
                    return await self._agenerate(
                        messages=messages,
                        streaming=streaming,
                        callbacks=callbacks,
                        **kwargs,
                    )
        # 处理重试失败
        except RetryError as e:
            self._reporter.error(f"在agenerate()时出错：{e}")
            # 返回空字符串
            return ""
        # 如果没有异常，返回结果
        else:
            # TODO: 为什么这里不直接抛出异常？
            return ""

    # 同步生成文本的内部方法
    def _generate(
        self,
        messages: str | list[Any],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        # 检查是否有模型名称
        model = self.model
        if not model:
            raise ValueError("需要指定模型")
        # 使用API客户端创建聊天完成请求
        response = self.sync_client.chat.completions.create(  # type: ignore
            model=model,
            messages=messages,  # type: ignore
            stream=streaming,
            **kwargs,
        )  # type: ignore
        # 如果是流式处理
        if streaming:
            # 初始化完整响应
            full_response = ""
            # 循环获取响应块
            while True:
                try:
                    chunk = response.__next__()  # type: ignore
                    # 如果块无效或无选择，继续
                    if not chunk or not chunk.choices:
                        continue

                    # 获取选择的增量内容
                    delta = (
                        chunk.choices[0].delta.content
                        if chunk.choices[0].delta and chunk.choices[0].delta.content
                        else ""
                    )  # type: ignore

                    # 添加到完整响应
                    full_response += delta
                    # 如果有回调函数，调用它们
                    if callbacks:
                        for callback in callbacks:
                            callback.on_llm_new_token(delta)
                    # 如果选择的结束原因是"stop"，停止循环
                    if chunk.choices[0].finish_reason == "stop":  # type: ignore
                        break
                # 如果遇到StopIteration异常，表示流结束
                except StopIteration:
                    break
            # 返回完整响应
            return full_response
        # 如果不是流式处理，返回第一个选择的消息内容
        return response.choices[0].message.content or ""  # type: ignore

    # 异步生成文本的内部方法
    async def _agenerate(
        self,
        messages: str | list[Any],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        # 检查是否有模型名称
        model = self.model
        if not model:
            raise ValueError("需要指定模型")
        # 使用异步API客户端创建聊天完成请求
        response = await self.async_client.chat.completions.create(  # type: ignore
            model=model,
            messages=messages,  # type: ignore
            stream=streaming,
            **kwargs,
        )
        # 如果是流式处理
        if streaming:
            # 初始化完整响应
            full_response = ""
            # 循环获取响应块
            while True:
                try:
                    chunk = await response.__anext__()  # type: ignore
                    # 如果块无效或无选择，继续
                    if not chunk or not chunk.choices:
                        continue

                    # 获取选择的增量内容
                    delta = (
                        chunk.choices[0].delta.content
                        if chunk.choices[0].delta and chunk.choices[0].delta.content
                        else ""
                    )  # type: ignore

                    # 添加到完整响应
                    full_response += delta
                    # 如果有回调函数，调用它们
                    if callbacks:
                        for callback in callbacks:
                            callback.on_llm_new_token(delta)
                    # 如果选择的结束原因是"stop"，停止循环
                    if chunk.choices[0].finish_reason == "stop":  # type: ignore
                        break
                # 如果遇到StopIteration异常，表示流结束
                except StopIteration:
                    break
            # 返回完整响应
            return full_response

        # 如果不是流式处理，返回第一个选择的消息内容
        return response.choices[0].message.content or ""  # type: ignore

