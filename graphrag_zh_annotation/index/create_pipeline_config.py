# 导入json模块，用于处理JSON格式的数据
import json

# 导入logging模块，用于记录程序运行时的日志信息
import logging

# 导入Path模块，方便处理文件路径
from pathlib import Path

# 从graphrag.config.enums导入多个枚举类，这些类定义了一些特定的类型
from graphrag.config.enums import (
    CacheType,  # 缓存类型的枚举
    InputFileType,  # 输入文件类型的枚举
    ReportingType,  # 报告生成类型的枚举
    StorageType,  # 存储类型的枚举
    TextEmbeddingTarget,  # 文本嵌入的目标类型枚举
)

# 从graphrag.config.models导入两个配置模型类
from graphrag.config.models import (
    GraphRagConfig,  # 主要的GraphRag配置类
    TextEmbeddingConfig,  # 文本嵌入配置类
)

# 从graphrag.index.config.cache导入多个缓存配置类
from graphrag.index.config.cache import (
    PipelineBlobCacheConfig,  # 对象存储缓存配置类
    PipelineCacheConfigTypes,  # 缓存配置类型枚举
    PipelineFileCacheConfig,  # 文件系统缓存配置类
    PipelineMemoryCacheConfig,  # 内存缓存配置类
    PipelineNoneCacheConfig,  # 无缓存配置类
)

# 从graphrag.index.config.input导入输入配置类
from graphrag.index.config.input import (
    PipelineCSVInputConfig,  # CSV文件输入配置类
    PipelineInputConfigTypes,  # 输入配置类型枚举
    PipelineTextInputConfig,  # 文本输入配置类
)

# 从graphrag.index.config.pipeline导入管道配置类
from graphrag.index.config.pipeline import (
    PipelineConfig,  # 管道配置类
)

# 从graphrag.index.config.reporting导入报告配置类
from graphrag.index.config.reporting import (
    PipelineBlobReportingConfig,  # 对象存储报告配置类
    PipelineConsoleReportingConfig,  # 控制台报告配置类
    PipelineFileReportingConfig,  # 文件报告配置类
    PipelineReportingConfigTypes,  # 报告配置类型枚举
)

# 从graphrag.index.config.storage导入存储配置类
from graphrag.index.config.storage import (
    PipelineBlobStorageConfig,  # 对象存储配置类
    PipelineFileStorageConfig,  # 文件系统存储配置类
    PipelineMemoryStorageConfig,  # 内存存储配置类
    PipelineStorageConfigTypes,  # 存储配置类型枚举
)

# 从graphrag.index.config.workflow导入工作流引用类
from graphrag.index.config.workflow import (
    PipelineWorkflowReference,  # 工作流引用类
)

# 从graphrag.index.workflows.default_workflows导入多个默认工作流程函数
from graphrag.index.workflows.default_workflows import (
    create_base_documents,  # 创建基础文档
    create_base_entity_graph,  # 创建基础实体图
    create_base_extracted_entities,  # 创建基础提取的实体
    create_base_text_units,  # 创建基础文本单元
    create_final_communities,  # 创建最终社区
    create_final_community_reports,  # 创建最终社区报告
    create_final_covariates,  # 创建最终协变量
    create_final_documents,  # 创建最终文档
    create_final_entities,  # 创建最终实体
    create_final_nodes,  # 创建最终节点
    create_final_relationships,  # 创建最终关系
    create_final_text_units,  # 创建最终文本单元
    create_summarized_entities,  # 创建总结的实体
    join_text_units_to_covariate_ids,  # 将文本单元连接到协变量ID
    join_text_units_to_entity_ids,  # 将文本单元连接到实体ID
    join_text_units_to_relationship_ids,  # 将文本单元连接到关系ID
)

# 这段代码的版权属于微软公司，2024年
# 并且遵循MIT许可证

# 定义默认配置方法的模块

# 导入需要的库
import json  # 用于处理JSON数据
import logging  # 用于记录程序运行日志
from pathlib import Path  # 用于处理文件路径

# 导入自定义的枚举类型和模型类
from graphrag.config.enums import (
    CacheType,  # 缓存类型枚举
    InputFileType,  # 输入文件类型枚举
    ReportingType,  # 报告类型枚举
    StorageType,  # 存储类型枚举
    TextEmbeddingTarget,  # 文本嵌入目标枚举
)
from graphrag.config.models import (
    GraphRagConfig,  # 图形碎片配置类
    TextEmbeddingConfig,  # 文本嵌入配置类
)

