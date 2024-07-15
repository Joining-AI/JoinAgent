# 这段代码是导入了多个不同功能的模块，它们都是用来配置和管理某些任务的。下面我会用简单易懂的语言解释每一行。

# 导入"缓存配置输入"模块，它帮助我们保存和加载数据，防止重复计算。
from .cache_config_input import CacheConfigInput

# 导入"分块配置输入"模块，这个可能用于大文件处理，分成小块操作。
from .chunking_config_input import ChunkingConfigInput

# 导入"声明提取配置输入"模块，用于识别和提取文本中的关键信息。
from .claim_extraction_config_input import ClaimExtractionConfigInput

# 导入"聚类图配置输入"模块，帮助组织和分类数据。
from .cluster_graph_config_input import ClusterGraphConfigInput

# 导入"社区报告配置输入"模块，可能用于生成关于用户群体的报告。
from .community_reports_config_input import CommunityReportsConfigInput

# 导入"嵌入图配置输入"模块，将数据转换成图形并存储其关系。
from .embed_graph_config_input import EmbedGraphConfigInput

# 导入"实体提取配置输入"模块，用于找出文本中的专有名词，如人名、地名等。
from .entity_extraction_config_input import EntityExtractionConfigInput

# 导入"全局搜索配置输入"模块，用于在整个数据集中查找信息。
from .global_search_config_input import GlobalSearchConfigInput

# 导入"图碎片配置输入"模块，可能与处理复杂图形或网络有关。
from .graphrag_config_input import GraphRagConfigInput

# 导入"输入配置输入"模块，定义如何处理程序接收的数据。
from .input_config_input import InputConfigInput

# 导入"大型语言模型配置输入"模块，用于处理复杂的自然语言任务。
from .llm_config_input import LLMConfigInput

# 导入"大型语言模型参数输入"模块，设置语言模型的特定参数。
from .llm_parameters_input import LLMParametersInput

# 导入"局部搜索配置输入"模块，用于在特定范围内查找信息。
from .local_search_config_input import LocalSearchConfigInput

# 导入"并行化参数输入"模块，让程序同时做多件事，提高效率。
from .parallelization_parameters_input import ParallelizationParametersInput

# 导入"报告配置输入"模块，定义如何生成和格式化报告。
from .reporting_config_input import ReportingConfigInput

# 导入"快照配置输入"模块，可能用于保存程序运行时的状态。
from .snapshots_config_input import SnapshotsConfigInput

# 导入"存储配置输入"模块，设置数据的存储方式。
from .storage_config_input import StorageConfigInput

# 导入"总结描述配置输入"模块，用于简述长文本。
SummarizeDescriptionsConfigInput,

# 导入"文本嵌入配置输入"模块，将文本转换成可以比较的形式。
from .text_embedding_config_input import TextEmbeddingConfigInput

# 导入"UMAP配置输入"模块，UMAP是一种降维技术，让高维数据可视化。
from .umap_config_input import UmapConfigInput

# 这行代码是说，从2024年开始，这段代码的版权属于微软公司。
# Copyright (c) 2024 Microsoft Corporation.

# 接下来这一行表示，这段代码遵循MIT许可证的规则。
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块的功能。它定义了一些默认配置参数的接口。
"""这是用于默认配置参数化的接口。"""

# 下面这些行在导入不同的配置输入类。这些类可能用于处理各种任务，比如缓存、分块、文本提取等。
# 每个类代表一种特定的配置需求。
from .cache_config_input import CacheConfigInput
from .chunking_config_input import ChunkingConfigInput
from .claim_extraction_config_input import ClaimExtractionConfigInput
from .cluster_graph_config_input import ClusterGraphConfigInput
from .community_reports_config_input import CommunityReportsConfigInput
from .embed_graph_config_input import EmbedGraphConfigInput
from .entity_extraction_config_input import EntityExtractionConfigInput
from .global_search_config_input import GlobalSearchConfigInput
from .graphrag_config_input import GraphRagConfigInput
from .input_config_input import InputConfigInput
from .llm_config_input import LLMConfigInput
from .llm_parameters_input import LLMParametersInput
from .local_search_config_input import LocalSearchConfigInput
from .parallelization_parameters_input import ParallelizationParametersInput
from .reporting_config_input import ReportingConfigInput
from .snapshots_config_input import SnapshotsConfigInput
from .storage_config_input import StorageConfigInput
from .summarize_descriptions_config_input import SummarizeDescriptionsConfigInput
from .text_embedding_config_input import TextEmbeddingConfigInput
from .umap_config_input import UmapConfigInput

# 这一行创建了一个列表，包含了所有导入的类名。这样其他部分的代码可以通过这个列表知道有哪些可用的配置类。
__all__ = [
    "CacheConfigInput",
    "ChunkingConfigInput",
    "ClaimExtractionConfigInput",
    "ClusterGraphConfigInput",
    "CommunityReportsConfigInput",
    "EmbedGraphConfigInput",
    "EntityExtractionConfigInput",
    "GlobalSearchConfigInput",
    "GraphRagConfigInput",
    "InputConfigInput",
    "LLMConfigInput",
    "LLMParametersInput",
    "LocalSearchConfigInput",
    "ParallelizationParametersInput",
    "ReportingConfigInput",
    "SnapshotsConfigInput",
    "StorageConfigInput",
    "SummarizeDescriptionsConfigInput",
    "TextEmbeddingConfigInput",
    "UmapConfigInput",
]

