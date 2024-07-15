# 导入一个叫做PipelineCache的模块，这个模块可以帮助我们存储数据
from .cache import PipelineCache

# 导入多个配置相关的类，这些类是用来设置和管理管道（Pipeline）的参数
from .config import (
    PipelineBlobCacheConfig,  # 用于设置Blob缓存的配置
    PipelineBlobReportingConfig,  # Blob报告配置
    PipelineBlobStorageConfig,  # Blob存储配置
    PipelineCacheConfig,  # 缓存配置基础类
    PipelineCacheConfigTypes,  # 缓存配置类型
    PipelineConfig,  # 管道总配置
    PipelineConsoleReportingConfig,  # 控制台报告配置
    PipelineCSVInputConfig,  # CSV输入配置
    PipelineFileCacheConfig,  # 文件缓存配置
    PipelineFileReportingConfig,  # 文件报告配置
    PipelineFileStorageConfig,  # 文件存储配置
    PipelineInputConfig,  # 输入配置基础类
    PipelineInputConfigTypes,  # 输入配置类型
    PipelineMemoryCacheConfig,  # 内存缓存配置
    PipelineMemoryStorageConfig,  # 内存存储配置
    PipelineNoneCacheConfig,  # 无缓存配置
    PipelineReportingConfig,  # 报告配置基础类
    PipelineReportingConfigTypes,  # 报告配置类型
    PipelineStorageConfig,  # 存储配置基础类
    PipelineStorageConfigTypes,  # 存储配置类型
    PipelineTextInputConfig,  # 文本输入配置
    PipelineWorkflowConfig,  # 工作流配置
    PipelineWorkflowReference,  # 工作流引用
    PipelineWorkflowStep,  # 工作流步骤
)

# 导入一个函数，用来创建管道配置
from .create_pipeline_config import create_pipeline_config

# 导入错误处理类，当遇到问题时，程序会抛出这些错误
from .errors import (
    NoWorkflowsDefinedError,  # 没有定义工作流的错误
    UndefinedWorkflowError,  # 未定义的工作流错误
    UnknownWorkflowError,  # 未知工作流错误
)

# 导入一个函数，从文件加载管道配置
from .load_pipeline_config import load_pipeline_config

# 导入两个运行管道的函数，一个直接运行，一个带配置运行
from .run import run_pipeline, run_pipeline_with_config

# 导入一个模块，用于管理管道的数据存储
from .storage import PipelineStorage

# 这段代码是Python语言写的，它定义了一个叫做"Indexing Engine package"的东西。
# 注释中的年份2024是版权信息，Microsoft公司拥有这个代码。
# 它遵循MIT许可证，意味着你可以自由使用，但需要遵守一定的规则。

# 这个字符串是包的描述，告诉人们这个包是用来做什么的。
"""The Indexing Engine package root."""

# 这里从.cache模块导入了PipelineCache类
from .cache import PipelineCache

# 从.config模块导入了很多配置相关的类
from .config import (
    PipelineBlobCacheConfig,
    PipelineBlobReportingConfig,
    PipelineBlobStorageConfig,
    PipelineCacheConfig,
    PipelineCacheConfigTypes,
    PipelineConfig,
    PipelineConsoleReportingConfig,
    PipelineCSVInputConfig,
    PipelineFileCacheConfig,
    PipelineFileReportingConfig,
    PipelineFileStorageConfig,
    PipelineInputConfig,
    PipelineInputConfigTypes,
    PipelineMemoryCacheConfig,
    PipelineMemoryStorageConfig,
    PipelineNoneCacheConfig,
    PipelineReportingConfig,
    PipelineReportingConfigTypes,
    PipelineStorageConfig,
    PipelineStorageConfigTypes,
    PipelineTextInputConfig,
    PipelineWorkflowConfig,
    PipelineWorkflowReference,
    PipelineWorkflowStep,
)

# 从.create_pipeline_config模块导入了create_pipeline_config函数
from .create_pipeline_config import create_pipeline_config

# 从.errors模块导入了一些错误类
from .errors import (
    NoWorkflowsDefinedError,
    UndefinedWorkflowError,
    UnknownWorkflowError,
)

# 从.load_pipeline_config模块导入了load_pipeline_config函数
from .load_pipeline_config import load_pipeline_config

# 从.run模块导入了run_pipeline和run_pipeline_with_config两个函数
from .run import run_pipeline, run_pipeline_with_config

# 从.storage模块导入了PipelineStorage类
from .storage import PipelineStorage

# 这个列表(__all__)告诉别人这个包里有哪些东西可以被外部直接使用
__all__ = [
    # 这里列出了所有可以被外部使用的类和函数
    ...
]

# 注意：这里的省略号表示列表中还有很多类和函数，为了简洁没有全部列出

