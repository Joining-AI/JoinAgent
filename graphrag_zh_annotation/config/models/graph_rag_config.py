# 导入一个叫做pformat的工具，它能帮助我们格式化打印复杂的Python对象
from devtools import pformat

# 导入Pydantic的Field类，这是一个用来定义数据模型字段的工具
from pydantic import Field

# 导入默认配置的模块
import graphrag.config.defaults as defs

# 从当前目录下的cache_config模块导入CacheConfig类，关于缓存的配置
from .cache_config import CacheConfig
# 从chunking_config模块导入ChunkingConfig类，关于数据分块的配置
from .chunking_config import ChunkingConfig
# 从claim_extraction_config模块导入ClaimExtractionConfig类，关于主张提取的配置
from .claim_extraction_config import ClaimExtractionConfig
# 从cluster_graph_config模块导入ClusterGraphConfig类，关于聚类图的配置
from .cluster_graph_config import ClusterGraphConfig
# 从community_reports_config模块导入CommunityReportsConfig类，关于社区报告的配置
from .community_reports_config import CommunityReportsConfig
# 从embed_graph_config模块导入EmbedGraphConfig类，关于嵌入图的配置
from .embed_graph_config import EmbedGraphConfig
# 从entity_extraction_config模块导入EntityExtractionConfig类，关于实体提取的配置
from .entity_extraction_config import EntityExtractionConfig
# 从global_search_config模块导入GlobalSearchConfig类，关于全局搜索的配置
from .global_search_config import GlobalSearchConfig
# 从input_config模块导入InputConfig类，关于输入的配置
from .input_config import InputConfig
# 从llm_config模块导入LLMConfig类，关于语言模型的配置
from .llm_config import LLMConfig
# 从local_search_config模块导入LocalSearchConfig类，关于本地搜索的配置
from .local_search_config import LocalSearchConfig
# 从reporting_config模块导入ReportingConfig类，关于报告的配置
from .reporting_config import ReportingConfig
# 从snapshots_config模块导入SnapshotsConfig类，关于快照的配置
from .snapshots_config import SnapshotsConfig
# 从storage_config模块导入StorageConfig类，关于存储的配置
from .storage_config import StorageConfig
# 从summarize_descriptions_config模块导入SummarizeDescriptionsConfig类，关于总结描述的配置
from .summarize_descriptions_config import SummarizeDescriptionsConfig
# 从text_embedding_config模块导入TextEmbeddingConfig类，关于文本嵌入的配置
from .text_embedding_config import TextEmbeddingConfig
# 从umap_config模块导入UmapConfig类，关于UMAP（统一多维降维）的配置
from .umap_config import UmapConfig

# 这是版权信息，说明代码由微软公司2024年创建，遵循MIT许可证
# 注释：这部分代码不执行，只是提供法律信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块的作用
"""
Parameterization settings for the default configuration.
"""

# 这里没有实际的代码，只是模块的一部分，可能用于将来添加内容

