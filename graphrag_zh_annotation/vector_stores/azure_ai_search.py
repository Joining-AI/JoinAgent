# 导入json模块，它用来处理JSON格式的数据
import json

# 从typing库导入Any类型，这是一个表示任何类型的占位符
from typing import Any

# 从azure.core.credentials导入AzureKeyCredential，这是Azure服务认证的一种方式
from azure.core.credentials import AzureKeyCredential

# 从azure.identity导入DefaultAzureCredential，它能自动获取Azure服务的默认身份验证
from azure.identity import DefaultAzureCredential

# 从azure.search.documents导入SearchClient和SearchIndexClient，它们是与Azure Search服务交互的类
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

# 从azure.search.documents.indexes.models导入一系列类和数据结构，它们用于定义和操作Azure Search索引
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,  # 一种搜索算法配置
    HnswParameters,  # HNSW（Hierarchical Navigable Small World）算法的参数
    SearchableField,  # 可以进行全文搜索的字段
    SearchField,  # 搜索索引中的字段
    SearchFieldDataType,  # 字段的数据类型
    SearchIndex,  # 搜索索引的定义
    SimpleField,  # 简单的非全文搜索字段
    VectorSearch,  # 向量搜索功能
    VectorSearchAlgorithmMetric,  # 向量搜索算法的度量
    VectorSearchProfile,  # 向量搜索配置
)

# 从azure.search.documents.models导入VectorizedQuery，它用于处理向量查询
from azure.search.documents.models import VectorizedQuery

# 从graphrag.model.types导入TextEmbedder，这是一个文本嵌入模型
from graphrag.model.types import TextEmbedder

# 从当前项目的.base模块导入一些基础类和定义
from .base import (
    DEFAULT_VECTOR_SIZE,  # 默认的向量大小
    BaseVectorStore,  # 基础的向量存储类
    VectorStoreDocument,  # 向量存储中的文档结构
    VectorStoreSearchResult,  # 向量搜索结果的结构
)

# 这是微软公司2024年的代码，别人可以用，但要遵守MIT许可证。
# 这个代码包是用来实现Azure AI搜索向量存储功能的。

# 导入一些Python工具，让我们能做更多的事情。
# json模块帮助我们处理数据，typing模块让代码更清晰。
import json
from typing import Any

# 这两个模块帮我们连接到Azure服务并验证身份。
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential

# 这些模块让我们可以创建和管理Azure搜索服务。
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    # 这些是Azure搜索服务里的各种工具，用来构建和操作搜索索引。
    # 它们定义了索引的样子和工作方式。
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
)

# 这个模块让我们可以进行向量搜索查询。
from azure.search.documents.models import VectorizedQuery

# 从另一个模块导入的，可能是一个把文字变成数字向量的工具。
from graphrag.model.types import TextEmbedder

# 从同一个包里导入一些基本的东西，比如默认向量大小和类。
from .base import (
    DEFAULT_VECTOR_SIZE,
    BaseVectorStore,
    VectorStoreDocument,
    VectorStoreSearchResult,
)

# 现在我们定义一个新类，它叫做VectorStore，是BaseVectorStore的子类，专门用来存向量。

