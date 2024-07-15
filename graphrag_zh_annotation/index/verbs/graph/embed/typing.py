# 导入一个叫做 Any 的类型提示，它代表任何类型的数据
from typing import Any

# 这是一个版权声明，表示这段代码由微软公司创作，2024年版权所有
# 并且遵循 MIT 许可证的规则

# 这是一个模块，里面包含不同的列表和字典的定义
"""A module containing different lists and dictionaries."""

# 使用这个简单的导入，而不是一个更复杂的包装器
from typing import Any

# 定义一个 NodeList 类型，它是一个字符串的列表
NodeList = list[str] 
# 比如：['apple', 'banana', 'orange']

# 定义一个 EmbeddingList 类型，它可以是任何类型数据的列表
EmbeddingList = list[Any] 
# 比如：[3, 'hello', True]

# 定义一个 NodeEmbeddings 类型，它是一个字典，键是字符串，值是浮点数列表
NodeEmbeddings = dict[str, list[float]] 
# 比如：{'apple': [0.1, 0.2, 0.3], 'banana': [0.4, 0.5, 0.6]}
# 这可以用来存储标签（如单词）对应的向量（一组浮点数）
# """Label -> Embedding"""
# 这句话是注释，表示字典中的键（Label）对应着嵌入（Embedding）

