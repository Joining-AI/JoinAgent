# 导入异步编程库，用于处理等待和并发任务
import asyncio

# 导入Callable接口，定义可调用对象的类型
from collections.abc import Callable

# 导入Any类型，表示任何类型的变量
from typing import Any

# 导入库，用于科学计算和数组操作
import numpy as np

# 导入库，用于处理OpenAI的认证令牌
import tiktoken

# 导入tenacity库，用于重试失败的操作
from tenacity import (
    AsyncRetrying,  # 异步重试
    RetryError,  # 重试时发生的错误
    Retrying,  # 重试策略类
    retry_if_exception_type,  # 如果异常类型匹配则重试
    stop_after_attempt,  # 在尝试次数达到指定值后停止
    wait_exponential_jitter,  # 指数增长的等待时间，带随机抖动
)

# 从graphrag库导入文本嵌入基类
from graphrag.query.llm.base import BaseTextEmbedding

# 从graphrag库导入OpenAI接口实现基类
from graphrag.query.llm.oai.base import OpenAILLMImpl

# 从graphrag库导入OpenAI相关的类型定义
from graphrag.query.llm.oai.typing import (
    OPENAI_RETRY_ERROR_TYPES,  # OpenAI接口可能出现的错误类型
    OpenaiApiType,  # OpenAI API的类型
)

# 从graphrag库导入文本处理工具
from graphrag.query.llm.text_utils import chunk_text

# 从graphrag库导入进度报告器
from graphrag.query.progress import StatusReporter

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是OpenAI嵌入模型实现的模块