# 导入各个部分的配置类
from graphrag.index.config.cache import (
    PipelineBlobCacheConfig,  # Blob缓存配置类
    PipelineCacheConfigTypes,  # 缓存配置类型
    PipelineFileCacheConfig,  # 文件缓存配置类
    PipelineMemoryCacheConfig,  # 内存缓存配置类
    PipelineNoneCacheConfig,  # 无缓存配置类
)
from graphrag.index.config.input import (
    PipelineCSVInputConfig,  # CSV输入配置类
    PipelineInputConfigTypes,  # 输入配置类型
    PipelineTextInputConfig,  # 文本输入配置类
)
from graphrag.index.config.pipeline import (
    PipelineConfig,  # 管道配置类
)
from graphrag.index.config.reporting import (
    PipelineBlobReportingConfig,  # Blob报告配置类
    PipelineConsoleReportingConfig,  # 控制台报告配置类
    PipelineFileReportingConfig,  # 文件报告配置类
    PipelineReportingConfigTypes,  # 报告配置类型
)
from graphrag.index.config.storage import (
    PipelineBlobStorageConfig,  # Blob存储配置类
    PipelineFileStorageConfig,  # 文件存储配置类
    PipelineMemoryStorageConfig,  # 内存存储配置类
    PipelineStorageConfigTypes,  # 存储配置类型
)
from graphrag.index.config.workflow import (
    PipelineWorkflowReference,  # 工作流程引用类
)

# 导入默认的工作流程函数
from graphrag.index.workflows.default_workflows import (
    create_base_documents,  # 创建基础文档
    create_base_entity_graph,  # 创建基础实体图
    create_base_extracted_entities,  # 创建基础提取的实体
    create_base_text_units,  # 创建基础文本单元
    create_final_communities,  # 创建最终社区
    create_final_community_reports,  # 创建最终社区报告
    create_final_covariates,  # 创建最终协变量
    create_final_documents,  # 创建最终文档
    create_final_entities,  # 创建最终实体
    create_final_nodes,  # 创建最终节点
    create_final_relationships,  # 创建最终关系
    create_final_text_units,  # 创建最终文本单元
    create_summarized_entities,  # 创建总结的实体
    join_text_units_to_covariate_ids,  # 将文本单元连接到协变量ID
    join_text_units_to_entity_ids,  # 将文本单元连接到实体ID
    join_text_units_to_relationship_ids,  # 将文本单元连接到关系ID
)

# 设置日志记录器
log = logging.getLogger(__name__)

# 定义一些文本嵌入的名称
entity_name_embedding = "entity.name"  # 实体名称的嵌入
entity_description_embedding = "entity.description"  # 实体描述的嵌入
relationship_description_embedding = "relationship.description"  # 关系描述的嵌入
document_raw_content_embedding = "document.raw_content"  # 文档原始内容的嵌入
community_title_embedding = "community.title"  # 社区标题的嵌入
community_summary_embedding = "community.summary"  # 社区摘要的嵌入
community_full_content_embedding = "community.full_content"  # 社区完整内容的嵌入
text_unit_text_embedding = "text_unit.text"  # 文本单元文本的嵌入

# 定义所有可用的嵌入名称集合
all_embeddings = {
    entity_name_embedding,
    entity_description_embedding,
    relationship_description_embedding,
    document_raw_content_embedding,
    community_title_embedding,
    community_summary_embedding,
    community_full_content_embedding,
    text_unit_text_embedding,
}

# 定义必需的嵌入名称集合
required_embeddings = {entity_description_embedding}

# 定义内置文档属性的集合
builtin_document_attributes = {
    "id",  # ID
    "source",  # 来源
    "text",  # 文本内容
    "title",  # 标题
    "timestamp",  # 时间戳
    "year",  # 年份
    "month",  # 月份
    "day",  # 日期
    "hour",  # 小时
    "minute",  # 分钟
    "second",  # 秒
}

