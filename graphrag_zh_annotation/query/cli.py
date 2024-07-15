# 导入操作系统模块，用于文件和目录操作
import os

# 导入Path模块，方便处理文件路径
from pathlib import Path

# 引入类型提示模块，用于更好地定义变量类型
from typing import cast

# 导入pandas库，用于数据处理
import pandas as pd

# 从graphrag的配置模块导入类
from graphrag.config import GraphRagConfig, create_graphrag_config

# 导入进度报告器，显示查询过程中的进度
from graphrag.index.progress import PrintProgressReporter

# 从graphrag的查询输入加载器中导入一个函数，用于存储实体的语义嵌入
from graphrag.query.input.loaders.dfs import store_entity_semantic_embeddings

# 从graphrag的向量存储模块导入工厂和类型
from graphrag.vector_stores import VectorStoreFactory, VectorStoreType

# 导入自定义的工厂方法，用于获取全局和本地搜索引擎
from .factories import get_global_search_engine, get_local_search_engine

# 导入索引适配器，用于读取索引器的各种信息
from .indexer_adapters import (
    read_indexer_covariates,
    read_indexer_entities,
    read_indexer_relationships,
    read_indexer_reports,
    read_indexer_text_units,
)

# 这是一个许可声明，表明代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义这个脚本的文档字符串，描述这是查询模块的命令行接口
__doc__ = """Command line interface for the query module."""

# 创建一个进度报告器实例，用于打印进度信息
reporter = PrintProgressReporter("")

# 定义一个函数，获取嵌入向量描述存储
def __get_embedding_description_store(vector_store_type, config_args=None):
    """获取用于存储向量描述的商店（数据库）"""
    # 如果没有提供配置参数，就创建一个空字典
    if not config_args:
        config_args = {}

    # 更新配置参数，设置集合名称（数据库中的表名）
    config_args["collection_name"] = config_args.get(
        "query_collection_name",  # 尝试从这里获取集合名
        config_args.get("collection_name", "description_embedding"),  # 或者从这里，如果都没有就用默认的"描述嵌入"
    )

    # 根据给定的类型创建向量存储对象
    description_embedding_store = VectorStoreFactory.get_vector_store(
        vector_store_type, kwargs=config_args
    )

    # 连接向量存储
    description_embedding_store.connect(**config_args)  # 使用配置参数连接
    # 返回这个存储对象
    return description_embedding_store

# 定义一个函数，运行全局搜索
def run_global_search(data_dir, root_dir, community_level, response_type, query):
    """使用给定的查询执行全局搜索"""
    # 配置路径和设置，返回数据目录、根目录和配置信息
    data_dir, root_dir, config = _configure_paths_and_settings(data_dir, root_dir)
    # 创建一个Path对象，方便操作文件路径
    data_path = Path(data_dir)

    # 读取并存储最终节点数据
    final_nodes = pd.read_parquet(data_path / "create_final_nodes.parquet")
    # 读取并存储最终实体数据
    final_entities = pd.read_parquet(data_path / "create_final_entities.parquet")
    # 读取并存储最终社区报告数据
    final_community_reports = pd.read_parquet(
        data_path / "create_final_community_reports.parquet"
    )

    # 处理社区报告数据
    reports = read_indexer_reports(final_community_reports, final_nodes, community_level)
    # 处理节点和实体数据
    entities = read_indexer_entities(final_nodes, final_entities, community_level)
    # 获取全局搜索引擎
    search_engine = get_global_search_engine(config, reports, entities, response_type)

    # 执行搜索
    result = search_engine.search(query=query)

    # 打印成功的消息和搜索结果
    reporter.success(f"全局搜索响应：{result.response}")
    # 返回搜索结果
    return result.response

