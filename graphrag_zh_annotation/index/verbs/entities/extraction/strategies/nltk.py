# 导入一个叫做 networkx 的库，它用来创建和操作图
import networkx as nx

# 导入 nltk，这是一个自然语言处理的库，帮助我们理解文本
import nltk

# 从 datashaper 库中导入 VerbCallbacks，可能用来处理动词
from datashaper import VerbCallbacks

# 从 nltk.corpus（nltk 的语料库）中导入 words，这是一个英文单词列表
from nltk.corpus import words

# 从 graphrag.index.cache 中导入 PipelineCache，可能是一个用于存储中间结果的工具
from graphrag.index.cache import PipelineCache

# 从当前模块的 typing 文件中导入一些数据类型定义
from .typing import Document, EntityExtractionResult, EntityTypes, StrategyConfig

# 这一行是版权信息，表示代码归微软公司所有，遵循 MIT 许可证

# 定义一个模块，包含运行方法的定义

# 因为我们可能在多线程环境下运行，而 nltk 不太支持这个，所以我们先加载 nltk 的 words 列表
# 这样可以确保在多线程中不会出现问题
words.ensure_loaded()

# 定义一个异步函数run，这个函数是必要的，因为我们需要异步处理
async def run(  # noqa RUF029 async is required for interface
    # 这里是一个列表，包含许多Document对象，每个对象代表一段文本
    docs: list[Document],
    # 这是一个枚举类型，用于表示实体的种类
    entity_types: EntityTypes,
    # 这个参数用来报告进度和结果，它的名字不推荐，但没关系
    reporter: VerbCallbacks,  # noqa ARG001
    # 用来存储管道执行过程中的缓存信息
    pipeline_cache: PipelineCache,  # noqa ARG001
    # 这是一个配置对象，包含策略相关的设置
    args: StrategyConfig,  # noqa ARG001
) -> EntityExtractionResult:
    """这个函数是用来提取文本中实体的定义。"""
    
    # 创建一个字典来存储找到的实体及其类型
    entity_map = {}
    # 创建一个无向图，用于连接在同一篇文章中出现的实体
    graph = nx.Graph()

    # 遍历每篇文档
    for doc in docs:
        # 初始化一个列表，用于存储当前文档中找到的连接实体
        connected_entities = []
        
        # 使用nltk库处理文本，找出名词短语（可能的实体）
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(doc.text))):
            # 如果chunk有标签（表示它是一个实体）
            if hasattr(chunk, "label"):
                # 获取实体类型并转换为小写
                entity_type = chunk.label().lower()
                # 检查这个类型是否在我们关心的类型列表中
                if entity_type in entity_types:
                    # 将实体名称转为大写并拼接起来
                    name = (" ".join(c[0] for c in chunk)).upper()
                    # 添加到连接实体列表
                    connected_entities.append(name)
                    # 如果这个实体还没添加到字典中
                    if name not in entity_map:
                        # 存储实体类型，并在图中添加一个节点
                        entity_map[name] = entity_type
                        graph.add_node(
                            name, type=entity_type, description=name, source_id=doc.id
                        )

    # 如果在一个文档中找到了两个或更多实体
    if len(connected_entities) > 1:
        # 遍历所有组合，连接这些实体
        for i in range(len(connected_entities)):
            for j in range(i + 1, len(connected_entities)):
                # 描述两个实体之间的关系
                description = f"{connected_entities[i]} -> {connected_entities[j]}"
                # 在图中添加边，表示这两个实体在同一篇文档中出现过
                graph.add_edge(
                    connected_entities[i],
                    connected_entities[j],
                    description=description,
                    source_id=doc.id,
                )

    # 返回一个结果对象，包含提取的实体列表和图形数据
    return EntityExtractionResult(
        # 将实体字典转化为列表返回
        entities=[
            {"type": entity_type, "name": name}
            for name, entity_type in entity_map.items()
        ],
        # 将图转换为GraphML格式的字符串
        graphml_graph="".join(nx.generate_graphml(graph)),
    )

