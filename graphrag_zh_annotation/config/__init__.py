# 导入一个叫做 create_graphrag_config 的函数，它来自 .create_graphrag_config 这个模块
from .create_graphrag_config import (
    create_graphrag_config,
)

# 导入一系列枚举类型（就是预定义的一些选项），它们来自 .enums 模块
from .enums import (
    CacheType,       # 缓存类型
    InputFileType,   # 输入文件类型
    InputType,       # 输入类型
    LLMType,         # 大语言模型类型
    ReportingType,   # 报告类型
    StorageType,     # 存储类型
    TextEmbeddingTarget, # 文本嵌入目标
)

# 导入一些错误类，当程序出错时会用到，它们来自 .errors 模块
from .errors import (
    ApiKeyMissingError,      # API密钥丢失错误
    AzureApiBaseMissingError,  # Azure API基础缺失错误
    AzureDeploymentNameMissingError, # Azure部署名称缺失错误
)

# 导入一些输入模型类，这些是配置信息的结构，来自 .input_models 模块
from .input_models import (
    CacheConfigInput,        # 缓存配置输入
    ChunkingConfigInput,      # 块划分配置输入
    ClaimExtractionConfigInput,  # 声明提取配置输入
    ClusterGraphConfigInput,   # 聚类图配置输入
    CommunityReportsConfigInput, # 社区报告配置输入
    EmbedGraphConfigInput,     # 嵌入图配置输入
    EntityExtractionConfigInput, # 实体提取配置输入
    GlobalSearchConfigInput,   # 全局搜索配置输入
    GraphRagConfigInput,       # GraphRAG配置输入
    InputConfigInput,          # 输入配置输入
    LLMConfigInput,            # 大语言模型配置输入
    LLMParametersInput,        # 大语言模型参数输入
    LocalSearchConfigInput,     # 本地搜索配置输入
    ParallelizationParametersInput, # 并行化参数输入
    ReportingConfigInput,       # 报告配置输入
    SnapshotsConfigInput,      # 快照配置输入
    StorageConfigInput,        # 存储配置输入
    SummarizeDescriptionsConfigInput, # 摘要描述配置输入
    TextEmbeddingConfigInput,   # 文本嵌入配置输入
    UmapConfigInput,           # UMAP配置输入
)

# 导入一些模型类，这些是配置信息的实例，来自 .models 模块
from .models import (
    CacheConfig,              # 缓存配置
    ChunkingConfig,           # 块划分配置
    ClaimExtractionConfig,     # 声明提取配置
    ClusterGraphConfig,        # 聚类图配置
    CommunityReportsConfig,    # 社区报告配置
    EmbedGraphConfig,          # 嵌入图配置
    EntityExtractionConfig,    # 实体提取配置
    GlobalSearchConfig,        # 全局搜索配置
    GraphRagConfig,            # GraphRAG配置
    InputConfig,               # 输入配置
    LLMConfig,                 # 大语言模型配置
    LLMParameters,             # 大语言模型参数
    LocalSearchConfig,         # 本地搜索配置
    ParallelizationParameters, # 并行化参数
    ReportingConfig,           # 报告配置
    SnapshotsConfig,           # 快照配置
    StorageConfig,             # 存储配置
    SummarizeDescriptionsConfig, # 摘要描述配置
    TextEmbeddingConfig,       # 文本嵌入配置
    UmapConfig,                # UMAP配置
)

# 导入一个函数 read_dotenv，它用来读取环境变量，来自 .read_dotenv 模块
from .read_dotenv import read_dotenv

# 这段代码是微软公司的一个软件配置包，使用了MIT许可证
# Copyright (c) 2024 Microsoft Corporation. # 版权属于微软公司，时间是2024年
# Licensed under the MIT License # 使用的是MIT许可证

# 这个文件是索引引擎的默认配置包的根目录
"""The Indexing Engine default config package root."""

# 从.create_graphrag_config模块导入了一个函数，用于创建GraphRag配置
from .create_graphrag_config import (
    create_graphrag_config,
)

# 从.enums模块导入了一系列的枚举类，用于定义不同的类型
from .enums import (
    CacheType,  # 缓存类型
    InputFileType,  # 输入文件类型
    InputType,  # 输入类型
    LLMType,  # 语言模型类型
    ReportingType,  # 报告类型
    StorageType,  # 存储类型
    TextEmbeddingTarget,  # 文本嵌入目标
)

# 从.errors模块导入了一些错误类，表示在程序运行时可能遇到的问题
from .errors import (
    ApiKeyMissingError,  # API密钥缺失错误
    AzureApiBaseMissingError,  # Azure API基础地址缺失错误
    AzureDeploymentNameMissingError,  # Azure部署名称缺失错误
)

# 从.input_models模块导入了一系列的输入配置类，用于定义配置信息
from .input_models import (
    # 导入各种配置输入类，如缓存、分块、实体提取等
    CacheConfigInput,
    ChunkingConfigInput,
    ClaimExtractionConfigInput,
    ClusterGraphConfigInput,
    CommunityReportsConfigInput,
    EmbedGraphConfigInput,
    EntityExtractionConfigInput,
    GlobalSearchConfigInput,
    GraphRagConfigInput,
    InputConfigInput,
    LLMConfigInput,
    LLMParametersInput,
    LocalSearchConfigInput,
    ParallelizationParametersInput,
    ReportingConfigInput,
    SnapshotsConfigInput,
    StorageConfigInput,
    SummarizeDescriptionsConfigInput,
    TextEmbeddingConfigInput,
    UmapConfigInput,
)

# 从.models模块导入了一系列的模型类，这些类对应于配置输入类，用于存储配置信息
from .models import (
    # 导入各种配置类，与输入类相对应
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
    LLMConfig,
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

# 从.read_dotenv模块导入了一个函数，用于读取环境变量
from .read_dotenv import read_dotenv

# 这里列出所有对外公开的类和函数，使得其他代码可以使用它们
__all__ = [
    # 列出所有的错误类
    "ApiKeyMissingError",
    "AzureApiBaseMissingError",
    "AzureDeploymentNameMissingError",
    
    # 列出所有的配置类和输入类，以及枚举类型
    "CacheConfig",
    "CacheConfigInput",
    "CacheType",
    "ChunkingConfig",
    "ChunkingConfigInput",
    ...
    # 其他类似的配置类、输入类和枚举类型
    
    # 导入的函数
    "create_graphrag_config",
    "read_dotenv",
]

