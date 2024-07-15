# 这段代码是用来导入不同模块的配置输入类的。每个类都代表一种特定的配置选项。

# 导入一个叫做NotRequired的特殊类型，来自typing_extensions库
from typing_extensions import NotRequired

# 从.cache_config_input模块导入CacheConfigInput类，这个类可能关于缓存设置
from .cache_config_input import CacheConfigInput

# 从.chunking_config_input模块导入ChunkingConfigInput类，可能用于数据分块处理
from .chunking_config_input import ChunkingConfigInput

# 从.claim_extraction_config_input模块导入ClaimExtractionConfigInput类，可能用于提取声明或事实
from .claim_extraction_config_input import ClaimExtractionConfigInput

# 从.cluster_graph_config_input模块导入ClusterGraphConfigInput类，可能涉及图形聚类
from .cluster_graph_config_input import ClusterGraphConfigInput

# 从.community_reports_config_input模块导入CommunityReportsConfigInput类，可能用于社区报告
from .community_reports_config_input import CommunityReportsConfigInput

# 从.embed_graph_config_input模块导入EmbedGraphConfigInput类，可能用于图形嵌入
from .embed_graph_config_input import EmbedGraphConfigInput

# 从.entity_extraction_config_input模块导入EntityExtractionConfigInput类，可能用于实体识别
from .entity_extraction_config_input import EntityExtractionConfigInput

# 从.global_search_config_input模块导入GlobalSearchConfigInput类，可能用于全局搜索设置
from .global_search_config_input import GlobalSearchConfigInput

# 从.input_config_input模块导入InputConfigInput类，可能用于输入配置
from .input_config_input import InputConfigInput

# 从.llm_config_input模块导入LLMConfigInput类，可能与大型语言模型有关
from .llm_config_input import LLMConfigInput

# 从.local_search_config_input模块导入LocalSearchConfigInput类，可能用于局部搜索设置
from .local_search_config_input import LocalSearchConfigInput

# 从.reporting_config_input模块导入ReportingConfigInput类，可能用于报告生成设置
from .reporting_config_input import ReportingConfigInput

# 从.snapshots_config_input模块导入SnapshotsConfigInput类，可能关于快照或版本控制
from .snapshots_config_input import SnapshotsConfigInput

# 从.storage_config_input模块导入StorageConfigInput类，可能涉及存储设置
from .storage_config_input import StorageConfigInput

# 从.summarize_descriptions_config_input模块导入SummarizeDescriptionsConfigInput类，可能用于摘要生成
from .summarize_descriptions_config_input import SummarizeDescriptionsConfigInput

# 从.text_embedding_config_input模块导入TextEmbeddingConfigInput类，可能关于文本嵌入
from .text_embedding_config_input import TextEmbeddingConfigInput

# 从.umap_config_input模块导入UmapConfigInput类，可能用于UMAP（统一多维降维）算法配置
from .umap_config_input import UmapConfigInput

# 这段代码是微软公司写的，受到2024年版权保护。
# 使用的是MIT许可证，允许他人自由使用，但需要遵守一些规定。

# 这是一个关于默认配置参数设置的文档字符串。
# 它像说明书一样描述了代码的功能。

# 导入了一个Python的特殊类型NotRequired，它来自typing_extensions库。
from typing_extensions import NotRequired

# 从不同的模块导入了一些配置输入类。这些类是用来设置各种功能的参数的。
# 比如，CacheConfigInput是关于缓存设置的，
# ChunkingConfigInput是关于数据分块的，以此类推。

from .cache_config_input import CacheConfigInput
from .chunking_config_input import ChunkingConfigInput
from .claim_extraction_config_input import ClaimExtractionConfigInput
from .cluster_graph_config_input import ClusterGraphConfigInput
from .community_reports_config_input import CommunityReportsConfigInput
from .embed_graph_config_input import EmbedGraphConfigInput
from .entity_extraction_config_input import EntityExtractionConfigInput
from .global_search_config_input import GlobalSearchConfigInput
from .input_config_input import InputConfigInput
from .llm_config_input import LLMConfigInput
from .local_search_config_input import LocalSearchConfigInput
from .reporting_config_input import ReportingConfigInput
from .snapshots_config_input import SnapshotsConfigInput
from .storage_config_input import StorageConfigInput
from .summarize_descriptions_config_input import (
    SummarizeDescriptionsConfigInput,
)  # 注意这里括号里有一个逗号，表示这是一个列表，只有一个元素
from .text_embedding_config_input import TextEmbeddingConfigInput
from .umap_config_input import UmapConfigInput

# 定义一个名为GraphRagConfigInput的类，它是LLMConfigInput类的子类
class GraphRagConfigInput(LLMConfigInput):
    """这是一个基础类，用来设置默认配置参数。"""

    # 这一行定义了一个变量reporting，它可能不存在，如果存在可以是ReportingConfigInput类型或者None
    reporting: NotRequired[ReportingConfigInput | None]

    # 同上，定义了storage变量，可以是StorageConfigInput类型或None
    storage: NotRequired[StorageConfigInput | None]

    # 定义cache变量，可以是CacheConfigInput类型或None
    cache: NotRequired[CacheConfigInput | None]

    # 定义input变量，可以是InputConfigInput类型或None
    input: NotRequired[InputConfigInput | None]

    # 定义embed_graph变量，可以是EmbedGraphConfigInput类型或None
    embed_graph: NotRequired[EmbedGraphConfigInput | None]

    # 定义embeddings变量，可以是TextEmbeddingConfigInput类型或None
    embeddings: NotRequired[TextEmbeddingConfigInput | None]

    # 定义chunks变量，可以是ChunkingConfigInput类型或None
    chunks: NotRequired[ChunkingConfigInput | None]

    # 定义snapshots变量，可以是SnapshotsConfigInput类型或None
    snapshots: NotRequired[SnapshotsConfigInput | None]

    # 定义entity_extraction变量，可以是EntityExtractionConfigInput类型或None
    entity_extraction: NotRequired[EntityExtractionConfigInput | None]

    # 定义summarize_descriptions变量，可以是SummarizeDescriptionsConfigInput类型或None
    summarize_descriptions: NotRequired[SummarizeDescriptionsConfigInput | None]

    # 定义community_reports变量，可以是CommunityReportsConfigInput类型或None
    community_reports: NotRequired[CommunityReportsConfigInput | None]

    # 定义claim_extraction变量，可以是ClaimExtractionConfigInput类型或None
    claim_extraction: NotRequired[ClaimExtractionConfigInput | None]

    # 定义cluster_graph变量，可以是ClusterGraphConfigInput类型或None
    cluster_graph: NotRequired[ClusterGraphConfigInput | None]

    # 定义umap变量，可以是UmapConfigInput类型或None
    umap: NotRequired[UmapConfigInput | None]

    # 定义encoding_model变量，可以是一个字符串或None
    encoding_model: NotRequired[str | None]

    # 定义skip_workflows变量，可以是一个包含字符串的列表、单个字符串或None
    skip_workflows: NotRequired[list[str] | str | None]

    # 定义local_search变量，可以是LocalSearchConfigInput类型或None
    local_search: NotRequired[LocalSearchConfigInput | None]

    # 定义global_search变量，可以是GlobalSearchConfigInput类型或None
    global_search: NotRequired[GlobalSearchConfigInput | None]

