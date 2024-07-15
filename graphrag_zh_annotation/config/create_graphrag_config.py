# 导入操作系统的模块，可以获取和操作文件路径等信息
import os

# 导入枚举类的扩展库，用于定义一些固定的选项
from enum import Enum

# 导入Pathlib模块，提供更方便的文件路径操作
from pathlib import Path

# 从typing库导入cast函数，用于类型转换
from typing import cast

# 导入异步数据类型的库
from datashaper import AsyncType

# 导入Env模块，用于从环境变量读取配置
from environs import Env

# 从pydantic库导入TypeAdapter，帮助处理数据模型
from pydantic import TypeAdapter

# 导入默认配置的模块
import graphrag.config.defaults as defs

# 导入自定义的枚举类型
from .enums import (
    CacheType,  # 缓存类型
    InputFileType,  # 输入文件类型
    InputType,  # 输入类型
    LLMType,  # 语言模型类型
    ReportingType,  # 报告类型
    StorageType,  # 存储类型
    TextEmbeddingTarget,  # 文本嵌入目标
)

# 导入环境读取器类
from .environment_reader import EnvironmentReader

# 导入错误类
from .errors import (
    ApiKeyMissingError,  # API密钥缺失错误
    AzureApiBaseMissingError,  # Azure API基础地址缺失错误
    AzureDeploymentNameMissingError,  # Azure部署名称缺失错误
)

# 导入输入模型类
from .input_models import (
    GraphRagConfigInput,  # GraphRag配置输入
    LLMConfigInput,  # 语言模型配置输入
)

# 导入模型类
from .models import (
    CacheConfig,  # 缓存配置
    ChunkingConfig,  # 块化配置
    ClaimExtractionConfig,  # 声明提取配置
    ClusterGraphConfig,  # 聚类图配置
    CommunityReportsConfig,  # 社区报告配置
    EmbedGraphConfig,  # 嵌入图配置
    EntityExtractionConfig,  # 实体提取配置
    GlobalSearchConfig,  # 全局搜索配置
    GraphRagConfig,  # GraphRag配置
    InputConfig,  # 输入配置
    LLMParameters,  # 语言模型参数
    LocalSearchConfig,  # 本地搜索配置
    ParallelizationParameters,  # 并行化参数
    ReportingConfig,  # 报告配置
    SnapshotsConfig,  # 快照配置
    StorageConfig,  # 存储配置
    SummarizeDescriptionsConfig,  # 摘要描述配置
    TextEmbeddingConfig,  # 文本嵌入配置
    UmapConfig,  # UMAP配置
)

# 导入读取.env文件的函数
from .read_dotenv import read_dotenv

# 这是代码的版权信息，表明这段代码属于微软公司，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块的作用，用于设置默认配置的参数，从环境变量加载
"""Parameterization settings for the default configuration, loaded from environment variables."""

# 导入操作系统相关的模块，用于与操作系统交互
import os

# 导入Enum类，用于创建枚举类型
from enum import Enum

# 导入Path类，用于处理文件路径
from pathlib import Path

# 导入typing模块中的cast函数，用于类型转换
from typing import cast

# 导入datashaper库中的AsyncType，可能用于异步操作
from datashaper import AsyncType

# 导入environs库，用于从环境变量读取配置
from environs import Env

# 导入pydantic库中的TypeAdapter，用于自定义数据类型的适配器
from pydantic import TypeAdapter

# 导入默认配置模块
import graphrag.config.defaults as defs

# 导入自定义的枚举类型
from .enums import (
    CacheType,
    InputFileType,
    InputType,
    LLMType,
    ReportingType,
    StorageType,
    TextEmbeddingTarget,
)

# 导入环境读取器类
from .environment_reader import EnvironmentReader

# 导入错误类
from .errors import (
    ApiKeyMissingError,
    AzureApiBaseMissingError,
    AzureDeploymentNameMissingError,
)

# 导入输入模型类
from .input_models import (
    GraphRagConfigInput,
    LLMConfigInput,
)