# 定义一个函数create_pipeline_config，它接受一个名为settings的参数，类型为GraphRagConfig，还有一个可选的verbose参数，默认为False
def create_pipeline_config(settings: GraphRagConfig, verbose=False) -> PipelineConfig:
    """这个函数用来获取管道的默认配置"""
    
    # 如果verbose参数为真（即开启详细模式），打印设置信息
    if verbose:
        _log_llm_settings(settings)

    # 确定哪些工作流程应该被跳过
    skip_workflows = _determine_skip_workflows(settings)
    # 获取嵌入字段列表
    embedded_fields = _get_embedded_fields(settings)
    # 判断是否启用协变量（基于设置和是否在skip_workflows中）
    covariates_enabled = (
        settings.claim_extraction.enabled
        and create_final_covariates not in skip_workflows
    )

    # 创建PipelineConfig对象
    result = PipelineConfig(
        # 设置根目录
        root_dir=settings.root_dir,
        # 获取输入配置
        input=_get_pipeline_input_config(settings),
        # 获取报告配置
        reporting=_get_reporting_config(settings),
        # 获取存储配置
        storage=_get_storage_config(settings),
        # 获取缓存配置
        cache=_get_cache_config(settings),
        # 将各种工作流程添加到列表中
        workflows=[
            # 文档工作流程
            *_document_workflows(settings, embedded_fields),
            # 文本单元工作流程
            *_text_unit_workflows(settings, covariates_enabled, embedded_fields),
            # 图形工作流程
            *_graph_workflows(settings, embedded_fields),
            # 社区工作流程
            *_community_workflows(settings, covariates_enabled, embedded_fields),
            # 协变量工作流程（如果启用协变量）
            *(_covariate_workflows(settings) if covariates_enabled else []),
        ],
    )

    # 打印要跳过的工作流程并从列表中移除
    log.info("跳过的工作流程有：%s", ",".join(skip_workflows))
    # 过滤掉在skip_workflows中的工作流程
    result.workflows = [w for w in result.workflows if w.name not in skip_workflows]
    # 返回最终的PipelineConfig对象
    return result

# 定义一个内部辅助函数，用于获取嵌入字段集合，根据settings的嵌入目标来决定
def _get_embedded_fields(settings: GraphRagConfig) -> set[str]:
    # 根据settings的embeddings.target值进行匹配
    match settings.embeddings.target:
        # 如果目标是所有嵌入，返回所有嵌入字段，减去要忽略的字段
        case TextEmbeddingTarget.all:
            return all_embeddings - {*settings.embeddings.skip}
        # 如果目标是必需嵌入，直接返回必需嵌入字段
        case TextEmbeddingTarget.required:
            return required_embeddings
        # 其他情况，抛出错误，因为目标未知
        case _:
            # 构造错误消息
            msg = f"未知的嵌入目标：{settings.embeddings.target}"
            # 抛出值错误
            raise ValueError(msg)

# 定义一个函数_determine_skip_workflows，它接收一个名为settings的参数，这个参数是GraphRagConfig类型
def _determine_skip_workflows(settings: GraphRagConfig) -> list[str]:
    # 从settings中获取skip_workflows列表
    skip_workflows = settings.skip_workflows
    # 检查create_final_covariates是否在skip_workflows中，同时join_text_units_to_covariate_ids不在skip_workflows中
    if (create_final_covariates in skip_workflows and join_text_units_to_covariate_ids not in skip_workflows):
        # 如果条件满足，将join_text_units_to_covariate_ids添加到skip_workflows列表
        skip_workflows.append(join_text_units_to_covariate_ids)
    # 返回更新后的skip_workflows列表
    return skip_workflows

# 定义一个函数_log_llm_settings，它也接收一个名为settings的参数，这个参数同样是GraphRagConfig类型
def _log_llm_settings(settings: GraphRagConfig) -> None:
    # 使用日志模块（log）打印信息，内容是"Using LLM Config"和LLM模型的配置（用json格式化并保留缩进）
    log.info(
        "使用LLM配置：%s",
        json.dumps(
            {**settings.entity_extraction.llm.model_dump(), "api_key": "*****"},
            indent=4,
        ),
    )
    # 同样使用日志模块打印信息，内容是"Using Embeddings Config"和嵌入（Embeddings）模型的配置（同样json格式化并保留缩进）
    log.info(
        "使用嵌入配置：%s",
        json.dumps(
            {**settings.embeddings.llm.model_dump(), "api_key": "*****"}, indent=4
        ),
    )