# 这是一个名为AzureAISearch的类，它继承自一个叫BaseVectorStore的基类。
class AzureAISearch(BaseVectorStore):
    # 这个类用来实现与Azure AI Search的向量存储交互。

    # 这个变量保存与Azure Search索引交互的客户端。
    index_client: SearchIndexClient

    # 这个方法用于连接到Azure AI的向量存储。
    def connect(self, **kwargs: Any) -> Any:
        # 获取从方法参数传来的URL、API密钥和受众信息。
        url = kwargs.get("url", None)
        api_key = kwargs.get("api_key", None)
        audience = kwargs.get("audience", None)
        self.vector_size = kwargs.get("vector_size", DEFAULT_VECTOR_SIZE)

        # 设置向量搜索配置文件的名称。
        self.vector_search_profile_name = kwargs.get(
            "vector_search_profile_name", "vectorSearchProfile"
        )

        # 如果有URL，就建立与Azure Search服务的连接。
        if url:
            # 如果有受众，就把它作为参数。
            audience_arg = {"audience": audience} if audience else {}
            # 创建一个用于与Azure Search服务交流的客户端。
            self.db_connection = SearchClient(
                endpoint=url,  # 服务的地址
                index_name=self.collection_name,  # 索引的名字
                credential=AzureKeyCredential(api_key) if api_key else DefaultAzureCredential(),  # 使用API密钥或默认凭证登录
                **audience_arg,  # 添加受众参数
            )
            # 创建一个管理Azure Search索引的客户端。
            self.index_client = SearchIndexClient(
                endpoint=url,  # 服务的地址
                credential=AzureKeyCredential(api_key) if api_key else DefaultAzureCredential(),  # 使用API密钥或默认凭证登录
                **audience_arg,  # 添加受众参数
            )
        else:
            # 如果没有URL，表示不能在本地运行，所以抛出一个错误。
            raise ValueError("AAISearchDBClient is not supported on local host.")

    # 这个方法将文档加载到Azure AI Search索引中。
    def load_documents(self, documents: list[VectorStoreDocument], overwrite: bool = True) -> None:
        # 如果overwrite为True，会覆盖已有数据。
        if overwrite:
            # 如果索引已存在，就删除它。
            if self.collection_name in self.index_client.list_index_names():
                self.index_client.delete_index(self.collection_name)

            # 配置向量搜索，设置算法和参数。
            vector_search = VectorSearch(
                algorithms=[
                    HnswAlgorithmConfiguration(
                        name="HnswAlg",
                        parameters=HnswParameters(metric=VectorSearchAlgorithmMetric.COSINE),  # 使用余弦相似度
                    )
                ],
                profiles=[
                    VectorSearchProfile(
                        name=self.vector_search_profile_name,  # 设置配置文件名
                        algorithm_configuration_name="HnswAlg",  # 使用上面定义的算法
                    )
                ],
            )

            # 创建或更新一个索引，定义其名称和字段。
            index = SearchIndex(
                name=self.collection_name,
                fields=[
                    # 唯一标识符字段。
                    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                    # 向量字段，用于存储文档的向量表示。
                    SearchField(
                        name="vector",
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True,
                        vector_search_dimensions=self.vector_size,
                        vector_search_profile_name=self.vector_search_profile_name,
                    ),
                    # 可搜索的文本内容字段。
                    SearchableField(name="text", type=SearchFieldDataType.String),
                    # 存储文档其他属性的简单字段。
                    SimpleField(name="attributes", type=SearchFieldDataType.String),
                ],
                vector_search=vector_search,
            )

            # 在Azure AI Search服务中创建或更新索引。
            self.index_client.create_or_update_index(index)

        # 准备要上传的文档批次。
        batch = [
            {
                "id": doc.id,
                "vector": doc.vector,
                "text": doc.text,
                "attributes": json.dumps(doc.attributes),  # 将属性转换为JSON字符串
            }
            for doc in documents  # 遍历所有文档
            if doc.vector is not None  # 只选有向量的文档
        ]

        # 如果有文档，就上传到Azure AI Search。
        if batch and len(batch) > 0:
            self.db_connection.upload_documents(batch)

    # 这个方法根据ID列表过滤文档。
    def filter_by_id(self, include_ids: list[str] | list[int]) -> Any:
        # 如果没有ID或ID列表为空，就设置过滤器为None。
        if include_ids is None or len(include_ids) == 0:
            self.query_filter = None
            return self.query_filter

        # 将ID列表转换成逗号分隔的字符串。
        id_filter = ",".join([f"{id!s}" for id in include_ids])

        # 设置过滤器，按ID列表过滤文档。
        self.query_filter = f"search.in(id, '{id_filter}', ',')"

        # 返回过滤器（实际上这个返回值可能不被使用）。
        return self.query_filter

    # 这个方法基于向量进行相似性搜索。
    def similarity_search_by_vector(
        self, query_embedding: list[float], k: int = 10, **kwargs: Any
    ) -> list[VectorStoreSearchResult]:
        # 创建向量化查询，包含查询向量、最近邻数量k和要搜索的字段。
        vectorized_query = VectorizedQuery(
            vector=query_embedding, k_nearest_neighbors=k, fields="vector"
        )

        # 执行搜索查询并获取响应。
        response = self.db_connection.search(vector_queries=[vectorized_query])

        # 处理搜索结果，返回一个包含结果的列表。
        return [
            VectorStoreSearchResult(
                document=VectorStoreDocument(
                    id=doc.get("id", ""),
                    text=doc.get("text", ""),
                    vector=doc.get("vector", []),
                    attributes=json.loads(doc.get("attributes", "{}")),
                ),
                score=doc["@search.score"],
            )
            for doc in response
        ]

    # 这个方法基于文本进行相似性搜索。
    def similarity_search_by_text(
        self, text: str, text_embedder: TextEmbedder, k: int = 10, **kwargs: Any
    ) -> list[VectorStoreSearchResult]:
        # 使用文本嵌入器将文本转换为向量。
        query_embedding = text_embedder(text)
        # 如果转换成功，进行向量相似性搜索。
        if query_embedding:
            return self.similarity_search_by_vector(query_embedding=query_embedding, k=k)
        # 如果转换失败，返回空的结果列表。
        return []

