# 这段代码是用来定义一些基础类的，它们和语言模型（LLM）和嵌入模型有关。
# 它使用了Python的抽象基类（ABC）和抽象方法（abstractmethod）来创建接口，
# 以及一些库来与OpenAI API交互。

# 第一部分：导入需要的模块
# from abc import ABC, abstractmethod
# 这两行导入了Python的抽象基类（ABC）和抽象方法，它们用于创建不能直接实例化的类，作为其他类的模板。

# from collections.abc import Callable
# 这行导入了Callable，这是一个可以调用的对象的抽象基类，比如函数。

# from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, OpenAI
# 这四行导入了OpenAI库的不同版本，用于异步和同步地与OpenAI API进行通信。

# from graphrag.query.llm.base import BaseTextEmbedding
# 这行导入了BaseTextEmbedding，它可能是用于处理文本嵌入的基础类。

# from graphrag.query.llm.oai.typing import OpenaiApiType
# 这行导入了OpenaiApiType，它可能是一个枚举类型，定义了OpenAI API的不同使用方式。

# from graphrag.query.progress import ConsoleStatusReporter, StatusReporter
# 这两行导入了ConsoleStatusReporter和StatusReporter，它们可能是用于报告任务进度的类，ConsoleStatusReporter可能在控制台上显示进度信息。

# # Copyright (c) 2024 Microsoft Corporation.
# # Licensed under the MIT License
# 这两行是版权声明，表示这段代码由微软公司所有，并遵循MIT许可证。

# """Base classes for LLM and Embedding models."""
# 这是一个多行字符串注释，说明这些代码定义的是语言模型和嵌入模型的基础类。

# 以下部分没有实际的代码，只是导入了上面的模块，所以不需要额外的注释。

# 定义一个名为BaseOpenAILLM的类，它继承自一个叫做ABC的抽象基类
class BaseOpenAILLM(ABC):
    """这是一个基础的OpenAI语言模型实现类。"""

    # 这两个变量是类的成员，用来存储异步和同步的客户端对象
    _async_client: AsyncOpenAI | AsyncAzureOpenAI  # 异步客户端
    _sync_client: OpenAI | AzureOpenAI  # 同步客户端

    # 类的初始化方法，当创建一个BaseOpenAILLM的对象时会执行这个方法
    def __init__(self):
        # 调用一个特殊的方法来创建客户端
        self._create_openai_client()

    # 一个需要子类去实现的抽象方法，用于创建同步和异步的OpenAI客户端实例
    @abstractmethod
    def _create_openai_client(self):
        """创建新的同步和异步OpenAI客户端实例。"""

    # 一个方法，用来设置用于API请求的同步和异步客户端
    def set_clients(
        self,
        sync_client: OpenAI | AzureOpenAI,  # 同步客户端对象
        async_client: AsyncOpenAI | AsyncAzureOpenAI,  # 异步客户端对象
    ):
        """
        设置用于API请求的同步和异步客户端。

        参数:
            sync_client (OpenAI | AzureOpenAI): 同步客户端对象。
            async_client (AsyncOpenAI | AsyncAzureOpenAI): 异步客户端对象。
        """
        self._sync_client = sync_client
        self._async_client = async_client

    # 获取异步客户端的方法，返回异步客户端对象
    @property
    def async_client(self) -> AsyncOpenAI | AsyncAzureOpenAI | None:
        """
        获取用于API请求的异步客户端。

        返回值:
            AsyncOpenAI | AsyncAzureOpenAI: 异步客户端对象。
        """
        return self._async_client

    # 获取同步客户端的方法，返回同步客户端对象
    @property
    def sync_client(self) -> OpenAI | AzureOpenAI | None:
        """
        获取用于API请求的同步客户端。

        返回值:
            AsyncOpenAI | AsyncAzureOpenAI: 同步客户端对象。
        """
        return self._sync_client

    # 设置异步客户端的方法，接收一个异步客户端对象作为参数
    @async_client.setter
    def async_client(self, client: AsyncOpenAI | AsyncAzureOpenAI):
        """
        设置用于API请求的异步客户端。

        参数:
            client (AsyncOpenAI | AsyncAzureOpenAI): 异步客户端对象。
        """
        self._async_client = client

    # 设置同步客户端的方法，接收一个同步客户端对象作为参数
    @sync_client.setter
    def sync_client(self, client: OpenAI | AzureOpenAI):
        """
        设置用于API请求的同步客户端。

        参数:
            client (OpenAI | AzureOpenAI): 同步客户端对象。
        """
        self._sync_client = client