# 定义一个函数_document_workflows，它接收两个参数：settings（GraphRagConfig类型）和embedded_fields（set类型字符串集合）
def _document_workflows(
    settings: GraphRagConfig, embedded_fields: set[str]
) -> list[PipelineWorkflowReference]:
    # 检查document_raw_content_embedding是否不在embedded_fields中
    skip_document_raw_content_embedding = (document_raw_content_embedding not in embedded_fields)
    # 创建一个PipelineWorkflowReference类型的列表
    return [
        # 列表的第一个元素，包含name为create_base_documents的流程，以及它的配置
        PipelineWorkflowReference(
            name=create_base_documents,
            config={
                "document_attribute_columns": list(
                    {*(settings.input.document_attribute_columns)}
                    - builtin_document_attributes
                )
            },
        ),
        # 列表的第二个元素，包含name为create_final_documents的流程，以及它的配置
        PipelineWorkflowReference(
            name=create_final_documents,
            config={
                "document_raw_content_embed": _get_embedding_settings(
                    settings.embeddings, "document_raw_content"
                ),
                "skip_raw_content_embedding": skip_document_raw_content_embedding,
            },
        ),
    ]

# 定义一个函数，叫_text_unit_workflows，它接受三个参数
# settings: 一个包含图形配置信息的对象
# covariates_enabled: 一个布尔值，表示是否启用协变量
# embedded_fields: 一个包含字符串的集合，表示已嵌入的字段

# 检查"text_unit_text_embedding"是否在embedded_fields集合中，如果不在，则赋值为True，否则赋值为False
skip_text_unit_embedding = text_unit_text_embedding not in embedded_fields

# 创建一个列表，将要执行的工作流程（PipelineWorkflowReference）添加进去
# 这个列表会返回给调用者

# 添加第一个工作流程，创建基础文本单元
list.append(
    PipelineWorkflowReference(
        name=create_base_text_units,  # 工作流程的名字
        config={  # 配置信息
            "chunk_by": settings.chunks.group_by_columns,  # 根据设置中的分块列进行分块
            "text_chunk": {"strategy": settings.chunks.resolved_strategy()},  # 使用设置中的策略处理文本块
        },
    )
)

# 添加第二个工作流程，将文本单元连接到实体ID
list.append(PipelineWorkflowReference(name=join_text_units_to_entity_ids))

# 添加第三个工作流程，将文本单元连接到关系ID
list.append(PipelineWorkflowReference(name=join_text_units_to_relationship_ids))

# 如果协变量启用（covariates_enabled为True），则添加第四个工作流程，否则不添加
if covariates_enabled:
    list.append(PipelineWorkflowReference(name=join_text_units_to_covariate_ids))
else:
    pass  # 不执行任何操作

# 添加最后一个工作流程，创建最终的文本单元
list.append(
    PipelineWorkflowReference(
        name=create_final_text_units,  # 工作流程的名字
        config={  # 配置信息
            "text_unit_text_embed": _get_embedding_settings(  # 获取嵌入设置
                settings.embeddings,  # 设置中的嵌入信息
                "text_unit_text",
            ),
            "covariates_enabled": covariates_enabled,  # 是否启用协变量
            "skip_text_unit_embedding": skip_text_unit_embedding,  # 是否跳过文本单元嵌入
        },
    )
)

# 返回包含所有工作流程的列表
return list

# 定义一个函数，叫做_get_embedding_settings，它接受两个参数：settings（一个TextEmbeddingConfig类型的变量）和embedding_name（一个字符串）
def _get_embedding_settings(settings: TextEmbeddingConfig, embedding_name: str) -> dict:

    # 获取settings中的vector_store部分，这可能包含了关于向量存储的信息
    vector_store_settings = settings.vector_store

    # 如果vector_store_settings没有值，返回一个字典，其中"strategy"键的值是根据settings解析出的默认策略
    if vector_store_settings is None:
        return {"strategy": settings.resolved_strategy()}

    # 如果我们执行到这里，说明settings.vector_store是有定义的，而且针对这个embedding有特定设置
    # settings.vector_store.base包含连接信息，或者可能未定义
    # settings.vector_store.<vector_name>包含这个embedding的特定设置

    # 获取默认策略
    strategy = settings.resolved_strategy()

    # 使用update方法将vector_store_settings添加到默认策略中，这样确保向量存储配置成为策略的一部分，而不是全局配置
    strategy.update({
        "vector_store": vector_store_settings
    })

    # 最后，返回一个字典，包含更新后的策略和embedding的名称
    return {
        "strategy": strategy,
        "embedding_name": embedding_name,
    }

