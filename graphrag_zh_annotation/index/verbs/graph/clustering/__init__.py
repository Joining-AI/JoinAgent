# 导入模块中的两个特殊东西
from .cluster_graph import GraphCommunityStrategyType, cluster_graph
# 这是版权信息，说明代码由微软公司在2024年创建
# 并且遵循MIT许可证，这是一个允许他人自由使用、修改和分享代码的许可协议

# 这个是文档字符串，它描述了这个包是关于图聚类引擎的一部分
# "__"前缀的变量在Python中通常是内部使用的，但这里它告诉别人这个包里有哪些东西可以被外部使用
# "Indexing Engine"可能是程序的一个部分，负责处理图数据

from .cluster_graph import GraphCommunityStrategyType, cluster_graph

# "__all__"变量告诉别人当从这个包导入时，可以只用这两行代码列出的东西
# 这里是"GraphCommunityStrategyType"和"cluster_graph"，它们是对外提供的功能

