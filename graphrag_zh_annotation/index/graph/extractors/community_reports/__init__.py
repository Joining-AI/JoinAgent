# 导入一个叫做schemas的模块，这个模块包含了一些关于社区报告的规则
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 从当前目录下的build_mixed_context文件中导入一个函数，用于创建混合上下文
from .build_mixed_context import build_mixed_context

# 从community_reports_extractor文件中导入一个类，用于提取社区报告
from .community_reports_extractor import CommunityReportsExtractor

# 从prep_community_report_context文件中导入一个函数，用于准备社区报告的上下文
from .prep_community_report_context import prep_community_report_context

# 从prompts文件中导入一个常量，可能是一个提示信息，用于社区报告
from .prompts import COMMUNITY_REPORT_PROMPT

# 从sort_context文件中导入一个函数，用于排序上下文
from .sort_context import sort_context

# 从utils模块中导入多个辅助函数，它们分别有特定的功能
from .utils import (
    filter_claims_to_nodes,  # 过滤声明并转换成节点
    filter_edges_to_nodes,  # 过滤边并转换成节点
    filter_nodes_to_level,  # 根据级别过滤节点
    get_levels,  # 获取节点的级别
    set_context_exceeds_flag,  # 设置上下文是否超过某个标志
    set_context_size,  # 设置上下文的大小
)

# 这是微软公司2024年的版权信息，代码遵循MIT许可证

# 这是一个有关社区报告的包的根目录的注释

# 把上面导入的一些常量、类和函数公开，这样其他地方可以使用它们
__all__ = [
    "COMMUNITY_REPORT_PROMPT",
    "CommunityReportsExtractor",
    "build_mixed_context",
    "filter_claims_to_nodes",
    "filter_edges_to_nodes",
    "filter_nodes_to_level",
    "get_levels",
    "prep_community_report_context",
    "schemas",
    "set_context_exceeds_flag",
    "set_context_size",
    "sort_context",
]