# 定义一个函数 _graph_workflows，它接受两个参数：settings（配置信息）和 embedded_fields（已嵌入的字段集合）
def _graph_workflows(
    settings: GraphRagConfig,  # 图形配置
    embedded_fields: set[str]  # 已嵌入的字段集合
) -> list[PipelineWorkflowReference]:  # 返回值是一个工作流程引用列表

    # 检查 entity_name_embedding 是否在 embedded_fields 中，如果不在，则赋值为 True，否则为 False
    skip_entity_name_embedding = entity_name_embedding not in embedded_fields

    # 同上，检查 entity_description_embedding
    skip_entity_description_embedding = (
        entity_description_embedding not in embedded_fields
    )

    # 同上，检查 relationship_description_embedding
    skip_relationship_description_embedding = (
        relationship_description_embedding not in embedded_fields
    )

    # 创建并返回一个包含多个工作流程引用的工作流程列表
    return [
        # 第一个工作流程：创建基础提取的实体
        PipelineWorkflowReference(
            name=create_base_extracted_entities,  # 工作流程名称
            config={  # 工作流程配置
                "graphml_snapshot": settings.snapshots.graphml,  # 图形ML快照
                "raw_entity_snapshot": settings.snapshots.raw_entities,  # 原始实体快照
                "entity_extract": {  # 实体提取配置
                    **settings.entity_extraction.parallelization.model_dump(),  # 并行化模型信息
                    "async_mode": settings.entity_extraction.async_mode,  # 异步模式
                    "strategy": settings.entity_extraction.resolved_strategy(
                        settings.root_dir, settings.encoding_model
                    ),  # 解析策略
                    "entity_types": settings.entity_extraction.entity_types,  # 实体类型
                },
            },
        ),
        # 第二个工作流程：创建总结的实体
        PipelineWorkflowReference(
            name=create_summarized_entities,  # 工作流程名称
            config={  # 工作流程配置
                "graphml_snapshot": settings.snapshots.graphml,  # 图形ML快照
                "summarize_descriptions": {  # 总结描述配置
                    **settings.summarize_descriptions.parallelization.model_dump(),  # 并行化模型信息
                    "async_mode": settings.summarize_descriptions.async_mode,  # 异步模式
                    "strategy": settings.summarize_descriptions.resolved_strategy(
                        settings.root_dir,
                    ),  # 解析策略
                },
            },
        ),
        # 第三个工作流程：创建基础实体图
        PipelineWorkflowReference(
            name=create_base_entity_graph,  # 工作流程名称
            config={  # 工作流程配置
                "graphml_snapshot": settings.snapshots.graphml,  # 图形ML快照
                "embed_graph_enabled": settings.embed_graph.enabled,  # 是否启用图嵌入
                "cluster_graph": {  # 簇图配置
                    "strategy": settings.cluster_graph.resolved_strategy()
                }, 
                "embed_graph": {"strategy": settings.embed_graph.resolved_strategy()},  # 图嵌入策略
            },
        ),
        # 第四个工作流程：创建最终实体
        PipelineWorkflowReference(
            name=create_final_entities,  # 工作流程名称
            config={  # 工作流程配置
                "entity_name_embed": _get_embedding_settings(  # 实体名称嵌入配置
                    settings.embeddings, "entity_name"
                ),
                "entity_name_description_embed": _get_embedding_settings(  # 实体名称描述嵌入配置
                    settings.embeddings, "entity_name_description"
                ),
                "skip_name_embedding": skip_entity_name_embedding,  # 是否跳过实体名称嵌入
                "skip_description_embedding": skip_entity_description_embedding,  # 是否跳过实体描述嵌入
            },
        ),
        # 第五个工作流程：创建最终关系
        PipelineWorkflowReference(
            name=create_final_relationships,  # 工作流程名称
            config={  # 工作流程配置
                "relationship_description_embed": _get_embedding_settings(  # 关系描述嵌入配置
                    settings.embeddings, "relationship_description"
                ),
                "skip_description_embedding": skip_relationship_description_embedding,  # 是否跳过关系描述嵌入
            },
        ),
        # 第六个工作流程：创建最终节点
        PipelineWorkflowReference(
            name=create_final_nodes,  # 工作流程名称
            config={  # 工作流程配置
                "layout_graph_enabled": settings.umap.enabled,  # 是否启用UMAP布局
                "snapshot_top_level_nodes": settings.snapshots.top_level_nodes,  # 顶级节点快照
            },
        ),
    ]