# 导入各种配置模型类
from .models import (
    CacheConfig,
    ChunkingConfig,
    ClaimExtractionConfig,
    ClusterGraphConfig,
    CommunityReportsConfig,
    EmbedGraphConfig,
    EntityExtractionConfig,
    GlobalSearchConfig,
    GraphRagConfig,
    InputConfig,
    LLMParameters,
    LocalSearchConfig,
    ParallelizationParameters,
    ReportingConfig,
    SnapshotsConfig,
    StorageConfig,
    SummarizeDescriptionsConfig,
    TextEmbeddingConfig,
    UmapConfig,
)

# 导入读取.env文件的函数
from .read_dotenv import read_dotenv

# 定义一个类型适配器，专门用于验证GraphRagConfigInput类型的输入
InputModelValidator = TypeAdapter(GraphRagConfigInput)

# 定义一个函数create_graphrag_config，接收两个参数：values和root_dir，它们可以是None
def create_graphrag_config(
    values: GraphRagConfigInput | None = None,  # values可以是GraphRagConfigInput类型的字典或None
    root_dir: str | None = None  # root_dir可以是字符串或None
) -> GraphRagConfig:  # 函数返回值类型为GraphRagConfig

    # 如果values没有传入，就设为空字典
    values = values or {}

    # 如果root_dir没有传入，就设为当前工作目录的字符串表示
    root_dir = root_dir or str(Path.cwd())

    # 创建环境对象env
    env = _make_env(root_dir)

    # 对values中的字典进行处理
    _token_replace(cast(dict, values))

    # 验证values中Python部分的数据
    InputModelValidator.validate_python(values, strict=True)

    # 创建环境读取器
    reader = EnvironmentReader(env)

    # 定义一个函数hydrated_async_type，将LLMConfigInput类型的input与AsyncType类型的base结合
    def hydrate_async_type(input: LLMConfigInput, base: AsyncType) -> AsyncType:
        # 获取input中的async_mode值
        value = input.get(Fragment.async_mode)
        # 如果value存在，返回AsyncType(value)，否则返回base
        return AsyncType(value) if value else base

    # 定义一个函数hydrated_llm_params，将LLMConfigInput类型的config与LLMParameters类型的base结合
    def hydrate_llm_params(
        config: LLMConfigInput, base: LLMParameters
    ) -> LLMParameters:
        # 使用config中的llm信息更新reader
        with reader.use(config.get("llm")):
            # 获取并处理llm_type、api_key、api_base等参数
            # ...（这部分代码较多，省略了详细注释，主要是从reader中获取或设置配置参数）

            # 返回处理后的LLMParameters对象

    # 定义一个函数hydrated_embeddings_params，与hydrated_llm_params类似，但用于处理embeddings参数
    def hydrate_embeddings_params(
        config: LLMConfigInput, base: LLMParameters
    ) -> LLMParameters:
        # 使用config中的llm信息更新reader
        with reader.use(config.get("llm")):
            # 获取并处理api_type、api_key等参数
            # ...（这部分代码较多，省略了详细注释，主要是从reader中获取或设置配置参数）

            # 返回处理后的LLMParameters对象

    # 定义一个函数hydrated_parallelization_params，用于处理并行化参数
    def hydrate_parallelization_params(
        config: LLMConfigInput, base: ParallelizationParameters
    ) -> ParallelizationParameters:
        # 使用config中的parallelization信息更新reader
        with reader.use(config.get("parallelization")):
            # 获取并处理num_threads和stagger参数
            # ...（这部分代码较少，直接返回处理后的ParallelizationParameters对象）

    # 获取默认的OpenAI API Key等环境变量
    fallback_oai_key = env("OPENAI_API_KEY", env("AZURE_OPENAI_API_KEY", None))
    fallback_oai_org = env("OPENAI_ORG_ID", None)
    fallback_oai_base = env("OPENAI_BASE_URL", None)
    fallback_oai_version = env("OPENAI_API_VERSION", None)

    # 使用values和envvar_prefix(Section.graphrag)更新reader
    with reader.envvar_prefix(Section.graphrag), reader.use(values):
        # 获取并处理async_mode、api_key等参数
        # ...（这部分代码较多，省略了详细注释，主要是从reader中获取或设置配置参数）

        # 创建并返回GraphRagConfig对象，包含各种配置参数