# 定义一个名为OpenAILLMImpl的类，它是BaseOpenAILLM类的子类
class OpenAILLMImpl(BaseOpenAILLM):
    """这个类用来管理OpenAI的大型语言模型服务"""

    # 创建一个变量_reporter，它是一个StatusReporter类型，这里默认是ConsoleStatusReporter
    _reporter: StatusReporter = ConsoleStatusReporter()

    # 定义一个构造函数（__init__方法），当创建新对象时会执行
    def __init__(
        self,
        # 接受一些参数，比如API密钥、Azure AD令牌提供者等
        api_key: str | None = None,
        azure_ad_token_provider: Callable | None = None,
        deployment_name: str | None = None,
        api_base: str | None = None,
        api_version: str | None = None,
        api_type: OpenaiApiType = OpenaiApiType.OpenAI,
        organization: str | None = None,
        max_retries: int = 10,
        request_timeout: float = 180.0,
        reporter: StatusReporter | None = None,
    ):
        # 将传入的参数赋值给对应的类属性
        self.api_key = api_key
        self.azure_ad_token_provider = azure_ad_token_provider
        self.deployment_name = deployment_name
        self.api_base = api_base
        self.api_version = api_version
        self.api_type = api_type
        self.organization = organization
        self.max_retries = max_retries
        self.request_timeout = request_timeout
        # 如果没有提供reporter，就用默认的ConsoleStatusReporter
        self.reporter = reporter or ConsoleStatusReporter()

        # 尝试调用父类（BaseOpenAILLM）的构造函数初始化
        try:
            super().__init__()
        # 如果出现异常，报告错误并再次抛出异常
        except Exception as e:
            self._reporter.error(
                message="创建OpenAI客户端失败",
                details={self.__class__.__name__: str(e)},
            )
            raise

    # 创建一个新的OpenAI客户端的方法
    def _create_openai_client(self):
        """创建一个OpenAI客户端实例"""
        # 根据api_type判断是AzureOpenAI还是OpenAI
        if self.api_type == OpenaiApiType.AzureOpenAI:
            # 如果是AzureOpenAI，检查api_base是否已提供
            if self.api_base is None:
                # 如果没提供，抛出错误
                msg = "需要提供api_base以使用Azure OpenAI"
                raise ValueError(msg)

            # 创建同步和异步的AzureOpenAI客户端
            sync_client = AzureOpenAI(
                api_key=self.api_key,
                azure_ad_token_provider=self.azure_ad_token_provider,
                organization=self.organization,
                api_version=self.api_version,
                azure_endpoint=self.api_base,
                azure_deployment=self.deployment_name,
                timeout=self.request_timeout,
                max_retries=self.max_retries,
            )

            async_client = AsyncAzureOpenAI(
                api_key=self.api_key,
                azure_ad_token_provider=self.azure_ad_token_provider,
                organization=self.organization,
                api_version=self.api_version,
                azure_endpoint=self.api_base,
                azure_deployment=self.deployment_name,
                timeout=self.request_timeout,
                max_retries=self.max_retries,
            )
            # 设置同步和异步客户端
            self.set_clients(sync_client=sync_client, async_client=async_client)

        else:
            # 如果是OpenAI，创建同步和异步的OpenAI客户端
            sync_client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base,
                organization=self.organization,
                timeout=self.request_timeout,
                max_retries=self.max_retries,
            )

            async_client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.api_base,
                organization=self.organization,
                timeout=self.request_timeout,
                max_retries=self.max_retries,
            )
            # 设置同步和异步客户端
            self.set_clients(sync_client=sync_client, async_client=async_client)

# 定义一个叫做OpenAITextEmbeddingImpl的类，它是BaseTextEmbedding类的子类
class OpenAITextEmbeddingImpl(BaseTextEmbedding):
    """这是一个用来协调OpenAI文本嵌入实现的类。"""

    # 这个变量存储了一个StatusReporter类型的对象或者None，暂时不用
    _reporter: StatusReporter | None = None

    # 定义一个名为_create_openai_client的方法
    def _create_openai_client(self, api_type: OpenaiApiType):
        """这个方法会创建一个新的同步或异步的OpenAI客户端实例。"""

