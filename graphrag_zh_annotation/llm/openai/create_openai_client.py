# 导入logging模块，用于记录程序运行时的信息
import logging

# 导入cache装饰器，用于缓存函数的结果，提高效率
from functools import cache

# 从azure.identity模块导入DefaultAzureCredential和get_bearer_token_provider，用于获取Azure身份验证凭证和令牌提供者
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# 从openai模块导入AsyncAzureOpenAI和AsyncOpenAI，这两个类与OpenAI服务的异步操作有关
from openai import AsyncAzureOpenAI, AsyncOpenAI

# 从当前项目的.openai_configuration模块导入OpenAIConfiguration，这是配置OpenAI客户端的类
from .openai_configuration import OpenAIConfiguration

# 从当前项目的.types模块导入OpenAIClientTypes，这是一个枚举类型，定义了OpenAI客户端的不同类型
from .types import OpenAIClientTypes

# 版权声明，2024年微软公司保留所有权利
# 许可证：遵循MIT许可证

# 定义一个名为log的变量，它使用logging.getLogger获取名为'__name__'（即当前模块名）的日志记录器
log = logging.getLogger(__name__)

# 定义一个常量，表示在Azure OpenAI客户端中需要API基础路径
API_BASE_REQUIRED_FOR_AZURE = "api_base is required for Azure OpenAI client"

# 使用cache装饰器的函数，它的具体功能需要看函数内部实现，这里先不详细解释
@cache

# 定义一个函数create_openai_client，它接受两个参数：configuration和azure
def create_openai_client(
    configuration: OpenAIConfiguration, azure: bool
) -> OpenAIClientTypes:
    """创建一个新的OpenAI客户端实例。"""

    # 如果azure参数为真（表示使用Azure服务）
    if azure:
        # 获取API的基础地址，如果没有设置，则抛出错误
        api_base = configuration.api_base
        if api_base is None:
            raise ValueError(API_BASE_REQUIRED_FOR_AZURE)

        # 打印日志信息，展示正在创建Azure OpenAI客户端
        log.info(
            "创建Azure OpenAI客户端，api_base=%s, deployment_name=%s",
            api_base,
            configuration.deployment_name,
        )

        # 如果没有设置认知服务端点，则使用默认值
        if configuration.cognitive_services_endpoint is None:
            cognitive_services_endpoint = "https://cognitiveservices.azure.com/.default"
        else:
            cognitive_services_endpoint = configuration.cognitive_services_endpoint

        # 创建AsyncAzureOpenAI对象并返回
        # 如果有API密钥，使用它；否则，使用Azure AD令牌提供者
        return AsyncAzureOpenAI(
            api_key=configuration.api_key if configuration.api_key else None,
            azure_ad_token_provider=get_bearer_token_provider(
                DefaultAzureCredential(), cognitive_services_endpoint
            )
            if not configuration.api_key
            else None,
            organization=configuration.organization,
            # Azure特定参数
            api_version=configuration.api_version,
            azure_endpoint=api_base,
            azure_deployment=configuration.deployment_name,
            # 超时和重试配置 - 使用Tenacity进行重试，所以在这里禁用
            timeout=configuration.request_timeout or 180.0,
            max_retries=0,
        )

    # 如果azure参数为假（表示不使用Azure服务）
    else:
        # 打印日志信息，展示正在创建OpenAI客户端
        log.info("创建OpenAI客户端，base_url=%s", configuration.api_base)

        # 创建AsyncOpenAI对象并返回
        # 使用配置中的API密钥、基础URL和组织名
        return AsyncOpenAI(
            api_key=configuration.api_key,
            base_url=configuration.api_base,
            organization=configuration.organization,
            # 超时和重试配置 - 使用Tenacity进行重试，所以在这里禁用
            timeout=configuration.request_timeout or 180.0,
            max_retries=0,
        )

