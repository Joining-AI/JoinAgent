# 这是一个代码文件的开头，它告诉我们这段代码是微软公司在2024年写的，并且遵循MIT许可证。

"""这是向量存储的基础类。"""

# 我们引入一些工具，让编程变得更简单。
from abc import ABC, abstractmethod  # 这些工具让我们能创建一个需要别人去实现具体功能的特殊类
from dataclasses import dataclass, field  # 这些工具帮助我们快速创建有固定结构的数据类
from typing import Any  # 这个工具告诉Python，变量可以是任何类型的值

# 我们还用到了一个特别的文本转向量的工具。
from graphrag.model.types import TextEmbedder

# 假设每个文档的向量由1536个数字组成，这就是一个默认的向量大小。
DEFAULT_VECTOR_SIZE = 1536

# 这个类叫VectorStoreDocument，用来存放存储在向量库里的文档信息。
@dataclass
class VectorStoreDocument:
    """这个类代表一个存储在向量库里的文档。"""
    id: str or int  # 每个文档都有一个独一无二的ID
    text: str or None  # 文档的内容，可能有的时候没有
    vector: list of numbers or None  # 文档的向量表示，也可能不存在
    attributes: dict[str, Any] = field(default_factory=dict)  # 保存额外信息，比如标题、日期等

# 另一个类叫VectorStoreSearchResult，用于展示向量库搜索的结果。
@dataclass
class VectorStoreSearchResult:
    """这个类表示搜索向量库后的结果。"""
    document: VectorStoreDocument  # 搜索到的文档
    score: float  # 相似度分数，越高表示越相似（从0到1之间）

# 最后，我们创建了一个基础的向量存储类，叫做BaseVectorStore，它规定了向量库应该有哪些功能，但不具体实现。

# 定义一个叫BaseVectorStore的类，它是所有向量存储数据访问类的基础
class BaseVectorStore(ABC):
    """这个类是用来存取向量数据的模板类。"""

    # 当我们创建一个新的BaseVectorStore对象时，会执行这个方法
    def __init__(self,
                 collection_name: str,  # 集合的名字，就像一个数据库里的表格
                 db_connection: Any | None = None,  # 数据库连接，可以是任何类型，但默认是None
                 document_collection: Any | None = None,  # 文档集合，也是数据的一部分，可能为空
                 query_filter: Any | None = None,  # 查询过滤器，用于筛选数据，也可能为空
                 **kwargs: Any,  # 其他可能需要的参数，用星号表示可以传很多个
    ):
        self.collection_name = collection_name  # 保存集合名字
        self.db_connection = db_connection  # 保存数据库连接
        self.document_collection = document_collection  # 保存文档集合
        self.query_filter = query_filter  # 保存查询过滤器
        self.kwargs = kwargs  # 保存其他额外的参数

    # 这是一个必须实现的方法，但它没有具体内容，是用来连接到向量存储的
    @abstractmethod
    def connect(self, **kwargs: Any) -> None:
        """连接到存储向量的地方。"""

    # 另一个必须实现的方法，用于把文档加载到向量存储里
    @abstractmethod
    def load_documents(self, documents: list[VectorStoreDocument], overwrite: bool = True) -> None:
        """把文档（包含向量信息）加载到存储里。如果overwrite=True，会覆盖原有数据。"""

    # 第三个必须实现的方法，用于寻找与给定向量最相似的邻居
    @abstractmethod
    def similarity_search_by_vector(self, query_embedding: list[float], k: int = 10, **kwargs: Any) -> list[VectorStoreSearchResult]:
        """通过一个向量找最接近的k个邻居。返回结果列表。"""

    # 第四个必须实现的方法，通过文本内容寻找相似的向量
    @abstractmethod
    def similarity_search_by_text(self, text: str, text_embedder: TextEmbedder, k: int = 10, **kwargs: Any) -> list[VectorStoreSearchResult]:
        """用一段文本找最接近的k个邻居。需要一个能转换文本为向量的工具。"""

    # 最后一个必须实现的方法，根据一串id来创建查询过滤器
    @abstractmethod
    def filter_by_id(self, include_ids: list[str] | list[int]) -> Any:
        """根据提供的id列表创建一个过滤器，用于查找特定的文档。"""

