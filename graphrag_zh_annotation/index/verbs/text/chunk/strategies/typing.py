# 导入Callable和Iterable，它们是Python中定义函数和可迭代对象的抽象基类
from collections.abc import Callable, Iterable

# 导入Any，它在Python类型注释中代表任何类型的数据
from typing import Any

# 导入ProgressTicker，这是一个用于显示进度条的工具
from datashaper import ProgressTicker

# 从graphrag库的index.verbs.text.chunk.typing模块导入TextChunk类，这可能是一个文本块的定义
from graphrag.index.verbs.text.chunk.typing import TextChunk

# 这段文字是版权信息，告诉我们代码由微软公司创建，并遵循MIT许可证

# 定义一个模块，里面包含ChunkStrategy的定义
# "ChunkStrategy" 是一个特殊类型的函数

# ChunkStrategy是一个函数，它接收以下参数：
# - 一个字符串列表（文档文本）
# - 一个字典（包含额外信息）
# - 一个ProgressTicker对象（用于追踪进度）

ChunkStrategy = Callable[
    # 参数列表
    [list[str],  # 文档文本列表
     dict[str, Any],  # 额外信息字典
     ProgressTicker],  # 进度条工具
    # 函数返回值类型
    Iterable[TextChunk]  # 返回一个包含TextChunk对象的可迭代序列
]

