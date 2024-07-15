# 导入pandas库，它用于处理表格数据
import pandas as pd

# 从graphrag.model导入一些类，它们代表不同的数据结构
from graphrag.model import (
    Community,  # 社区，可能是指文档中的某个主题或群体
    CommunityReport,  # 社区报告，可能是关于社区的分析结果
    Covariate,  # 协变量，统计学中与因变量相关的变量
    Document,  # 文档，比如一篇文章或报告
    Entity,  # 实体，如人、地点或事物
    Relationship,  # 关系，实体之间的联系
    TextUnit,  # 文本单元，可能是句子或段落
)

# 从graphrag.query.input.loaders.utils导入一些辅助函数，用于转换数据类型
from graphrag.query.input.loaders.utils import (
    to_list,  # 转换为列表
    to_optional_dict,  # 可能为空的字典转换
    to_optional_float,  # 可能为空的浮点数转换
    to_optional_int,  # 可能为空的整数转换
    to_optional_list,  # 可能为空的列表转换
    to_optional_str,  # 可能为空的字符串转换
    to_str,  # 转换为字符串
)

# 从graphrag.vector_stores导入两个类，用于存储和处理向量数据
from graphrag.vector_stores import BaseVectorStore, VectorStoreDocument

# 这是一个注释，表示代码的版权信息和许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件的作用是将数据框（DataFrame）里的数据加载到一组数据对象中
# 数据对象可以是社区、报告、文档、实体等

# 定义一个函数read_entities，它接受一个数据框（DataFrame）作为参数
def read_entities(
    # 数据框中的列名，表示实体的ID
    df: pd.DataFrame,
    id_col: str = "id",         # ID列，默认是"id"
    short_id_col: str | None = "short_id",   # 短ID列，默认是"short_id"，可以为空
    title_col: str = "title",    # 标题列，默认是"title"
    type_col: str | None = "type",   # 类型列，默认是"type"，可以为空
    description_col: str | None = "description",  # 描述列，默认是"description"，可以为空
    name_embedding_col: str | None = "name_embedding",  # 名称嵌入列，默认是"name_embedding"，可以为空
    description_embedding_col: str | None = "description_embedding",  # 描述嵌入列，默认是"description_embedding"，可以为空
    graph_embedding_col: str | None = "graph_embedding",  # 图嵌入列，默认是"graph_embedding"，可以为空
    community_col: str | None = "community_ids",  # 社区ID列，默认是"community_ids"，可以为空
    text_unit_ids_col: str | None = "text_unit_ids",  # 文本单元ID列，默认是"text_unit_ids"，可以为空
    document_ids_col: str | None = "document_ids",  # 文档ID列，默认是"document_ids"，可以为空
    rank_col: str | None = "degree",   # 排名列，默认是"degree"，可以为空
    attributes_cols: list[str] | None = None,  # 属性列列表，可以为空
) -> list[Entity]:  # 函数返回值是一个Entity对象的列表

    # 创建一个空列表，用于存储Entity对象
    entities = []

    # 遍历数据框的每一行
    for idx, row in df.iterrows():
        # 创建一个新的Entity对象
        entity = Entity(
            # 将ID列转换为字符串并赋值给Entity对象的id属性
            id=to_str(row, id_col),
            # 如果short_id_col有值，将对应的列转换为可选字符串，否则使用当前行的索引作为id
            short_id=to_optional_str(row, short_id_col) if short_id_col else str(idx),
            # 将标题列转换为字符串并赋值给Entity对象的title属性
            title=to_str(row, title_col),
            # 将类型列转换为可选字符串并赋值给Entity对象的type属性
            type=to_optional_str(row, type_col),
            # 将描述列转换为可选字符串并赋值给Entity对象的description属性
            description=to_optional_str(row, description_col),
            # 将名称嵌入列转换为可选的浮点数列表并赋值给Entity对象的name_embedding属性
            name_embedding=to_optional_list(row, name_embedding_col, item_type=float),
            # 将描述嵌入列转换为可选的浮点数列表并赋值给Entity对象的description_embedding属性
            description_embedding=to_optional_list(
                row, description_embedding_col, item_type=float
            ),
            # 将图嵌入列转换为可选的浮点数列表并赋值给Entity对象的graph_embedding属性
            graph_embedding=to_optional_list(row, graph_embedding_col, item_type=float),
            # 将社区ID列转换为可选的字符串列表并赋值给Entity对象的community_ids属性
            community_ids=to_optional_list(row, community_col, item_type=str),
            # 将文本单元ID列转换为可选的列表并赋值给Entity对象的text_unit_ids属性
            text_unit_ids=to_optional_list(row, text_unit_ids_col),
            # 将文档ID列转换为可选的列表并赋值给Entity对象的document_ids属性
            document_ids=to_optional_list(row, document_ids_col),
            # 将排名列转换为可选的整数并赋值给Entity对象的rank属性
            rank=to_optional_int(row, rank_col),
            # 如果attributes_cols有值，创建一个包含这些列值的字典，否则设置为None
            attributes=(
                {col: row.get(col) for col in attributes_cols} 
                if attributes_cols 
                else None
            ),
        )
        # 将新创建的Entity对象添加到列表中
        entities.append(entity)

    # 返回包含所有Entity对象的列表
    return entities