# 定义一个名为_community_workflows的函数，它接受三个参数：settings、covariates_enabled和embedded_fields
def _community_workflows(
    settings: GraphRagConfig,  # 这是一个配置对象，用来设置图形处理
    covariates_enabled: bool,  # 这是一个布尔值，表示是否启用协变量
    embedded_fields: set[str]  # 这是一个字符串集合，包含已嵌入的字段名
) -> list[PipelineWorkflowReference]:  # 函数返回一个工作流程引用列表

    # 检查community_title_embedding字段是否不在嵌入字段中，如果不在，则设为True
    skip_community_title_embedding = community_title_embedding not in embedded_fields

    # 检查community_summary_embedding字段是否不在嵌入字段中，如果不在，则设为True
    skip_community_summary_embedding = (
        community_summary_embedding not in embedded_fields
    )

    # 检查community_full_content_embedding字段是否不在嵌入字段中，如果不在，则设为True
    skip_community_full_content_embedding = (
        community_full_content_embedding not in embedded_fields
    )

    # 创建并返回一个工作流程引用列表，列表中有两个元素
    return [
        # 第一个元素是创建最终社区的工作流程引用
        PipelineWorkflowReference(name=create_final_communities),

        # 第二个元素是创建最终社区报告的工作流程引用，包含一些配置信息
        PipelineWorkflowReference(
            name=create_final_community_reports,

            # 配置字典
            config={
                "covariates_enabled": covariates_enabled,  # 是否启用协变量
                "skip_title_embedding": skip_community_title_embedding,  # 是否跳过标题嵌入
                "skip_summary_embedding": skip_community_summary_embedding,  # 是否跳过摘要嵌入
                "skip_full_content_embedding": skip_community_full_content_embedding,  # 是否跳过完整内容嵌入
                "create_community_reports": {  # 创建社区报告的设置
                    **settings.community_reports.parallelization.model_dump(),  # 并行化模型的设置
                    "async_mode": settings.community_reports.async_mode,  # 异步模式设置
                    "strategy": settings.community_reports.resolved_strategy(  # 解析后的策略设置
                        settings.root_dir
                    ),
                },
                "community_report_full_content_embed": _get_embedding_settings(  # 社区报告完整内容的嵌入设置
                    settings.embeddings, "community_report_full_content"
                ),
                "community_report_summary_embed": _get_embedding_settings(  # 社区报告摘要的嵌入设置
                    settings.embeddings, "community_report_summary"
                ),
                "community_report_title_embed": _get_embedding_settings(  # 社区报告标题的嵌入设置
                    settings.embeddings, "community_report_title"
                ),
            },
        ),
    ]

# 定义一个名为 "_covariate_workflows" 的函数，它接受一个叫做 "settings" 的参数，这个参数是 GraphRagConfig 类型的
def _covariate_workflows(
    settings: GraphRagConfig,
) -> list[PipelineWorkflowReference]:  # 函数返回值是一个 PipelineWorkflowReference 类型的列表

    # 创建一个空列表，用于存储将要返回的工作流程引用
    return [  # 开始创建列表

        # 创建一个 PipelineWorkflowReference 对象，它代表一个工作流程
        PipelineWorkflowReference(  # 工作流程引用的开始

            # 设置工作流程的名字为 "create_final_covariates"
            name=create_final_covariates,  # 这个名字可能是一个函数或标识符

            # 设置工作流程的配置信息，这是一个字典
            config={  # 开始配置字典

                # 键为 "claim_extract"，对应的值是一个嵌套的字典
                "claim_extract": {  # 关于索赔提取的部分

                    # 使用星号运算符展开 settings.claim_extraction.parallelization.model_dump() 的结果
                    **settings.claim_extraction.parallelization.model_dump(),  # 可能是模型的保存信息

                    # 设置 "strategy"，根据 settings 中的 claim_extraction 和 root_dir 来决定策略
                    "strategy": settings.claim_extraction.resolved_strategy(
                        settings.root_dir
                    ),  # 策略选择可能与项目根目录有关
                },
            },  # 结束配置字典

        )  # 结束 PipelineWorkflowReference 对象

    ]  # 结束列表，现在列表中有一个工作流程引用

