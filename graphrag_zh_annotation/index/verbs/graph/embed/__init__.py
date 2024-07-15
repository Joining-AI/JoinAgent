# 导入模块中的两个东西，它们是关于图嵌入的类型和方法
from .embed_graph import EmbedGraphStrategyType, embed_graph

# 这一行是版权信息，表示代码由微软公司在2024年创建
# Licensed under the MIT License 表示代码使用MIT许可证，允许别人自由使用，只要遵守一定规则

# 这个模块的文档字符串，简单说明这是图嵌入引擎的一部分
"""这个包是关于图嵌入引擎的根目录。"""

# 再次从(embed_graph)导入EmbedGraphStrategyType和embed_graph，并将它们公开给外部使用
from .embed_graph import EmbedGraphStrategyType, embed_graph

# '__all__' 是一个特殊变量，告诉其他程序这个模块中哪些东西可以被"导入*"(import *)使用
# 这里列出了两个：EmbedGraphStrategyType 和 embed_graph
__all__ = ["EmbedGraphStrategyType", "embed_graph"]

