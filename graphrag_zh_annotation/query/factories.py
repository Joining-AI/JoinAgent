# 导入一个叫做tiktoken的库，它可能用来处理某种令牌或认证
import tiktoken

# 从azure.identity库中导入两个东西：DefaultAzureCredential和get_bearer_token_provider
# 这些是Azure云服务的身份验证工具
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# 导入GraphRagConfig和LLMType这两个类，它们来自graphrag.config模块
from graphrag.config import GraphRagConfig, LLMType

# 导入一系列与模型相关的类：CommunityReport、Covariate、Entity、Relationship和TextUnit
from graphrag.model import CommunityReport, Covariate, Entity, Relationship, TextUnit

# 从context_builder的entity_extraction子模块中导入EntityVectorStoreKey类
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey

# 导入与OpenAI聊天相关的ChatOpenAI类和OpenAI嵌入向量相关的OpenAIEmbedding类
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.embedding import OpenAIEmbedding

# 导入OpenAI API的类型枚举OpenaiApiType
from graphrag.query.llm.oai.typing import OpenaiApiType

# 导入全局社区上下文类GlobalCommunityContext
from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext

# 导入全局搜索类GlobalSearch
from graphrag.query.structured_search.global_search.search import GlobalSearch

# 导入混合本地搜索上下文类LocalSearchMixedContext
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext

# 导入本地搜索类LocalSearch
from graphrag.query.structured_search.local_search.search import LocalSearch

# 导入基类向量存储库BaseVectorStore
from graphrag.vector_stores import BaseVectorStore

# 这一行是版权信息，表示代码由微软公司拥有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是文档说明，说明这些代码是用来创建查询工厂方法以支持命令行界面的
# "Query Factory methods to support CLI."

# 定义一个名为get_llm的函数，它需要一个名为config的参数，这个参数类型是GraphRagConfig
def get_llm(config: GraphRagConfig) -> ChatOpenAI:

    # 检查config中的llm.type是否为AzureOpenAIChat或AzureOpenAI
    is_azure_client = (
        config.llm.type == LLMType.AzureOpenAIChat
        or config.llm.type == LLMType.AzureOpenAI
    )

    # 获取或设置一个空字符串作为debug_llm_key
    debug_llm_key = config.llm.api_key or ""

    # 创建一个字典llm_debug_info，包含config.llm的一些信息，并用REDACTED替换真实的api_key，只显示长度
    llm_debug_info = {
        **config.llm.model_dump(),
        "api_key": f"REDACTED,len={len(debug_llm_key)}",
    }

    # 如果config.llm.cognitive_services_endpoint没有设置，那么设置默认值
    if config.llm.cognitive_services_endpoint is None:
        cognitive_services_endpoint = "https://cognitiveservices.azure.com/.default"
    else:
        cognitive_services_endpoint = config.llm.cognitive_services_endpoint

    # 打印一条消息，显示正在创建llm客户端和一些调试信息
    print(f"creating llm client with {llm_debug_info}")  # noqa T201

    # 返回一个ChatOpenAI对象，传入相关的配置参数
    return ChatOpenAI(
        # 使用config.llm.api_key作为api_key
        api_key=config.llm.api_key,

        # 如果是Azure客户端且没有api_key，获取azure_ad_token_provider，否则设为None
        azure_ad_token_provider=(
            get_bearer_token_provider(
                DefaultAzureCredential(), cognitive_services_endpoint
            )
            if is_azure_client and not config.llm.api_key
            else None
        ),

        # 使用config.llm.api_base作为api基础路径
        api_base=config.llm.api_base,

        # 使用config.llm.model作为模型
        model=config.llm.model,

        # 根据is_azure_client的值，设置api类型为AzureOpenAI或OpenAI
        api_type=OpenaiApiType.AzureOpenAI if is_azure_client else OpenaiApiType.OpenAI,

        # 使用config.llm.deployment_name作为部署名称
        deployment_name=config.llm.deployment_name,

        # 使用config.llm.api_version作为API版本
        api_version=config.llm.api_version,

        # 使用config.llm.max_retries作为最大重试次数
        max_retries=config.llm.max_retries,
    )