# 定义一个名为run_local_search的函数，它接受5个参数
def run_local_search(
    data_dir: str | None,  # 数据目录，可以是字符串或None
    root_dir: str | None,  # 根目录，也可以是字符串或None
    community_level: int,  # 社区级别，一个整数
    response_type: str,  # 响应类型，一个字符串
    query: str,  # 查询内容，一个字符串
):
    """这个函数用来执行一个基于给定查询的本地搜索。"""
    
    # 配置路径和设置，返回data_dir, root_dir和config
    data_dir, root_dir, config = _configure_paths_and_settings(data_dir, root_dir)
    # 创建一个Path对象，用于后续操作
    data_path = Path(data_dir)

    # 从parquet文件中加载最终节点数据到DataFrame
    final_nodes = pd.read_parquet(data_path / "create_final_nodes.parquet")
    
    # 加载最终社区报告数据到DataFrame
    final_community_reports = pd.read_parquet(
        data_path / "create_final_community_reports.parquet"
    )
    
    # 加载最终文本单元数据到DataFrame
    final_text_units = pd.read_parquet(data_path / "create_final_text_units.parquet")
    
    # 加载最终关系数据到DataFrame
    final_relationships = pd.read_parquet(
        data_path / "create_final_relationships.parquet"
    )
    
    # 再次加载最终节点数据（可能是重复的）
    final_nodes = pd.read_parquet(data_path / "create_final_nodes.parquet")
    
    # 加载最终实体数据到DataFrame
    final_entities = pd.read_parquet(data_path / "create_final_entities.parquet")
    
    # 读取最终协变量路径，如果存在则加载到DataFrame，否则设为None
    final_covariates_path = data_path / "create_final_covariates.parquet"
    final_covariates = (
        pd.read_parquet(final_covariates_path)
        if final_covariates_path.exists()
        else None
    )

    # 获取嵌入向量存储的参数，如果没有则为空字典
    vector_store_args = (
        config.embeddings.vector_store if config.embeddings.vector_store else {}
    )
    # 从参数中获取或默认设置向量存储类型
    vector_store_type = vector_store_args.get("type", VectorStoreType.LanceDB)

    # 根据向量存储类型获取描述嵌入存储
    description_embedding_store = __get_embedding_description_store(
        vector_store_type=vector_store_type,
        config_args=vector_store_args,
    )
    
    # 从最终节点和实体数据中读取索引器实体
    entities = read_indexer_entities(final_nodes, final_entities, community_level)
    
    # 将实体的语义嵌入存储到向量存储中
    store_entity_semantic_embeddings(
        entities=entities, vectorstore=description_embedding_store
    )
    
    # 如果有协变量数据，则读取，否则创建一个空列表
    covariates = (
        read_indexer_covariates(final_covariates)
        if final_covariates is not None
        else []
    )

    # 根据配置、报告、文本单元、实体、关系、协变量和嵌入存储创建本地搜索引擎
    search_engine = get_local_search_engine(
        config,
        reports=read_indexer_reports(
            final_community_reports, final_nodes, community_level
        ),
        text_units=read_indexer_text_units(final_text_units),
        entities=entities,
        relationships=read_indexer_relationships(final_relationships),
        covariates={"claims": covariates},
        description_embedding_store=description_embedding_store,
        response_type=response_type,
    )

    # 使用搜索引擎执行查询
    result = search_engine.search(query=query)
    
    # 报告成功并打印搜索响应
    reporter.success(f"Local Search Response: {result.response}")
    
    # 返回搜索响应
    return result.response

# 定义一个函数，用来设置路径和配置
def _configure_paths_and_settings(数据目录: str 或 None, 根目录: str 或 None) -> 元组[str, str 或 None, GraphRagConfig]:
    # 如果两个目录都未提供，抛出错误
    if 数据目录 is None and 根目录 is None:
        错误信息 = "必须提供数据目录或根目录。"
        raise ValueError(错误信息)
    # 如果数据目录未提供，从根目录推断数据目录
    if 数据目录 is None:
        数据目录 = 推断数据目录(根目录转换为str类型)
    # 创建GraphRag配置
    配置 = 创建_graphrag配置(根目录, 数据目录)
    # 返回数据目录、根目录和配置
    return 数据目录, 根目录, 配置

# 定义一个函数，用于根据根目录推断数据目录
def _infer_data_dir(根: str) -> str:
    输出目录 = 路径(根) / "output"
    # 查找最新的"data-run"文件夹
    如果输出目录存在():
        文件夹列表 = 按修改时间降序排序(输出目录列出所有文件夹())
        # 如果有文件夹
        如果 len(文件夹列表) > 0:
            最新文件夹 = 文件夹列表[0]
            # 返回最新文件夹内"artifacts"的绝对路径
            返回 str((最新文件夹 / "artifacts").absolute())
    # 如果无法推断数据目录，抛出错误
    错误信息 = f"无法根据根={根}推断数据目录。"
    raise ValueError(错误信息)

# 定义一个函数，创建GraphRag配置
def _create_graphrag_config(根: str 或 None, 数据目录: str 或 None) -> GraphRagConfig:
    """创建GraphRag配置。"""
    # 读取配置参数并返回配置
    返回 _read_config_parameters(根或数据目录转换为str类型)

# 定义一个函数，从文件或环境变量读取配置参数
def _read_config_parameters(根: str):
    _root = 路径(根)
    # 尝试读取settings.yaml
    设置yaml = _root / "settings.yaml"
    如果设置yaml存在():
        报告器.info(f"从{设置yaml}读取设置")
        with 设置yaml.open("r") as 文件:
            # 导入yaml库
            import yaml
            # 安全加载文件内容
            数据 = yaml.safe_load(文件)
            # 使用数据和根目录创建GraphRag配置并返回
            返回 create_graphrag_config(数据, 根)
    # 如果settings.yaml不存在，尝试读取settings.json
    设置json = _root / "settings.json"
    如果设置json存在():
        报告器.info(f"从{设置json}读取设置")
        with 设置json.open("r") as 文件:
            # 导入json库
            import json
            # 解析文件内容
            数据 = json.loads(文件.read())
            # 使用数据和根目录创建GraphRag配置并返回
            返回 create_graphrag_config(数据, 根)
    # 如果两个文件都不存在，从环境变量读取设置
    报告器.info("从环境变量读取设置")
    # 使用根目录创建GraphRag配置并返回
    返回 create_graphrag_config(根目录=根)

