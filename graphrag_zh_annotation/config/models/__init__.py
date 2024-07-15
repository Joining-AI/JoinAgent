# 这段代码是导入一些预先定义好的配置类。这些类帮助程序知道如何执行不同的任务。
# 每个类都代表一种特定的设置或参数，比如缓存、分块、实体提取等。

# 导入CacheConfig类，它关于如何存储和检索数据的规则。
from .cache_config import CacheConfig

# 导入ChunkingConfig类，它定义了如何把大文本分成小块。
from .chunking_config import ChunkingConfig

# 导入ClaimExtractionConfig类，它包含了识别声明或观点的规则。
from .claim_extraction_config import ClaimExtractionConfig

# 导入ClusterGraphConfig类，可能与数据聚类和图形结构有关。
from .cluster_graph_config import ClusterGraphConfig

# 导入CommunityReportsConfig类，可能用于生成社区报告的设置。
from .community_reports_config import CommunityReportsConfig

# 导入EmbedGraphConfig类，它处理文本嵌入到图中的方式。
from .embed_graph_config import EmbedGraphConfig

# 导入EntityExtractionConfig类，用于识别文本中的名词短语或实体。
from .entity_extraction_config import EntityExtractionConfig

# 导入GlobalSearchConfig类，定义全局搜索的规则。
from .global_search_config import GlobalSearchConfig

# 导入GraphRagConfig类，可能涉及图的随机访问格（RAG）操作。
from .graph_rag_config import GraphRagConfig

# 导入InputConfig类，它定义了程序接受输入的方式。
from .input_config import InputConfig

# 导入LLMConfig类，可能与语言模型的配置相关。
from .llm_config import LLMConfig

# 导入LLMParameters类，包含语言模型的特定参数。
from .llm_parameters import LLMParameters

# 导入LocalSearchConfig类，定义局部搜索的规则。
from .local_search_config import LocalSearchConfig

# 导入ParallelizationParameters类，关于如何并行化任务以提高效率的设置。
from .parallelization_parameters import ParallelizationParameters

# 导入ReportingConfig类，它包含生成报告的选项和格式。
from .reporting_config import ReportingConfig

# 导入SnapshotsConfig类，可能涉及保存和恢复程序状态的规则。
from .snapshots_config import SnapshotsConfig

# 导入StorageConfig类，定义数据存储的规则。
from .storage_config import StorageConfig

# 导入SummarizeDescriptionsConfig类，用于生成文本摘要的设置。
from .summarize_descriptions_config import SummarizeDescriptionsConfig

# 导入TextEmbeddingConfig类，处理文本嵌入到向量空间的方法。
from .text_embedding_config import TextEmbeddingConfig

# 导入UmapConfig类，可能涉及UMAP（统一近邻嵌入）算法的配置。
from .umap_config import UmapConfig

# 这段代码的版权属于2024年的微软公司。
# 它遵循MIT许可证的规定

# 这是一个关于默认配置参数化的接口描述。

# 从不同的模块导入一些配置类：
# - CacheConfig: 关于缓存设置的类
# - ChunkingConfig: 分块处理配置类
# - ClaimExtractionConfig: 声明提取配置类
# - ClusterGraphConfig: 簇图配置类
# - CommunityReportsConfig: 社区报告配置类
# - EmbedGraphConfig: 嵌入图配置类
# - EntityExtractionConfig: 实体提取配置类
# - GlobalSearchConfig: 全局搜索配置类
# - GraphRagConfig: 图RAG（区域附加图形）配置类
# - InputConfig: 输入配置类
# - LLMConfig: 大规模语言模型配置类
# - LLMParameters: 语言模型参数类
# - LocalSearchConfig: 局部搜索配置类
# - ParallelizationParameters: 并行化参数类
# - ReportingConfig: 报告生成配置类
# - SnapshotsConfig: 快照配置类
# - StorageConfig: 存储配置类
# - SummarizeDescriptionsConfig: 摘要描述配置类
# - TextEmbeddingConfig: 文本嵌入配置类
# - UmapConfig: UMAP（统一多维尺度映射）配置类

# '__all__' 是一个列表，包含了这个文件中对外公开的类名，
# 这些类可以在其他地方被导入和使用。

__all__ = [
    "CacheConfig",
    "ChunkingConfig",
    "ClaimExtractionConfig",
    "ClusterGraphConfig",
    "CommunityReportsConfig",
    "EmbedGraphConfig",
    "EntityExtractionConfig",
    "GlobalSearchConfig",
    "GraphRagConfig",
    "InputConfig",
    "LLMConfig",
    "LLMParameters",
    "LocalSearchConfig",
    "ParallelizationParameters",
    "ReportingConfig",
    "SnapshotsConfig",
    "StorageConfig",
    "SummarizeDescriptionsConfig",
    "TextEmbeddingConfig",
    "UmapConfig",
]

