# 这段代码是从不同的模块中导入一些特定的类和配置。让我们逐行解释：

from .cache import (
    # 这里是关于缓存的部分，用于存储数据以加快处理速度
    PipelineBlobCacheConfig,  # 一种基于云存储的缓存配置
    PipelineCacheConfig,      # 缓存配置的基类
    PipelineCacheConfigTypes,  # 缓存配置类型的枚举
    PipelineFileCacheConfig,   # 基于文件系统的缓存配置
    PipelineMemoryCacheConfig,  # 基于内存的缓存配置
    PipelineNoneCacheConfig,   # 不使用缓存的配置
)

from .input import (
    # 这里是关于输入数据的部分，定义了如何读取数据
    PipelineCSVInputConfig,   # CSV文件输入配置
    PipelineInputConfig,       # 输入配置的基类
    PipelineInputConfigTypes,  # 输入配置类型的枚举
    PipelineTextInputConfig,   # 文本输入配置
)

from .pipeline import PipelineConfig  # 这是整个管道（处理流程）的配置

from .reporting import (
    # 这部分是关于报告和结果输出的配置
    PipelineBlobReportingConfig,  # 通过云存储报告结果的配置
    PipelineConsoleReportingConfig,  # 在控制台打印报告的配置
    PipelineFileReportingConfig,   # 通过文件保存报告的配置
    PipelineReportingConfig,       # 报告配置的基类
    PipelineReportingConfigTypes,  # 报告配置类型的枚举
)

from .storage import (
    # 这里是关于数据存储的部分，定义了如何保存处理后的数据
    PipelineBlobStorageConfig,  # 云存储配置
    PipelineFileStorageConfig,   # 文件系统存储配置
    PipelineMemoryStorageConfig,  # 内存存储配置
    PipelineStorageConfig,       # 存储配置的基类
    PipelineStorageConfigTypes,  # 存储配置类型的枚举
)

from .workflow import (
    # 这部分是关于工作流程的配置和定义
    PipelineWorkflowConfig,     # 工作流程配置
    PipelineWorkflowReference,  # 引用其他工作流程的配置
    PipelineWorkflowStep,       # 工作流程中的一个步骤
)

# 这是Python代码，它定义了一些关于索引引擎配置的类型
# 注释中的文字表示这是微软公司的版权信息，2024年有效
# 并且代码遵循MIT许可证

# 这是一个描述包的字符串，"Indexing Engine config typing package root" 意味着这是一个配置相关的类型定义包的根目录
"""The Indexing Engine config typing package root."""

# 从.cache模块导入以下类：
# PipelineBlobCacheConfig: 有关缓存Blob（大对象）的配置
# PipelineCacheConfig: 通用的缓存配置
# PipelineCacheConfigTypes: 缓存配置的类型集合
# PipelineFileCacheConfig: 文件缓存的配置
# PipelineMemoryCacheConfig: 内存缓存的配置
# PipelineNoneCacheConfig: 不使用缓存的配置
from .cache import (
    PipelineBlobCacheConfig,
    PipelineCacheConfig,
    PipelineCacheConfigTypes,
    PipelineFileCacheConfig,
    PipelineMemoryCacheConfig,
    PipelineNoneCacheConfig,
)

# 从.input模块导入以下类：
# PipelineCSVInputConfig: CSV文件输入的配置
# PipelineInputConfig: 一般输入配置
# PipelineInputConfigTypes: 输入配置的类型集合
# PipelineTextInputConfig: 文本输入的配置
from .input import (
    PipelineCSVInputConfig,
    PipelineInputConfig,
    PipelineInputConfigTypes,
    PipelineTextInputConfig,
)

# 从.pipeline模块导入 PipelineConfig 类：这是整个管道的配置
from .pipeline import PipelineConfig

# 从.reporting模块导入以下类：
# PipelineBlobReportingConfig: Blob报告配置
# PipelineConsoleReportingConfig: 控制台报告配置
# PipelineFileReportingConfig: 文件报告配置
# PipelineReportingConfig: 报告配置的基类
# PipelineReportingConfigTypes: 报告配置的类型集合
from .reporting import (
    PipelineBlobReportingConfig,
    PipelineConsoleReportingConfig,
    PipelineFileReportingConfig,
    PipelineReportingConfig,
    PipelineReportingConfigTypes,
)

# 从.storage模块导入以下类：
# PipelineBlobStorageConfig: Blob存储配置
# PipelineFileStorageConfig: 文件存储配置
# PipelineMemoryStorageConfig: 内存存储配置
# PipelineStorageConfig: 存储配置的基类
# PipelineStorageConfigTypes: 存储配置的类型集合
from .storage import (
    PipelineBlobStorageConfig,
    PipelineFileStorageConfig,
    PipelineMemoryStorageConfig,
    PipelineStorageConfig,
    PipelineStorageConfigTypes,
)

# 从.workflow模块导入以下类：
# PipelineWorkflowConfig: 工作流程配置
# PipelineWorkflowReference: 工作流程引用
# PipelineWorkflowStep: 工作流程步骤
from .workflow import (
    PipelineWorkflowConfig,
    PipelineWorkflowReference,
    PipelineWorkflowStep,
)

# "__all__" 是一个列表，它告诉别人这个模块导出了哪些名字
# 这里列出了所有前面导入的类，以便其他地方可以方便地使用它们
__all__ = [
    # 列出的所有类名...
]

