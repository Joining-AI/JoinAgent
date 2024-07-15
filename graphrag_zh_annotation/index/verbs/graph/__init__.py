# 导入模块，这些模块是用来处理图（比如社交网络或关系网络）的
from .clustering import cluster_graph     # 导入用于聚类图的函数
from .compute_edge_combined_degree import compute_edge_combined_degree  # 导入计算边的组合度的函数
from .create import DEFAULT_EDGE_ATTRIBUTES, DEFAULT_NODE_ATTRIBUTES, create_graph  # 导入创建图时的默认边属性、节点属性和创建图的函数
from .embed import embed_graph             # 导入将图嵌入到某个空间的函数
from .layout import layout_graph           # 导入布局图，使其在视觉上更易理解的函数
from .merge import merge_graphs            # 导入合并多个图的函数
from .report import (                       # 导入生成关于图社区结构报告的相关函数
    create_community_reports,
    prepare_community_reports,
    prepare_community_reports_claims,
    prepare_community_reports_edges,
    restore_community_hierarchy,
)
from .unpack import unpack_graph           # 导入解包图，可能是指分解或扩展图的函数

# 版权声明，这段代码由微软公司拥有，遵循MIT许可证

# 这是图形处理包的主文件

# 再次导入上述的一些关键功能，这样当其他人使用这个包时，可以直接使用这些名字
# 这些都是对外公开的接口，方便他人调用
__all__ = [
    "DEFAULT_EDGE_ATTRIBUTES",
    "DEFAULT_NODE_ATTRIBUTES",
    "cluster_graph",
    "compute_edge_combined_degree",
    "create_community_reports",
    "create_graph",
    "embed_graph",
    "layout_graph",
    "merge_graphs",
    "prepare_community_reports",
    "prepare_community_reports_claims",
    "prepare_community_reports_edges",
    "restore_community_hierarchy",
    "unpack_graph",
]