# 定义一个函数get_text_embedder，它接收一个名为config的参数，这个参数是GraphRagConfig类型的
def get_text_embedder(config: GraphRagConfig) -> OpenAIEmbedding:
    # 检查config中的embeddings.llm.type是否等于LLMType.AzureOpenAIEmbedding
    is_azure_client = config.embeddings.llm.type == LLMType.AzureOpenAIEmbedding

    # 获取或设置一个空字符串作为debug_embedding_api_key
    debug_embedding_api_key = config.embeddings.llm.api_key or ""

    # 创建一个字典llm_debug_info，包含config中关于模型的信息，并用"REDACTED,len=长度"替换真实的api_key
    llm_debug_info = {
        **config.embeddings.llm.model_dump(),
        "api_key": f"REDACTED,len={len(debug_embedding_api_key)}",
    }

    # 如果config中没有设置cognitive_services_endpoint，就给它一个默认值
    if config.embeddings.llm.cognitive_services_endpoint is None:
        cognitive_services_endpoint = "https://cognitiveservices.azure.com/.default"
    else:
        cognitive_services_endpoint = config.embeddings.llm.cognitive_services_endpoint

    # 打印一条信息，说明正在创建一个用于嵌入的LLM客户端，但隐藏了真实的api_key（为了安全）
    print(f"creating embedding llm client with {llm_debug_info}")  # noqa T201

    # 返回一个OpenAIEmbedding对象，根据之前检查的is_azure_client和其他配置信息来初始化
    return OpenAIEmbedding(
        # 设置api_key
        api_key=config.embeddings.llm.api_key,
        # 如果是Azure客户端且没有api_key，创建一个令牌提供器，否则设为None
        azure_ad_token_provider=(
            get_bearer_token_provider(
                DefaultAzureCredential(), cognitive_services_endpoint
            )
            if is_azure_client and not config.embeddings.llm.api_key
            else None
        ),
        # 设置api的基础地址
        api_base=config.embeddings.llm.api_base,
        # 根据is_azure_client设置API类型
        api_type=OpenaiApiType.AzureOpenAI if is_azure_client else OpenaiApiType.OpenAI,
        # 设置模型
        model=config.embeddings.llm.model,
        # 设置部署名称
        deployment_name=config.embeddings.llm.deployment_name,
        # 设置API版本
        api_version=config.embeddings.llm.api_version,
        # 设置最大重试次数
        max_retries=config.embeddings.llm.max_retries,
    )

# 定义一个函数，叫get_local_search_engine，它需要一些参数来创建一个本地搜索引擎
def get_local_search_engine(
    config: GraphRagConfig,       # 这是一个配置对象，包含有关如何运行搜索的信息
    reports: list[CommunityReport],  # 这是一个社区报告列表，可能包含了社区的信息
    text_units: list[TextUnit],     # 这是一个文本单元列表，可能是文章或句子
    entities: list[Entity],         # 这是一个实体列表，比如人、地点、事物
    relationships: list[Relationship],  # 这是一个关系列表，描述了实体之间的联系
    covariates: dict[str, list[Covariate]],  # 这是一个字典，存储了变量和它们的值
    response_type: str,             # 搜索结果的类型，比如文本、图像等
    description_embedding_store: BaseVectorStore,  # 这是一个存储实体描述向量的地方
) -> LocalSearch:
    """这个函数用来根据数据和配置创建一个本地搜索引擎"""

    # 获取语言模型，它能理解并生成文本
    llm = get_llm(config)

    # 获取文本嵌入器，将文本转化为数字向量
    text_embedder = get_text_embedder(config)

    # 获取一个工具，用于将文本编码成模型可以理解的形式
    token_encoder = tiktoken.get_encoding(config.encoding_model)

    # 从配置中获取本地搜索的相关设置
    ls_config = config.local_search

    # 创建本地搜索引擎，给它提供所需的组件和设置
    return LocalSearch(
        llm=llm,                          # 用上面获取的语言模型
        context_builder=LocalSearchMixedContext(
            community_reports=reports,      # 提供社区报告
            text_units=text_units,           # 提供文本单元
            entities=entities,               # 提供实体信息
            relationships=relationships,     # 提供关系信息
            covariates=covariates,           # 提供变量信息
            entity_text_embeddings=description_embedding_store,  # 使用描述向量存储
            embedding_vectorstore_key=EntityVectorStoreKey.ID,   # 使用ID作为向量的标识
            text_embedder=text_embedder,     # 使用文本嵌入器
            token_encoder=token_encoder,     # 使用文本编码器
        ),
        token_encoder=token_encoder,       # 再次提供文本编码器，可能在其他地方也需要
        llm_params={                       # 设置语言模型的参数
            "max_tokens": ls_config.llm_max_tokens,  # 设置最大处理的令牌数
            "temperature": 0.0,             # 温度设为0，生成确定性结果
        },
        context_builder_params={          # 设置上下文构建器的参数
            "text_unit_prop": ls_config.text_unit_prop,  # 文本单元的比例
            "community_prop": ls_config.community_prop,  # 社区信息的比例
            "conversation_history_max_turns": ls_config.conversation_history_max_turns,  # 对话历史的最大回合数
            "conversation_history_user_turns_only": True,  # 只考虑用户的对话回合
            "top_k_mapped_entities": ls_config.top_k_entities,  # 选择的顶级实体数量
            "top_k_relationships": ls_config.top_k_relationships,  # 选择的顶级关系数量
            "include_entity_rank": True,    # 包含实体的排名
            "include_relationship_weight": True,  # 包含关系的权重
            "include_community_rank": False,   # 不包含社区的排名
            "return_candidate_context": False,  # 不返回候选上下文
            "embedding_vectorstore_key": EntityVectorStoreKey.ID,  # 用ID作为向量的标识
            "max_tokens": ls_config.max_tokens,  # 根据模型限制设置最大令牌数
        },
        response_type=response_type,       # 用给定的响应类型
    )