# 定义一个名为OpenAIEmbedding的类，它同时继承了BaseTextEmbedding和OpenAILLMImpl两个类
class OpenAIEmbedding(BaseTextEmbedding, OpenAILLMImpl):
    # 这个类是用于包装OpenAI的嵌入模型的
    """Wrapper for OpenAI Embedding models."""

    # 初始化方法，用于创建类的实例时设置参数
    def __init__(self,
                 # API密钥，可以是字符串或None
                 api_key: str | None = None,
                 # Azure AD令牌提供者，可以是函数或None
                 azure_ad_token_provider: Callable | None = None,
                 # 模型名称，默认为"text-embedding-3-small"
                 model: str = "text-embedding-3-small",
                 # 部署名称，可以是字符串或None
                 deployment_name: str | None = None,
                 # API的基础URL，可以是字符串或None
                 api_base: str | None = None,
                 # API版本，可以是字符串或None
                 api_version: str | None = None,
                 # API类型，默认为OpenAI
                 api_type: OpenaiApiType = OpenaiApiType.OpenAI,
                 # 组织名称，可以是字符串或None
                 organization: str | None = None,
                 # 编码名称，默认为"cl100k_base"
                 encoding_name: str = "cl100k_base",
                 # 最大处理的令牌数，默认为8191
                 max_tokens: int = 8191,
                 # 最大重试次数，默认为10
                 max_retries: int = 10,
                 # 请求超时时间，默认为180秒
                 request_timeout: float = 180.0,
                 # 错误报告器，可以是StatusReporter类的实例或None
                 reporter: StatusReporter | None = None,
    ):
        # 调用OpenAILLMImpl的初始化方法
        OpenAILLMImpl.__init__(
            self=self,
            api_key=api_key,
            azure_ad_token_provider=azure_ad_token_provider,
            deployment_name=deployment_name,
            api_base=api_base,
            api_version=api_version,
            api_type=api_type,  # 忽略类型提示
            organization=organization,
            max_retries=max_retries,
            request_timeout=request_timeout,
            reporter=reporter,
        )

        # 设置模型、编码名称和其他属性
        self.model = model
        self.encoding_name = encoding_name
        self.max_tokens = max_tokens
        # 获取编码器
        self.token_encoder = tiktoken.get_encoding(self.encoding_name)
        # 设置可重试的错误类型
        self.retry_error_types = retry_error_types

    # 同步嵌入方法，将文本转换为向量列表
    def embed(self, text: str, **kwargs: Any) -> list[float]:
        """
        使用OpenAI Embedding的同步函数将文本嵌入。
        
        对于超过max_tokens长度的文本，会将其分割成多个部分，分别嵌入，然后用加权平均合并。
        查看更多：https://github.com/openai/openai-cookbook/blob/main/examples/Embedding_long_inputs.ipynb
        """
        # 分割文本
        token_chunks = chunk_text(
            text=text, token_encoder=self.token_encoder, max_tokens=self.max_tokens
        )
        # 存储各部分的嵌入向量和长度
        chunk_embeddings = []
        chunk_lens = []
        # 对每个文本块进行嵌入
        for chunk in token_chunks:
            try:
                # 重试并嵌入文本块
                embedding, chunk_len = self._embed_with_retry(chunk, **kwargs)
                chunk_embeddings.append(embedding)
                chunk_lens.append(chunk_len)
            # 捕获所有异常
            except Exception as e:  # noqa BLE001
                # 报告错误
                self._reporter.error(
                    message="嵌入文本块时出错",
                    details={self.__class__.__name__: str(e)},
                )
                # 继续处理下一个文本块
                continue
        # 计算平均嵌入向量
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        # 归一化平均嵌入向量
        chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings)
        # 返回向量列表
        return chunk_embeddings.tolist()

    # 异步嵌入方法，与同步方法类似，但使用异步函数
    async def aembed(self, text: str, **kwargs: Any) -> list[float]:
        """
        使用OpenAI Embedding的异步函数将文本嵌入。
        
        对于超过max_tokens长度的文本，会将其分割成多个部分，分别嵌入，然后用加权平均合并。
        """
        # 分割文本
        token_chunks = chunk_text(
            text=text, token_encoder=self.token_encoder, max_tokens=self.max_tokens
        )
        # 异步获取各部分的嵌入向量和长度
        embedding_results = await asyncio.gather(*[
            self._aembed_with_retry(chunk, **kwargs) for chunk in token_chunks
        ])
        # 过滤掉失败的结果
        embedding_results = [result for result in embedding_results if result[0]]
        chunk_embeddings = [result[0] for result in embedding_results]
        chunk_lens = [result[1] for result in embedding_results]
        # 计算平均嵌入向量
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)  # type: ignore
        # 归一化平均嵌入向量
        chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings)
        # 返回向量列表
        return chunk_embeddings.tolist()

    # 同步重试嵌入方法，用于处理单个文本块
    def _embed_with_retry(
        self, text: str | tuple, **kwargs: Any
    ) -> tuple[list[float], int]:
        try:
            # 创建重试器，设置最大重试次数和等待策略
            retryer = Retrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),
            )
            # 重试直到成功或达到最大重试次数
            for attempt in retryer:
                with attempt:
                    # 调用API嵌入文本
                    embedding = (
                        self.sync_client.embeddings.create(  # type: ignore
                            input=text,
                            model=self.model,
                            **kwargs,  # type: ignore
                        )
                        .data[0]
                        .embedding
                        or []
                    )
                    # 返回嵌入向量和文本长度
                    return (embedding, len(text))
        # 如果所有尝试都失败，报告错误
        except RetryError as e:
            self._reporter.error(
                message="在embed_with_retry()中出错",
                details={self.__class__.__name__: str(e)},
            )
            # 返回空向量和长度0
            return ([], 0)
        else:
            # 这里不应该到达，返回空向量和长度0
            return ([], 0)

    # 异步重试嵌入方法，与同步方法类似，但使用异步函数
    async def _aembed_with_retry(
        self, text: str | tuple, **kwargs: Any
    ) -> tuple[list[float], int]:
        try:
            # 创建异步重试器
            retryer = AsyncRetrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),
            )
            # 异步重试直到成功或达到最大重试次数
            async for attempt in retryer:
                with attempt:
                    # 调用API异步嵌入文本
                    embedding = (
                        await self.async_client.embeddings.create(  # type: ignore
                            input=text,
                            model=self.model,
                            **kwargs,  # type: ignore
                        )
                    ).data[0].embedding or []
                    # 返回嵌入向量和文本长度
                    return (embedding, len(text))
        # 如果所有尝试都失败，报告错误
        except RetryError as e:
            self._reporter.error(
                message="在embed_with_retry()中出错",
                details={self.__class__.__name__: str(e)},
            )
            # 返回空向量和长度0
            return ([], 0)
        else:
            # 这里不应该到达，返回空向量和长度0
            return ([], 0)