# 定义一个函数_get_pipeline_input_config，它接受一个名为settings的参数，这个参数是GraphRagConfig类型的
def _get_pipeline_input_config(
    settings: GraphRagConfig,
) -> PipelineInputConfigTypes:

    # 从settings中获取输入文件的类型（比如是csv还是text）
    file_type = settings.input.file_type

    # 使用Python的match-case结构，根据file_type的值执行不同的代码块
    match file_type:
        # 如果file_type是InputFileType.csv（表示CSV文件）
        case InputFileType.csv:
            # 创建并返回一个PipelineCSVInputConfig对象，这个对象包含了处理CSV文件所需的各种配置
            return PipelineCSVInputConfig(
                # 基本目录
                base_dir=settings.input.base_dir,
                # 文件模式，用于匹配文件
                file_pattern=settings.input.file_pattern,
                # 文件编码
                encoding=settings.input.encoding,
                # 源数据列名
                source_column=settings.input.source_column,
                # 时间戳列名
                timestamp_column=settings.input.timestamp_column,
                # 时间戳格式
                timestamp_format=settings.input.timestamp_format,
                # 文本内容列名
                text_column=settings.input.text_column,
                # 标题列名
                title_column=settings.input.title_column,
                # 输入类型
                type=settings.input.type,
                # 数据库连接字符串
                connection_string=settings.input.connection_string,
                # 存储账户的blob URL
                storage_account_blob_url=settings.input.storage_account_blob_url,
                # 存储容器名称
                container_name=settings.input.container_name,
            )
        # 如果file_type是InputFileType.text（表示纯文本文件）
        case InputFileType.text:
            # 创建并返回一个PipelineTextInputConfig对象，这个对象包含了处理文本文件所需的各种配置
            return PipelineTextInputConfig(
                # 基本目录
                base_dir=settings.input.base_dir,
                # 文件模式，用于匹配文件
                file_pattern=settings.input.file_pattern,
                # 文件编码
                encoding=settings.input.encoding,
                # 输入类型
                type=settings.input.type,
                # 数据库连接字符串
                connection_string=settings.input.connection_string,
                # 存储账户的blob URL
                storage_account_blob_url=settings.input.storage_account_blob_url,
                # 存储容器名称
                container_name=settings.input.container_name,
            )
        # 如果file_type既不是CSV也不是文本，那么抛出一个错误
        case _:
            # 构造一个错误消息，说明未知的输入类型
            msg = f"Unknown input type: {file_type}"
            # 抛出一个ValueError，附带错误消息
            raise ValueError(msg)

# 定义一个函数，叫做_get_reporting_config，它接收一个名为settings的参数，这个参数类型是GraphRagConfig
def _get_reporting_config(
    settings: GraphRagConfig,
) -> PipelineReportingConfigTypes:
    """从settings中获取报告配置信息。"""
    
    # 检查settings中的reporting.type是什么类型
    match settings.reporting.type:
        # 如果是ReportingType.file类型
        case ReportingType.file:
            # 返回一个基于文件的报告配置，其中base_dir是相对于根目录的路径
            return PipelineFileReportingConfig(base_dir=settings.reporting.base_dir)

        # 如果是ReportingType.blob类型
        case ReportingType.blob:
            # 获取连接字符串和存储账户的blob URL
            connection_string = settings.reporting.connection_string
            storage_account_blob_url = settings.reporting.storage_account_blob_url
            container_name = settings.reporting.container_name
            
            # 如果没有提供容器名称，抛出一个错误
            if container_name is None:
                msg = "对于blob报告，必须提供容器名称。"
                raise ValueError(msg)
            
            # 如果没有提供连接字符串和存储账户的blob URL，抛出一个错误
            if connection_string is None and storage_account_blob_url is None:
                msg = "对于blob报告，必须提供连接字符串或存储账户的blob URL。"
                raise ValueError(msg)
            
            # 返回一个基于blob的报告配置，包括连接字符串、容器名称、base_dir和存储账户的blob URL
            return PipelineBlobReportingConfig(
                connection_string=connection_string,
                container_name=container_name,
                base_dir=settings.reporting.base_dir,
                storage_account_blob_url=storage_account_blob_url,
            )

        # 如果是ReportingType.console类型
        case ReportingType.console:
            # 返回一个基于控制台的报告配置
            return PipelineConsoleReportingConfig()

        # 如果是其他未知类型
        case _:
            # 默认情况下，返回一个基于文件的报告配置，其中base_dir是相对于根目录的路径
            return PipelineFileReportingConfig(base_dir=settings.reporting.base_dir)

