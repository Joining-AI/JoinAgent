# 导入一个叫做networkx的库，它用于处理图形数据
import networkx as nx

# 导入一个叫做VerbCallbacks的类，可能用于报告或处理操作
from datashaper import VerbCallbacks

# 导入默认配置
from graphrag.config.defaults import defs

# 从枚举类型中导入LLMType，这可能是语言模型的类型
from graphrag.config.enums import LLMType

# 导入缓存类，用于存储处理过程中的数据
from graphrag.index.cache import PipelineCache

# 导入一个用于从图中提取信息的类
from graphrag.index.graph.extractors.graph import GraphExtractor

# 从语言模型模块导入加载语言模型的函数
from graphrag.index.llm import load_llm

# 导入不同类型的文本分割器
from graphrag.index.text_splitting import (
    NoopTextSplitter,  # 不做任何处理的文本分割器
    TextSplitter,  # 基本的文本分割器
    TokenTextSplitter,  # 根据单词进行文本分割的器
)

# 导入与实体提取相关的类型定义
from graphrag.index.verbs.entities.extraction.strategies.typing import (
    Document,  # 文档类
    EntityExtractionResult,  # 实体提取结果类
    EntityTypes,  # 实体类型的枚举
    StrategyConfig,  # 策略配置类
)

# 导入完成型语言模型
from graphrag.llm import CompletionLLM

# 导入默认的语言模型配置
from .defaults import DEFAULT_LLM_CONFIG

# 版权声明和许可信息

# 这个模块包含运行图智能的方法
# 注意：'.' 表示当前目录下的文件

# 定义一个异步函数run_gi，用于执行图智能实体提取策略
async def run_gi(
    # 输入参数列表：
    # - docs：一个文档列表
    docs: list[Document],
    # - entity_types：需要提取的实体类型
    entity_types: EntityTypes,
    # - reporter：用于报告进度或结果的对象
    reporter: VerbCallbacks,
    # - pipeline_cache：处理过程中的数据缓存
    pipeline_cache: PipelineCache,
    # - args：配置参数
    args: StrategyConfig,
) -> EntityExtractionResult:
    # 从配置中获取语言模型配置，如果没有则使用默认配置
    llm_config = args.get("llm", DEFAULT_LLM_CONFIG)
    # 获取语言模型的类型
    llm_type = llm_config.get("type", LLMType.StaticResponse)
    # 加载对应类型的语言模型
    llm = load_llm("entity_extraction", llm_type, reporter, pipeline_cache, llm_config)
    # 调用run_extract_entities函数，使用加载的语言模型处理文档
    # 并返回处理结果
    return await run_extract_entities(llm, docs, entity_types, reporter, args)

# 定义一个异步函数run_extract_entities，它接收几个参数：
# llm：完成语言模型
# docs：文档列表
# entity_types：实体类型
# reporter：用于报告错误的回调函数，或None
# args：策略配置

async def run_extract_entities(
    llm: CompletionLLM,
    docs: list[Document],
    entity_types: EntityTypes,
    reporter: VerbCallbacks | None,
    args: StrategyConfig,
) -> EntityExtractionResult:
    """运行实体提取流程"""
    
    # 获取编码器名称，如果args中没有，则默认为"cl100k_base"
    encoding_name = args.get("encoding_name", "cl100k_base")

    # 分块参数设置
    prechunked = args.get("prechunked", False)  # 是否已预先分块
    chunk_size = args.get("chunk_size", defs.CHUNK_SIZE)  # 每个分块的大小
    chunk_overlap = args.get("chunk_overlap", defs.CHUNK_OVERLAP)  # 分块之间的重叠量

    # 提取参数设置
    tuple_delimiter = args.get("tuple_delimiter", None)  # 元组分隔符
    record_delimiter = args.get("record_delimiter", None)  # 记录分隔符
    completion_delimiter = args.get("completion_delimiter", None)  # 完成分隔符
    extraction_prompt = args.get("extraction_prompt", None)  # 提取提示
    encoding_model = args.get("encoding_name", None)  # 编码模型
    max_gleanings = args.get("max_gleanings", defs.ENTITY_EXTRACTION_MAX_GLEANINGS)  # 最大提取数量

    # 创建文本分割器，根据预分块、分块大小和重叠量
    text_splitter = _create_text_splitter(
        prechunked, chunk_size, chunk_overlap, encoding_name
    )

    # 创建实体提取器，使用语言模型、提取提示、编码模型和最大提取数量
    extractor = GraphExtractor(
        llm_invoker=llm,
        prompt=extraction_prompt,
        encoding_model=encoding_model,
        max_gleanings=max_gleanings,
        on_error=lambda e, s, d: (
            reporter.error("实体提取错误", e, s, d) if reporter else None
        ),
    )

    # 将文档列表中的文本整理成一个只包含文本的列表
    text_list = [doc.text.strip() for doc in docs]

    # 如果没有预分块，就对输入文本进行分块
    if not prechunked:
        text_list = text_splitter.split_text("\n".join(text_list))

    # 使用提取器处理文本列表并获取结果
    results = await extractor(
        list(text_list),
        {
            "entity_types": entity_types,
            "tuple_delimiter": tuple_delimiter,
            "record_delimiter": record_delimiter,
            "completion_delimiter": completion_delimiter,
        },
    )

    # 获取结果中的图结构
    graph = results.output

    # 将"source_id"字段映射回"文档id"
    for _, node in graph.nodes(data=True):  # type: ignore
        if node is not None:
            node["source_id"] = ",".join(
                docs[int(id)].id for id in node["source_id"].split(",")
            )

    # 同样处理边的"source_id"
    for _, _, edge in graph.edges(data=True):  # type: ignore
        if edge is not None:
            edge["source_id"] = ",".join(
                docs[int(id)].id for id in edge["source_id"].split(",")
            )

    # 将图中的节点转换为实体列表
    entities = [
        ({"name": item[0], **(item[1] or {})})  # item[1]可能是None，用**展开字典
        for item in graph.nodes(data=True)
        if item is not None
    ]

    # 生成并连接图的GraphML格式数据
    graph_data = "".join(nx.generate_graphml(graph))

    # 返回实体列表和图数据
    return EntityExtractionResult(entities, graph_data)

# 定义一个名为_create_text_splitter的函数，它有四个参数
def _create_text_splitter(
    # 参数1：prechunked，表示文本是否已经分块
    prechunked: bool, 
    # 参数2：chunk_size，每个分块的大小
    chunk_size: int, 
    # 参数3：chunk_overlap，分块之间的重叠部分
    chunk_overlap: int, 
    # 参数4：encoding_name，使用的编码名称
    encoding_name: str
) -> TextSplitter:
    """创建一个用于提取链的文本分割器。

    参数说明：
        - prechunked - 文本是否已经预先分块
        - chunk_size - 每个分块的字节数
        - chunk_overlap - 分块之间重叠的字节数
        - encoding_name - 使用的文本编码方式

    返回值：
        - 一个文本分割器对象
    """
    # 如果文本已经分块
    if prechunked:
        # 直接返回NoopTextSplitter，这是一个不做任何操作的分割器
        return NoopTextSplitter()
    
    # 否则，返回TokenTextSplitter，这是处理未分块文本的分割器
    # 并传入chunk_size、chunk_overlap和encoding_name作为参数
    return TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        encoding_name=encoding_name,
    )

