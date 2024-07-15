# 定义一个名为LanceDBVectorStore的类，它将帮助我们使用LanceDB来存储向量。
class LanceDBVectorStore(BaseVectorStore):
    def __init__(self, uri: str, text_embedder: TextEmbedder) -> None:
        # 初始化这个类时，我们需要LanceDB的地址（uri）和一个能将文本转为向量的工具。
        self.uri = uri
        self.text_embedder = text_embedder
        self.client = lancedb.Client(self.uri)  # 创建一个连接LanceDB的客户端

    def upsert(self, document: VectorStoreDocument) -> None:
        # 将一个文档（包含文本和向量）添加或更新到数据库中。
        vector = self.text_embedder.embed(document.text)  # 先把文档的文本转换为向量
        self.client.upsert(document.id, vector)  # 然后用ID和向量更新数据库

    def search(self, query: str, top_k: int = 10) -> VectorStoreSearchResult:
        # 搜索与查询最相似的向量，并返回结果。
        vector = self.text_embedder.embed(query)  # 把查询文本转换为向量
        results = self.client.search(vector, top_k)  # 在数据库中找到最匹配的向量
        return VectorStoreSearchResult(results)  # 将结果包装成一个特殊的搜索结果对象

    def close(self) -> None:
        # 关闭与LanceDB的连接。
        self.client.close()

# 这是一个名为LanceDBVectorStore的类，它用于存储和检索向量数据。
class LanceDBVectorStore(BaseVectorStore):
    # 类的描述，告诉我们这个类是用来做什么的。
    """用于实现LanceDB向量存储的类"""

    # 这个方法用来连接到存储向量数据的数据库。
    def connect(self, **kwargs: Any) -> Any:
        """连接到向量数据的数据库"""
        # 检查是否提供了数据库的地址，如果没有，就用默认的。
        db_uri = kwargs.get("db_uri", "./lancedb")
        # 使用LanceDB的函数连接到数据库。
        self.db_connection = lancedb.connect(db_uri)  # 不考虑类型检查

    # 这个方法将文档加载到存储中。
    def load_documents(
        self, documents: list[VectorStoreDocument], overwrite: bool = True
    ) -> None:
        """将文档加载到向量存储中"""
        # 创建一个列表，存储每个文档的信息（id、文本、向量和属性）。
        data = [
            {"id": doc.id, "text": doc.text, "vector": doc.vector, "attributes": json.dumps(doc.attributes)}
            for doc in documents
            if doc.vector is not None  # 只有含有向量的文档才会被加入
        ]

        # 如果没有数据，就设置为None。
        if len(data) == 0:
            data = None

        # 定义数据的结构。
        schema = pa.schema([
            pa.field("id", pa.string()),  # id是字符串
            pa.field("text", pa.string()),  # 文本也是字符串
            pa.field("vector", pa.list_(pa.float64())),  # 向量是浮点数列表
            pa.field("attributes", pa.string()),  # 属性是字符串
        ])

        # 如果要覆盖现有数据（overwrite=True），则创建或更新表。
        if overwrite:
            if data:
                # 创建新表，用数据填充。
                self.document_collection = self.db_connection.create_table(
                    self.collection_name, data=data, mode="overwrite"
                )
            else:
                # 创建新表，只包含定义的结构。
                self.document_collection = self.db_connection.create_table(
                    self.collection_name, schema=schema, mode="overwrite"
                )
        else:
            # 如果不覆盖（overwrite=False），打开现有表并添加数据。
            self.document_collection = self.db_connection.open_table(self.collection_name)
            if data:
                self.document_collection.add(data)  # 将数据添加到表中

    # 这个方法根据id过滤文档。
    def filter_by_id(self, include_ids: list[str] | list[int]) -> Any:
        """根据id过滤文档"""
        # 如果没有id，过滤器设为None。
        if len(include_ids) == 0:
            self.query_filter = None
        else:
            # 将id转成字符串列表或数字列表，用于过滤。
            if isinstance(include_ids[0], str):
                id_filter = ", ".join([f"'{id}'" for id in include_ids])
                self.query_filter = f"id in ({id_filter})"
            else:
                self.query_filter = f"id in ({', '.join([str(id) for id in include_ids])})"
        return self.query_filter

    # 根据向量进行相似性搜索。
    def similarity_search_by_vector(
        self, query_embedding: list[float], k: int = 10, **kwargs: Any
    ) -> list[VectorStoreSearchResult]:
        """根据向量搜索相似文档"""
        # 如果有查询过滤器，使用它。
        if self.query_filter:
            docs = (
                self.document_collection.search(query=query_embedding)
                .where(self.query_filter, prefilter=True)  # 应用过滤器
                .limit(k)  # 限制结果数量
                .to_list()  # 转换为列表
            )
        else:
            # 没有过滤器，直接搜索并限制结果数量。
            docs = (
                self.document_collection.search(query=query_embedding)
                .limit(k)
                .to_list()
            )
        # 将搜索结果转换为我们需要的格式并返回。
        return [
            VectorStoreSearchResult(
                document=VectorStoreDocument(
                    id=doc["id"],
                    text=doc["text"],
                    vector=doc["vector"],
                    attributes=json.loads(doc["attributes"]),  # 将属性从JSON转回
                ),
                score=1 - abs(float(doc["_distance"])),  # 计算得分
            )
            for doc in docs
        ]

    # 根据文本进行相似性搜索。
    def similarity_search_by_text(
        self, text: str, text_embedder: TextEmbedder, k: int = 10, **kwargs: Any
    ) -> list[VectorStoreSearchResult]:
        """使用给定的文本搜索相似文档"""
        # 使用文本嵌入工具将文本转换为向量。
        query_embedding = text_embedder(text)
        # 如果转换成功，使用向量进行搜索。
        if query_embedding:
            return self.similarity_search_by_vector(query_embedding, k)
        # 如果转换失败，返回空列表。
        return []