# 定义一个名为_get_storage_config的函数，它接受一个GraphRagConfig类型的参数settings
def _get_storage_config(
    settings: GraphRagConfig,
) -> PipelineStorageConfigTypes:
    """从设置中获取存储类型."""
    # 获取settings中的根目录
    root_dir = settings.root_dir

    # 根据settings.storage.type的值进行匹配
    match settings.storage.type:
        # 如果是内存存储类型
        case StorageType.memory:
            # 返回一个PipelineMemoryStorageConfig对象
            return PipelineMemoryStorageConfig()

        # 如果是文件存储类型
        case StorageType.file:
            # 获取相对于根目录的基础目录
            base_dir = settings.storage.base_dir
            # 如果基础目录未提供，抛出错误
            if base_dir is None:
                msg = "文件存储必须提供基础目录。"
                raise ValueError(msg)
            # 返回一个PipelineFileStorageConfig对象，基础目录用Path(root_dir) / base_dir计算
            return PipelineFileStorageConfig(base_dir=str(Path(root_dir) / base_dir))

        # 如果是云存储（blob）类型
        case StorageType.blob:
            # 获取连接字符串
            connection_string = settings.storage.connection_string
            # 获取存储账户的blob URL
            storage_account_blob_url = settings.storage.storage_account_blob_url
            # 获取容器名称
            container_name = settings.storage.container_name
            # 如果容器名称未提供，抛出错误
            if container_name is None:
                msg = "blob存储必须提供容器名称。"
                raise ValueError(msg)
            # 如果连接字符串和存储账户blob URL都未提供，抛出错误
            if connection_string is None and storage_account_blob_url is None:
                msg = "blob存储必须提供连接字符串或存储账户blob URL。"
                raise ValueError(msg)
            # 返回一个PipelineBlobStorageConfig对象，包含连接字符串、容器名称和基础目录
            return PipelineBlobStorageConfig(
                connection_string=connection_string,
                container_name=container_name,
                base_dir=settings.storage.base_dir,
                storage_account_blob_url=storage_account_blob_url,
            )

        # 如果设置的存储类型既不是内存也不是文件也不是云存储
        case _:
            # 使用与文件存储相同的方式处理，因为没有其他选择
            base_dir = settings.storage.base_dir
            # 如果基础目录未提供，抛出错误
            if base_dir is None:
                msg = "文件存储必须提供基础目录。"
                raise ValueError(msg)
            # 返回一个PipelineFileStorageConfig对象，基础目录用Path(root_dir) / base_dir计算
            return PipelineFileStorageConfig(base_dir=str(Path(root_dir) / base_dir))

# 定义一个名为_get_cache_config的函数，它接受一个名为settings的参数，类型为GraphRagConfig
def _get_cache_config(
    settings: GraphRagConfig,
) -> PipelineCacheConfigTypes:
    """这个函数的作用是从settings中获取缓存类型信息"""
    
    # 检查settings.cache.type的值
    match settings.cache.type:
        # 如果类型是'memory'，返回一个PipelineMemoryCacheConfig对象
        case CacheType.memory:
            return PipelineMemoryCacheConfig()

        # 如果类型是'file'，返回一个PipelineFileCacheConfig对象
        # 其中的base_dir属性设置为settings.cache.base_dir
        case CacheType.file:
            return PipelineFileCacheConfig(base_dir=settings.cache.base_dir)

        # 如果类型是'none'，返回一个PipelineNoneCacheConfig对象
        case CacheType.none:
            return PipelineNoneCacheConfig()

        # 如果类型是'blob'
        case CacheType.blob:
            # 获取connection_string、storage_account_blob_url和container_name
            connection_string = settings.cache.connection_string
            storage_account_blob_url = settings.cache.storage_account_blob_url
            container_name = settings.cache.container_name

            # 如果container_name没有提供，抛出一个错误
            if container_name is None:
                msg = "对于blob缓存，必须提供容器名称。"
                raise ValueError(msg)

            # 如果connection_string和storage_account_blob_url都没有提供，抛出一个错误
            if connection_string is None and storage_account_blob_url is None:
                msg = "对于blob缓存，必须提供连接字符串或存储帐户blob URL。"
                raise ValueError(msg)

            # 创建并返回一个PipelineBlobCacheConfig对象
            # 使用提供的connection_string、container_name、base_dir和storage_account_blob_url
            return PipelineBlobCacheConfig(
                connection_string=connection_string,
                container_name=container_name,
                base_dir=settings.cache.base_dir,
                storage_account_blob_url=storage_account_blob_url,
            )

        # 如果上面所有情况都不匹配，返回一个默认的PipelineFileCacheConfig对象
        # 其中的base_dir属性设置为当前目录下的'cache'子目录
        case _:
            return PipelineFileCacheConfig(base_dir="./cache")