# 定义一个函数，名为store_entity_semantic_embeddings，它接受两个参数：一个实体列表（entities）和一个向量存储（vectorstore）
def store_entity_semantic_embeddings(entities: list[Entity], vectorstore: BaseVectorStore) -> BaseVectorStore:
    # 这个函数的作用是将实体的语义嵌入（description_embedding）存入向量存储中
    """将实体的语义嵌入存储到向量库中。"""

    # 创建一个新列表，名为documents，用于存储每个实体的相关信息
    documents = [
        # 对于entities列表中的每一个实体（entity）：
        VectorStoreDocument(
            # 创建一个向量存储文档，设置以下属性：
            id=entity.id,  # 设置文档的ID为实体的ID
            text=entity.description,  # 设置文档的文本为实体的描述
            vector=entity.description_embedding,  # 设置文档的向量为实体的描述嵌入
            # 如果实体有额外的属性（attributes），则添加一个字典，包含标题（title）和所有属性，否则只包含标题
            attributes=(
                {"title": entity.title, **entity.attributes} if entity.attributes else {"title": entity.title}
            ),
        )
        # 结束对每个实体的循环
        for entity in entities
    ]

    # 将documents列表中的所有文档加载到vectorstore中
    vectorstore.load_documents(documents=documents)

    # 函数返回更新后的向量存储
    return vectorstore

# 定义另一个函数，名为store_entity_behavior_embeddings，与上一个函数类似，但存储的是行为嵌入（graph_embedding）
def store_entity_behavior_embeddings(entities: list[Entity], vectorstore: BaseVectorStore) -> BaseVectorStore:
    # 这个函数的作用是将实体的行为嵌入（graph_embedding）存入向量存储中
    """将实体的行为嵌入存储到向量库中。"""

    # 创建一个新列表，名为documents，用于存储每个实体的相关信息
    documents = [
        # 对于entities列表中的每一个实体（entity）：
        VectorStoreDocument(
            # 创建一个向量存储文档，设置以下属性：
            id=entity.id,  # 设置文档的ID为实体的ID
            text=entity.description,  # 设置文档的文本为实体的描述
            vector=entity.graph_embedding,  # 设置文档的向量为实体的行为嵌入
            # 如果实体有额外的属性（attributes），则添加一个字典，包含标题（title）和所有属性，否则只包含标题
            attributes=(
                {"title": entity.title, **entity.attributes} if entity.attributes else {"title": entity.title}
            ),
        )
        # 结束对每个实体的循环
        for entity in entities
    ]

    # 将documents列表中的所有文档加载到vectorstore中
    vectorstore.load_documents(documents=documents)

    # 函数返回更新后的向量存储
    return vectorstore

