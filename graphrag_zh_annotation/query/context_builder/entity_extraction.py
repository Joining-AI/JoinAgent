# 导入一个叫做 Enum 的特殊类，它帮助我们创建一组特定的枚举值
from enum import Enum

# 导入一个名为 Entity 和 Relationship 的类，它们可能代表图中的节点和边
from graphrag.model import Entity, Relationship

# 从 graphrag.query.input.retrieval.entities 模块中导入两个函数，用于根据键或名称获取实体
from graphrag.query.input.retrieval.entities import get_entity_by_key, get_entity_by_name

# 导入一个基类 BaseTextEmbedding，它可能与文本嵌入（将文本转换为数字向量）有关
from graphrag.query.llm.base import BaseTextEmbedding

# 导入一个基类 BaseVectorStore，它可能用于存储和检索向量数据
from graphrag.vector_stores import BaseVectorStore

# 这是一个版权声明，告诉我们代码的版权属于微软公司，并遵循 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为 EntityVectorStoreKey 的枚举类，它包含两个字符串成员：ID 和 TITLE
class EntityVectorStoreKey(str, Enum):
    # ID 成员表示在实体嵌入向量存储中使用的“id”作为标识
    ID = "id"
    # TITLE 成员表示使用“title”作为标识
    TITLE = "title"

    # 这是一个静态方法，可以将给定的字符串转换为 EntityVectorStoreKey 对象
    @staticmethod
    def from_string(value: str) -> "EntityVectorStoreKey":
        # 如果字符串是 "id"，返回 EntityVectorStoreKey.ID
        if value == "id":
            return EntityVectorStoreKey.ID
        # 如果字符串是 "title"，返回 EntityVectorStoreKey.TITLE
        if value == "title":
            return EntityVectorStoreKey.TITLE

        # 如果输入的字符串既不是 "id" 也不是 "title"，则抛出一个错误
        msg = f"无效的 EntityVectorStoreKey: {value}"
        # 抛出 ValueError 异常，并附带错误信息
        raise ValueError(msg)

# 定义一个函数，名为map_query_to_entities，接收多个参数
def map_query_to_entities(
    # 输入的查询字符串
    query: str,
    # 基本向量存储，用于文本嵌入
    text_embedding_vectorstore: BaseVectorStore,
    # 基本文本嵌入模型
    text_embedder: BaseTextEmbedding,
    # 所有实体列表
    all_entities: list[Entity],
    # 向量存储中的键类型，默认是ID
    embedding_vectorstore_key: str = EntityVectorStoreKey.ID,
    # 可选包含的实体名字列表，默认为空
    include_entity_names: list[str] | None = None,
    # 可选排除的实体名字列表，默认为空
    exclude_entity_names: list[str] | None = None,
    # 返回结果的数量，默认为10
    k: int = 10,
    # 超采样倍数，用于补偿排除的实体，默认为2
    oversample_scaler: int = 2,
) -> list[Entity]:

    # 如果include_entity_names未设置，则设为空列表
    if include_entity_names is None:
        include_entity_names = []

    # 如果exclude_entity_names未设置，则设为空列表
    if exclude_entity_names is None:
        exclude_entity_names = []

    # 匹配到的实体列表
    matched_entities = []

    # 如果查询字符串不为空
    if query != "":
        # 获取与查询语句语义最相似的实体
        # 考虑到排除的实体，超采样搜索结果
        search_results = text_embedding_vectorstore.similarity_search_by_text(
            # 查询文本
            text=query,
            # 使用text_embedder将文本转换为嵌入向量
            text_embedder=lambda t: text_embedder.embed(t),
            # 搜索结果数量为k的超采样倍数
            k=k * oversample_scaler,
        )

        # 遍历搜索结果
        for result in search_results:
            # 根据key和value从所有实体中找到匹配的实体
            matched = get_entity_by_key(
                entities=all_entities,
                key=embedding_vectorstore_key,
                value=result.document.id,
            )
            # 如果找到匹配的实体，添加到匹配列表
            if matched:
                matched_entities.append(matched)
    else:
        # 如果查询字符串为空，按排名从高到低选取前k个实体
        all_entities.sort(key=lambda x: x.rank if x.rank else 0, reverse=True)
        matched_entities = all_entities[:k]

    # 排除掉exclude_entity_names列表中的实体
    if exclude_entity_names:
        # 过滤匹配到的实体列表
        matched_entities = [
            entity
            for entity in matched_entities
            if entity.title not in exclude_entity_names
        ]

    # 添加include_entity_names列表中的实体
    included_entities = []
    # 遍历要包含的实体名字
    for entity_name in include_entity_names:
        # 从所有实体中找到这些实体并添加到列表
        included_entities.extend(get_entity_by_name(all_entities, entity_name))

    # 返回最终的实体列表（包含强制加入的和匹配到的）
    return included_entities + matched_entities

