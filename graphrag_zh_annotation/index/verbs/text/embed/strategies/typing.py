# 导入一些Python库，这些库帮助我们做不同的事情
from collections.abc import Awaitable, Callable  # 从这里导入可以等待的结果类型和可调用对象的定义
from dataclasses import dataclass  # 用于创建数据类的工具
from datashaper import VerbCallbacks  # 一个可能用于处理数据操作的类
from graphrag.index.cache import PipelineCache  # 一个关于数据管道缓存的类

# 这是代码的版权信息，说明由微软公司在2024年拥有，并遵循MIT许可证

# 这个模块包含了'TextEmbeddingResult'模型的定义

# 再次导入Awaitable和Callable，确保它们在本文件中可用
from collections.abc import Awaitable, Callable

# 导入VerbCallbacks，用于数据操作
from datashaper import VerbCallbacks

# 导入PipelineCache，用于缓存数据管道
from graphrag.index.cache import PipelineCache


# 使用dataclass装饰器创建一个类，叫做TextEmbeddingResult
@dataclass
class TextEmbeddingResult:
    """这是一个用来存储文本嵌入结果的类。

    它有一个属性：
    - embeddings：一个列表，里面装着浮点数列表或None，也可能整个列表为None。
    """

# 定义一个类型：TextEmbeddingStrategy
# 这是一个函数类型，它接受以下四个参数：
# - 列表中的字符串
# - VerbCallbacks对象
# - PipelineCache对象
# - 一个字典
# 并返回一个等待的结果（可能是TextEmbeddingResult）

TextEmbeddingStrategy = Callable[
    [
        list[str],  # 文本列表
        VerbCallbacks,  # 数据处理回调
        PipelineCache,  # 数据管道缓存
        dict,  # 额外的配置或参数
    ],
    Awaitable[TextEmbeddingResult],  # 返回的结果是一个可以等待的TextEmbeddingResult对象
]