# 定义一个名为read_relationships的函数，它接受一个数据框（DataFrame）作为参数
def read_relationships(
    # 这个数据框是DataFrame类型，用于存储关系信息
    df: pd.DataFrame,
    # 指定列名，表示每个关系的唯一标识
    id_col: str = "id",
    # 可选列名，表示简短的唯一标识
    short_id_col: str | None = "short_id",
    # 指定列名，表示关系的起点
    source_col: str = "source",
    # 指定列名，表示关系的终点
    target_col: str = "target",
    # 可选列名，描述关系的详细信息
    description_col: str | None = "description",
    # 可选列名，包含描述的嵌入向量
    description_embedding_col: str | None = "description_embedding",
    # 可选列名，表示关系的权重
    weight_col: str | None = "weight",
    # 可选列名，存储文本单元的ID列表
    text_unit_ids_col: str | None = "text_unit_ids",
    # 可选列名，存储文档ID列表
    document_ids_col: str | None = "document_ids",
    # 可选列名列表，存储关系的其他属性
    attributes_cols: list[str] | None = None,
) -> list[Relationship]:
    # 创建一个空列表，用来存储关系对象
    relationships = []
    
    # 遍历数据框中的每一行
    for idx, row in df.iterrows():
        # 创建一个Relationship对象
        rel = Relationship(
            # 将id列的值转换为字符串
            id=to_str(row, id_col),
            # 如果short_id_col存在，则将它的值转换为字符串，否则使用当前行的索引作为值
            short_id=to_optional_str(row, short_id_col) if short_id_col else str(idx),
            # 将source_col的值转换为字符串
            source=to_str(row, source_col),
            # 将target_col的值转换为字符串
            target=to_str(row, target_col),
            # 将description_col的值转换为可选字符串
            description=to_optional_str(row, description_col),
            # 将description_embedding_col的值转换为浮点数列表
            description_embedding=to_optional_list(
                row, description_embedding_col, item_type=float
            ),
            # 将weight_col的值转换为可选浮点数
            weight=to_optional_float(row, weight_col),
            # 将text_unit_ids_col的值转换为字符串列表
            text_unit_ids=to_optional_list(row, text_unit_ids_col, item_type=str),
            # 将document_ids_col的值转换为字符串列表
            document_ids=to_optional_list(row, document_ids_col, item_type=str),
            # 如果attributes_cols存在，创建一个字典，键为attributes_cols中的列名，值为对应行的值
            # 否则，设置为None
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        # 将创建的关系对象添加到列表中
        relationships.append(rel)
    # 返回关系列表
    return relationships

# 定义一个函数read_covariates，接收一个名为df的数据框（类似电子表格的东西）
# 这个函数有多个参数，用于指定数据框中特定列的名称

def read_covariates(
    df: pd.DataFrame,  # 输入的数据框，类型是pandas的DataFrame
    id_col: str = "id",  # 列名，用于标识ID，默认是"id"
    short_id_col: str | None = "short_id",  # 短ID列名，默认是"short_id"，可以为空
    subject_col: str = "subject_id",  # 主题ID列名，默认是"subject_id"
    subject_type_col: str | None = "subject_type",  # 主题类型列名，默认是"subject_type"，可以为空
    covariate_type_col: str | None = "covariate_type",  # 变量类型列名，默认是"covariate_type"，可以为空
    text_unit_ids_col: str | None = "text_unit_ids",  # 文本单元ID列名，默认是"text_unit_ids"，可以为空
    document_ids_col: str | None = "document_ids",  # 文档ID列名，默认是"document_ids"，可以为空
    attributes_cols: list[str] | None = None,  # 属性列名列表，可以为空
) -> list[Covariate]:  # 函数返回值，是一个Covariate对象的列表

    # 创建一个空列表，用于存储Covariate对象
    covariates = []

    # 遍历数据框的每一行，用索引idx和对应的行数据row
    for idx, row in df.iterrows():
        # 创建一个Covariate对象，根据数据框中的列填充属性
        cov = Covariate(
            id=to_str(row, id_col),  # ID属性，从指定列转换成字符串
            short_id=to_optional_str(row, short_id_col) if short_id_col else str(idx),  # 短ID属性，如果列存在则转换，否则用索引转换成字符串
            subject_id=to_str(row, subject_col),  # 主题ID属性，从指定列转换成字符串
            subject_type=(to_str(row, subject_type_col) if subject_type_col else "entity"),  # 主题类型属性，如果列存在则转换，否则默认为"entity"
            covariate_type=(to_str(row, covariate_type_col) if covariate_type_col else "claim"),  # 变量类型属性，如果列存在则转换，否则默认为"claim"
            text_unit_ids=to_optional_list(row, text_unit_ids_col, item_type=str),  # 文本单元ID属性，如果列存在则转换成字符串列表
            document_ids=to_optional_list(row, document_ids_col, item_type=str),  # 文档ID属性，如果列存在则转换成字符串列表
            attributes=(  # 属性字典，如果attributes_cols存在则创建，否则设为None
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )

        # 将创建的Covariate对象添加到列表中
        covariates.append(cov)

    # 返回包含所有Covariate对象的列表
    return covariates

# 定义一个名为read_communities的函数，它接收一个DataFrame（数据表格）作为参数
def read_communities(
    # 这个DataFrame中的列名，表示社区的唯一标识
    df: pd.DataFrame,
    # 指定id列的名称，默认为"id"
    id_col: str = "id",
    # 可选的短id列名，默认为"short_id"，如果不存在则为None
    short_id_col: str | None = "short_id",
    # 标题列的名称，默认为"title"
    title_col: str = "title",
    # 级别列的名称，默认为"level"
    level_col: str = "level",
    # 实体id列的名称，默认为"entity_ids"，如果不存在则为None
    entities_col: str | None = "entity_ids",
    # 关系id列的名称，默认为"relationship_ids"，如果不存在则为None
    relationships_col: str | None = "relationship_ids",
    # 协变量id列的名称，默认为"covariate_ids"，如果不存在则为None
    covariates_col: str | None = "covariate_ids",
    # 属性列的列表，默认为None
    attributes_cols: list[str] | None = None,
) -> list[Community]:
    # 初始化一个空的社区列表
    communities = []

    # 遍历DataFrame的每一行
    for idx, row in df.iterrows():
        # 创建一个新的社区对象
        comm = Community(
            # 将id列的值转换为字符串
            id=to_str(row, id_col),
            # 如果有short_id列，则转换为字符串，否则用当前行的索引转换为字符串
            short_id=to_optional_str(row, short_id_col) if short_id_col else str(idx),
            # 将标题列的值转换为字符串
            title=to_str(row, title_col),
            # 将级别列的值转换为字符串
            level=to_str(row, level_col),
            # 如果有实体id列，将其转换为字符串列表
            entity_ids=to_optional_list(row, entities_col, item_type=str),
            # 如果有关系id列，将其转换为字符串列表
            relationship_ids=to_optional_list(row, relationships_col, item_type=str),
            # 如果有协变量id列，将其转换为键值都是字符串的字典
            covariate_ids=to_optional_dict(
                row, covariates_col, key_type=str, value_type=str
            ),
            # 如果有属性列，创建一个包含这些列值的字典，否则设为None
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        # 将创建的社区对象添加到社区列表中
        communities.append(comm)

    # 返回社区列表
    return communities

# 定义一个名为 read_community_reports 的函数，它接受一个数据框（DataFrame）作为参数
def read_community_reports(
    # 这个数据框是一个包含社区报告信息的表格
    df: pd.DataFrame,

    # 指定列名，用于存储报告的唯一ID
    id_col: str = "id",

    # 可选的列名，用于存储简短的ID
    short_id_col: str | None = "short_id",

    # 标题的列名
    title_col: str = "title",

    # 社区名称的列名
    community_col: str = "community",

    # 报告摘要的列名
    summary_col: str = "summary",

    # 报告完整内容的列名
    content_col: str = "full_content",

    # 排名的列名，可能是数字
    rank_col: str | None = "rank",

    # 摘要嵌入向量的列名，可能是一串数字
    summary_embedding_col: str | None = "summary_embedding",

    # 内容嵌入向量的列名，可能是一串数字
    content_embedding_col: str | None = "full_content_embedding",

    # 可选的列名列表，用于存储其他属性
    attributes_cols: list[str] | None = None,
) -> list[CommunityReport]:
    """从数据框中读取社区报告的信息并返回列表."""
    
    # 初始化一个空列表，用于存储社区报告对象
    reports = []

    # 遍历数据框中的每一行（索引和数据）
    for idx, row in df.iterrows():
        
        # 将数据转换为 CommunityReport 对象的参数
        # 使用函数 to_str 转换字符串类型列
        id = to_str(row, id_col)
        short_id = to_optional_str(row, short_id_col) if short_id_col else str(idx)  # 如果没有简短ID，用索引创建
        title = to_str(row, title_col)
        community_id = to_str(row, community_col)
        summary = to_str(row, summary_col)
        full_content = to_str(row, content_col)
        rank = to_optional_float(row, rank_col)  # 转换排名列，可能为None
        summary_embedding = to_optional_list(row, summary_embedding_col, item_type=float)  # 转换摘要嵌入列，可能为None
        content_embedding = to_optional_list(row, content_embedding_col, item_type=float)  # 转换内容嵌入列，可能为None

        # 如果有 attributes_cols，创建一个字典存储这些列的值
        attributes = (
            {col: row.get(col) for col in attributes_cols} 
            if attributes_cols 
            else None
        )

        # 创建 CommunityReport 对象并将它添加到列表中
        reports.append(CommunityReport(
            id=id,
            short_id=short_id,
            title=title,
            community_id=community_id,
            summary=summary,
            full_content=full_content,
            rank=rank,
            summary_embedding=summary_embedding,
            full_content_embedding=content_embedding,
            attributes=attributes,
        ))

    # 返回包含所有社区报告的列表
    return reports

# 定义一个函数，叫做read_text_units，它接收一个数据框（DataFrame）作为参数
def read_text_units(
    df: pd.DataFrame,  # 输入的数据框
    id_col: str = "id",   # 标识列，默认是"id"
    short_id_col: str | None = "short_id",  # 短标识列，默认是"short_id"，也可以是None
    text_col: str = "text",  # 文本列，默认是"text"
    entities_col: str | None = "entity_ids",  # 实体ID列，默认是"entity_ids"
    relationships_col: str | None = "relationship_ids",  # 关系ID列，默认是"relationship_ids"
    covariates_col: str | None = "covariate_ids",  # 因子ID列，默认是"covariate_ids"
    tokens_col: str | None = "n_tokens",  # 词数列，默认是"n_tokens"
    document_ids_col: str | None = "document_ids",  # 文档ID列，默认是"document_ids"
    embedding_col: str | None = "text_embedding",  # 嵌入向量列，默认是"text_embedding"
    attributes_cols: list[str] | None = None,  # 属性列列表，默认是None
) -> list[TextUnit]:  # 函数返回一个TextUnit对象的列表

    # 创建一个空列表，用来存储TextUnit对象
    text_units = []

    # 遍历数据框的每一行
    for idx, row in df.iterrows():
        # 创建一个TextUnit对象
        chunk = TextUnit(
            # 将id列的值转换为字符串并作为id
            id=to_str(row, id_col),
            # 如果short_id_col存在，将对应的值转换为可选字符串；否则，用当前行的索引转换为字符串
            short_id=to_optional_str(row, short_id_col) if short_id_col else str(idx),
            # 将text_col列的值转换为字符串
            text=to_str(row, text_col),
            # 如果entities_col存在，将对应的值转换为字符串列表
            entity_ids=to_optional_list(row, entities_col, item_type=str),
            # 如果relationships_col存在，将对应的值转换为字符串列表
            relationship_ids=to_optional_list(row, relationships_col, item_type=str),
            # 如果covariates_col存在，将对应的值转换为键值都是字符串的字典
            covariate_ids=to_optional_dict(
                row, covariates_col, key_type=str, value_type=str
            ),
            # 如果embedding_col存在，将对应的值转换为浮点数列表
            text_embedding=to_optional_list(row, embedding_col, item_type=float),  # 忽略类型检查
            # 如果tokens_col存在，将对应的值转换为整数
            n_tokens=to_optional_int(row, tokens_col),
            # 如果document_ids_col存在，将对应的值转换为字符串列表
            document_ids=to_optional_list(row, document_ids_col, item_type=str),
            # 如果attributes_cols存在，创建包含这些列值的字典；否则，设置为None
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )

        # 将创建的TextUnit对象添加到列表中
        text_units.append(chunk)

    # 返回存储了所有TextUnit对象的列表
    return text_units

# 定义一个名为read_documents的函数，它接受一个DataFrame（数据表格）作为参数
def read_documents(
    df: pd.DataFrame,  # 输入的数据框
    id_col: str = "id",   # ID列的默认名称
    short_id_col: str = "short_id",  # 短ID列的默认名称
    title_col: str = "title",  # 标题列的默认名称
    type_col: str = "type",  # 类型列的默认名称
    summary_col: str | None = "entities",  # 摘要列的默认名称，也可以是None
    raw_content_col: str | None = "relationships",  # 原始内容列的默认名称，也可以是None
    summary_embedding_col: str | None = "summary_embedding",  # 摘要嵌入列的默认名称，也可以是None
    content_embedding_col: str | None = "raw_content_embedding",  # 内容嵌入列的默认名称，也可以是None
    text_units_col: str | None = "text_units",  # 文本单元列的默认名称，也可以是None
    attributes_cols: list[str] | None = None,  # 属性列的列表，也可以是None
) -> list[Document]:  # 函数返回值类型是一个Document对象的列表

    # 创建一个空列表，用于存储处理后的文档
    docs = []

    # 遍历数据框中的每一行
    for idx, row in df.iterrows():
        # 将每行数据转换为一个Document对象
        doc = Document(
            # ID设置为字符串形式的指定列
            id=to_str(row, id_col),
            # 短ID如果存在就转换为字符串，否则用当前行的索引转为字符串
            short_id=to_optional_str(row, short_id_col) if short_id_col else str(idx),
            # 标题设置为指定列的字符串形式
            title=to_str(row, title_col),
            # 类型设置为指定列的字符串形式
            type=to_str(row, type_col),
            # 摘要如果存在就转换为字符串，否则设为None
            summary=to_optional_str(row, summary_col),
            # 原始内容设置为指定列的字符串形式
            raw_content=to_str(row, raw_content_col),
            # 摘要嵌入如果存在就转换为浮点数列表，否则设为None
            summary_embedding=to_optional_list(row, summary_embedding_col, item_type=float),
            # 内容嵌入如果存在就转换为浮点数列表，否则设为None
            raw_content_embedding=to_optional_list(row, content_embedding_col, item_type=float),
            # 文本单元如果存在就转换为字符串列表，否则设为None
            text_units=to_list(row, text_units_col, item_type=str),  # type: ignore
            # 属性如果存在，就创建一个字典，键是属性列名，值是对应列的值；否则设为None
            attributes=(
                {col: row.get(col) for col in attributes_cols}  # 使用字典推导式
                if attributes_cols
                else None
            ),
        )

        # 将转换后的Document对象添加到列表中
        docs.append(doc)

    # 返回处理后的文档列表
    return docs

