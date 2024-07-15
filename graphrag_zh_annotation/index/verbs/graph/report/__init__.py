# 这段代码是从一个叫做 'create_community_reports' 的地方导入两个东西：
# - 一个类型，叫做 CreateCommunityReportsStrategyType
# - 一个函数，叫做 create_community_reports
from .create_community_reports import (
    CreateCommunityReportsStrategyType,
    create_community_reports,
)

# 从 'prepare_community_reports' 导入一个函数，叫做 prepare_community_reports
from .prepare_community_reports import prepare_community_reports

# 从 'prepare_community_reports_claims' 导入一个函数，叫做 prepare_community_reports_claims
from .prepare_community_reports_claims import prepare_community_reports_claims

# 从 'prepare_community_reports_edges' 导入一个函数，叫做 prepare_community_reports_edges
from .prepare_community_reports_edges import prepare_community_reports_edges

# 从 'prepare_community_reports_nodes' 导入一个函数，叫做 prepare_community_reports_nodes
from .prepare_community_reports_nodes import prepare_community_reports_nodes

# 从 'restore_community_hierarchy' 导入一个函数，叫做 restore_community_hierarchy
from .restore_community_hierarchy import restore_community_hierarchy

# 这是一个版权信息，告诉我们这个代码是微软公司2024年的作品，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个注释告诉我们，这是一个关于图报告（graph report）的包的根目录
# "Indexing Engine graph report package root."

# 再次导入 'create_community_reports' 的两个元素，这样在当前文件中可以直接使用它们
from .create_community_reports import (
    CreateCommunityReportsStrategyType,
    create_community_reports,
)

# 然后列出所有对外公开的（导出的）元素，这样其他地方可以使用这些名字来调用这里的功能
__all__ = [
    "CreateCommunityReportsStrategyType",
    "create_community_reports",
    "create_community_reports",  # 注意：这里重复了，可能是一个复制错误
    "prepare_community_reports",
    "prepare_community_reports_claims",
    "prepare_community_reports_edges",
    "prepare_community_reports_nodes",
    "restore_community_hierarchy",
]