# 定义一个名为get_global_search_engine的函数，它需要四个参数
def get_global_search_engine(
    # config: 这是一个配置对象，用于获取相关设置
    config: GraphRagConfig,
    # reports: 这是一个包含社区报告的列表
    reports: list[CommunityReport],
    # entities: 这是一个实体（比如人、地点、事物）的列表
    entities: list[Entity],
    # response_type: 这是一个字符串，决定返回结果的类型
    response_type: str,
):
    """这个函数会根据数据和配置创建一个全局搜索引擎"""
    
    # 使用tiktoken库获取编码模型
    token_encoder = tiktoken.get_encoding(config.encoding_model)
    
    # 从config中获取全局搜索的相关设置
    gs_config = config.global_search
    
    # 创建一个全局搜索对象
    return GlobalSearch(
        # 获取低层语言模型（LLM）
        llm=get_llm(config),
        
        # 创建全局社区上下文，用到前面的报告、实体和编码器
        context_builder=GlobalCommunityContext(
            community_reports=reports, 
            entities=entities, 
            token_encoder=token_encoder
        ),
        
        # 继续设置编码器
        token_encoder=token_encoder,
        
        # 设置数据最大令牌数
        max_data_tokens=gs_config.data_max_tokens,
        
        # 设置地图LLM参数
        map_llm_params={
            "max_tokens": gs_config.map_max_tokens,
            "temperature": gs_config.temperature,
            "top_p": gs_config.top_p,
            "n": gs_config.n,
        },
        
        # 设置减少LLM参数
        reduce_llm_params={
            "max_tokens": gs_config.reduce_max_tokens,
            "temperature": gs_config.temperature,
            "top_p": gs_config.top_p,
            "n": gs_config.n,
        },
        
        # 不允许使用一般知识
        allow_general_knowledge=False,
        
        # 不使用JSON模式
        json_mode=False,
        
        # 设置上下文构建器参数
        context_builder_params={
            "use_community_summary": False,
            "shuffle_data": True,
            "include_community_rank": True,
            "min_community_rank": 0,
            "community_rank_name": "rank",
            "include_community_weight": True,
            "community_weight_name": "occurrence weight",
            "normalize_community_weight": True,
            "max_tokens": gs_config.max_tokens,
            "context_name": "Reports",
        },
        
        # 设置并发协程数
        concurrent_coroutines=gs_config.concurrency,
        
        # 设置响应类型
        response_type=response_type,
    )