# 定义一个名为Fragment的类，它同时继承自str（字符串）和Enum（枚举类型）
class Fragment(str, Enum):
    # 这个类是用来表示配置片段的
    """Configuration Fragments."""

    # 下面这一系列的变量都是Fragment类的成员，它们是字符串类型的枚举值
    # 每个变量名代表一个配置项的名称，比如：
    api_base = "API_BASE"  # API的基础地址
    api_key = "API_KEY"  # API的密钥
    api_version = "API_VERSION"  # API的版本号
    api_organization = "API_ORGANIZATION"  # API组织
    api_proxy = "API_PROXY"  # API代理
    async_mode = "ASYNC_MODE"  # 异步模式
    base_dir = "BASE_DIR"  # 基础目录
    # ...（其他配置项，以此类推）

# 现在定义另一个名为Section的类，同样继承自str和Enum
class Section(str, Enum):
    # 这个类是用来表示配置段的
    """Configuration Sections."""

    # 同样，下面的变量是Section类的成员，它们也是字符串类型的枚举值
    # 每个变量名代表一个配置段的名称，例如：
    base = "BASE"  # 基础设置
    cache = "CACHE"  # 缓存设置
    chunk = "CHUNK"  # 块设置
    claim_extraction = "CLAIM_EXTRACTION"  # 声明提取设置
    community_reports = "COMMUNITY_REPORTS"  # 社区报告设置
    embedding = "EMBEDDING"  # 嵌入设置
    entity_extraction = "ENTITY_EXTRACTION"  # 实体提取设置
    graphrag = "GRAPHRAG"  # 图形碎片设置
    input = "INPUT"  # 输入设置
    llm = "LLM"  # 大语言模型设置
    node2vec = "NODE2VEC"  # Node2Vec设置
    reporting = "REPORTING"  # 报告设置
    snapshot = "SNAPSHOT"  # 快照设置
    storage = "STORAGE"  # 存储设置
    summarize_descriptions = "SUMMARIZE_DESCRIPTIONS"  # 描述总结设置
    umap = "UMAP"  # UMAP设置
    local_search = "LOCAL_SEARCH"  # 本地搜索设置
    global_search = "GLOBAL_SEARCH"  # 全局搜索设置

# 定义一个函数，检查输入的类型是否与Azure有关
def _is_azure(llm_type):  # llm_type可以是LLMType类型或者None
    # 如果llm_type等于以下三种Azure类型之一，返回True
    if llm_type == LLMType.AzureOpenAI 或者  # LLMType是一个枚举类型
       llm_type == LLMType.AzureOpenAIChat 或者  # 检查是否为聊天类型
       llm_type == LLMType.AzureOpenAIEmbedding:  # 检查是否为嵌入类型
        return True  # 是Azure相关，返回True
    else:
        return False  # 不是Azure相关，返回False

# 定义一个函数，用来创建环境对象
def _make_env(root_dir):  # root_dir是一个字符串，表示根目录
    # 从root_dir指定的目录读取.env文件，用来设置环境变量
    read_dotenv(root_dir)
    # 创建一个Env对象，expand_vars参数为True，意味着会扩展环境变量
    env = Env(expand_vars=True)
    # 从当前环境加载更多环境变量
    env.read_env()
    # 返回创建好的环境对象
    return env

# 定义一个函数，用于替换字典中环境变量占位符
def _token_replace(data):  # data是一个字典
    # 遍历字典中的每一项（键值对）
    for key, value in data.items():
        # 如果值是一个字典，递归调用_token_replace函数处理内部的字典
        if isinstance(value, dict):
            _token_replace(value)
        # 如果值是一个字符串
        elif isinstance(value, str):
            # 使用os.path.expandvars替换字符串中的环境变量占位符
            data[key] = os.path.expandvars(value)  # 替换后更新字典中的值