# 定义一个函数，找到与给定实体最相似的邻居
def find_nearest_neighbors_by_graph_embeddings(
    # 输入参数：实体ID（字符串）
    entity_id: str,
    # 输入参数：图嵌入向量存储库（基类向量存储）
    graph_embedding_vectorstore: BaseVectorStore,
    # 输入参数：所有实体列表（每个都是一个实体对象）
    all_entities: list[Entity],
    # 输入参数：要排除的实体名称列表（可选，默认为None）
    exclude_entity_names: list[str] | None = None,
    # 输入参数：向量存储库中用于标识实体的键（默认为ID）
    embedding_vectorstore_key: str = EntityVectorStoreKey.ID,
    # 输入参数：返回的最近邻数量（默认为10）
    k: int = 10,
    # 输入参数：过采样比例（默认为2）
    oversample_scaler: int = 2,
) -> list[Entity]:
    """通过图嵌入获取相关实体。"""

    # 如果没有提供要排除的实体名称，将其设置为空列表
    if exclude_entity_names is None:
        exclude_entity_names = []

    # 根据输入的实体ID在所有实体中找到对应的实体
    query_entity = get_entity_by_key(
        entities=all_entities, key=embedding_vectorstore_key, value=entity_id
    )

    # 获取该实体的图嵌入向量
    query_embedding = query_entity.graph_embedding if query_entity else None

    # 如果找到了查询实体的图嵌入，进行过采样以补偿要排除的实体
    if query_embedding:
        # 初始化匹配的实体列表
        matched_entities = []

        # 在图嵌入向量存储库中搜索与查询向量最相似的k * oversample_scaler个实体
        search_results = graph_embedding_vectorstore.similarity_search_by_vector(
            query_embedding=query_embedding, k=k * oversample_scaler
        )

        # 遍历搜索结果，将匹配的实体添加到列表中
        for result in search_results:
            matched_entity = get_entity_by_key(
                entities=all_entities,
                key=embedding_vectorstore_key,
                value=result.document.id,
            )
            if matched_entity:
                matched_entities.append(matched_entity)

        # 排除要排除的实体
        if exclude_entity_names:
            # 筛选出不在排除列表中的实体
            matched_entities = [
                entity
                for entity in matched_entities
                if entity.title not in exclude_entity_names
            ]

        # 根据相似度排名对匹配的实体进行降序排序
        matched_entities.sort(key=lambda x: x.rank, reverse=True)

        # 取前k个最相似的实体并返回
        return matched_entities[:k]

    # 如果没有找到查询实体的图嵌入，返回空列表
    return []

# 定义一个函数，叫做 find_nearest_neighbors_by_entity_rank，它帮助我们找到与目标实体相关联的最近邻实体
def find_nearest_neighbors_by_entity_rank(
    # 输入参数：entity_name 是我们要找的实体名字
    entity_name: str,
    # 输入参数：all_entities 是一个列表，包含所有实体
    all_entities: list[Entity],
    # 输入参数：all_relationships 是一个列表，包含所有关系
    all_relationships: list[Relationship],
    # 输入参数：exclude_entity_names 是一个可选列表，用于排除不想包含的实体
    exclude_entity_names: list[str] | None = None,
    # 输入参数：k 是一个可选整数，表示我们想要返回的最近邻数量，默认是10
    k: int | None = 10,
) -> list[Entity]:

    # 如果 exclude_entity_names 未设置，则将其设为空列表
    if exclude_entity_names is None:
        exclude_entity_names = []

    # 找到与目标实体有关的所有关系（作为源或目标）
    entity_relationships = [
        rel
        for rel in all_relationships
        if rel.source == entity_name or rel.target == entity_name
    ]

    # 获取这些关系中的源实体名字集合
    source_entity_names = {rel.source for rel in entity_relationships}

    # 获取这些关系中的目标实体名字集合
    target_entity_names = {rel.target for rel in entity_relationships}

    # 合并源和目标实体名字集合，然后排除不需要的实体
    related_entity_names = (source_entity_names.union(target_entity_names)).difference(
        set(exclude_entity_names)
    )

    # 找到所有与目标实体相关的实体
    top_relations = [
        entity for entity in all_entities if entity.title in related_entity_names
    ]

    # 按照实体的排名进行降序排序
    top_relations.sort(key=lambda x: x.rank if x.rank else 0, reverse=True)

    # 如果 k 设定，返回前 k 个最近邻实体
    if k:
        return top_relations[:k]

    # 如果 k 未设定，返回所有相关实体
    return top_relations