# 这是一个定义类的代码，叫做GraphRagConfig，它是LLMConfig类的子类
class GraphRagConfig(LLMConfig):
    # 这个类是默认配置参数设置的基础类
    """Base class for the Default-Configuration parameterization settings."""

    # 当我们打印这个类的实例时，会返回一个格式化的字符串
    def __repr__(self) -> str:
        """Get a string representation."""
        return pformat(self, highlight=False)

    # 同样，当用print()函数打印这个类的实例时，也会返回一个字符串，但这次是用缩进的JSON格式
    def __str__(self):
        """Get a string representation."""
        return self.model_dump_json(indent=4)

    # 这个变量root_dir是一个字符串，表示配置的根目录，默认值是None
    root_dir: str = Field(description="配置的根目录。", default=None)

    # reporting变量是ReportingConfig类的一个实例，用于配置报告相关设置，默认值是ReportingConfig类的一个实例
    reporting: ReportingConfig = Field(description="报告配置。", default=ReportingConfig())
    """The reporting configuration."""

    # storage变量是StorageConfig类的一个实例，用于配置存储相关设置，默认值是StorageConfig类的一个实例
    storage: StorageConfig = Field(description="存储配置。", default=StorageConfig())
    """The storage configuration."""

    # cache变量是CacheConfig类的一个实例，用于配置缓存相关设置，默认值是CacheConfig类的一个实例
    cache: CacheConfig = Field(description="缓存配置。", default=CacheConfig())
    """The cache configuration."""

    # input变量是InputConfig类的一个实例，用于配置输入相关设置，默认值是InputConfig类的一个实例
    input: InputConfig = Field(description="输入配置。", default=InputConfig())
    """The input configuration."""

    # embed_graph变量是EmbedGraphConfig类的一个实例，用于配置图嵌入的设置，默认值是EmbedGraphConfig类的一个实例
    embed_graph: EmbedGraphConfig = Field(description="图嵌入配置。", default=EmbedGraphConfig())
    """Graph Embedding configuration."""

    # embeddings变量是TextEmbeddingConfig类的一个实例，用于配置文本嵌入的LLM（大语言模型）设置，默认值是TextEmbeddingConfig类的一个实例
    embeddings: TextEmbeddingConfig = Field(description="使用的文本嵌入LLM配置。", default=TextEmbeddingConfig())
    """The embeddings LLM configuration to use."""

    # chunks变量是ChunkingConfig类的一个实例，用于配置分块的设置，默认值是ChunkingConfig类的一个实例
    chunks: ChunkingConfig = Field(description="使用的分块配置。", default=ChunkingConfig())
    """The chunking configuration to use."""

    # snapshots变量是SnapshotsConfig类的一个实例，用于配置快照的设置，默认值是SnapshotsConfig类的一个实例
    snapshots: SnapshotsConfig = Field(description="使用的快照配置。", default=SnapshotsConfig())
    """The snapshots configuration to use."""

    # entity_extraction变量是EntityExtractionConfig类的一个实例，用于配置实体提取的设置，默认值是EntityExtractionConfig类的一个实例
    entity_extraction: EntityExtractionConfig = Field(description="使用的实体提取配置。", default=EntityExtractionConfig())
    """The entity extraction configuration to use."""

    # summarize_descriptions变量是SummarizeDescriptionsConfig类的一个实例，用于配置描述摘要的设置，默认值是SummarizeDescriptionsConfig类的一个实例
    summarize_descriptions: SummarizeDescriptionsConfig = Field(description="使用的描述摘要配置。", default=SummarizeDescriptionsConfig())
    """The description summarization configuration to use."""

    # community_reports变量是CommunityReportsConfig类的一个实例，用于配置社区报告的设置，默认值是CommunityReportsConfig类的一个实例
    community_reports: CommunityReportsConfig = Field(description="使用的社区报告配置。", default=CommunityReportsConfig())
    """The community reports configuration to use."""

    # claim_extraction变量是ClaimExtractionConfig类的一个实例，用于配置声明提取的设置，默认值是ClaimExtractionConfig类的一个实例，可能包含是否启用的设置
    claim_extraction: ClaimExtractionConfig = Field(description="使用的声明提取配置。", default=ClaimExtractionConfig(enabled=defs.CLAIM_EXTRACTION_ENABLED))
    """The claim extraction configuration to use."""

    # cluster_graph变量是ClusterGraphConfig类的一个实例，用于配置聚类图的设置，默认值是ClusterGraphConfig类的一个实例
    cluster_graph: ClusterGraphConfig = Field(description="使用的聚类图配置。", default=ClusterGraphConfig())
    """The cluster graph configuration to use."""

    # umap变量是UmapConfig类的一个实例，用于配置UMAP（统一多维尺度映射）的设置，默认值是UmapConfig类的一个实例
    umap: UmapConfig = Field(description="使用的UMAP配置。", default=UmapConfig())
    """The UMAP configuration to use."""

    # local_search变量是LocalSearchConfig类的一个实例，用于配置局部搜索的设置，默认值是LocalSearchConfig类的一个实例
    local_search: LocalSearchConfig = Field(description="使用的局部搜索配置。", default=LocalSearchConfig())
    """The local search configuration."""

    # global_search变量是GlobalSearchConfig类的一个实例，用于配置全局搜索的设置，默认值是GlobalSearchConfig类的一个实例
    global_search: GlobalSearchConfig = Field(description="使用的全局搜索配置。", default=GlobalSearchConfig())
    """The global search configuration."""

    # encoding_model是一个字符串，用于指定要使用的编码模型，默认值是defs.ENCODING_MODEL中的值
    encoding_model: str = Field(description="要使用的编码模型。", default=defs.ENCODING_MODEL)
    """The encoding model to use."""

    # skip_workflows是一个字符串列表，用于指定在运行时要跳过的流程，通常用于测试，默认为空列表
    skip_workflows: list[str] = Field(description="因为测试等原因要跳过的流程。", default=[])
    """The workflows to skip, usually for testing reasons."""

