# 导入 claims 模块中的两个变量和一个类
from .claims import CLAIM_EXTRACTION_PROMPT, ClaimExtractor
# claims 模块帮助我们找到和提取声明（比如观点或事实）

# 导入 community_reports 模块中的两个变量和一个类
from .community_reports import (
    COMMUNITY_REPORT_PROMPT,
    CommunityReportsExtractor,
)
# community_reports 模块用来处理社区报告，提取相关信息

# 导入 graph 模块中的两个类
from .graph import GraphExtractionResult, GraphExtractor
# graph 模块帮助我们获取图形数据的提取结果和工具

# 这是微软公司的版权信息，告诉我们代码的归属和使用的许可
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个包是关于什么的
"""The Indexing Engine graph extractors package root."""

# 以下这一行列出了一些可以公开访问的名称，这些名称来自前面导入的模块
__all__ = [
    "CLAIM_EXTRACTION_PROMPT",
    "COMMUNITY_REPORT_PROMPT",
    "ClaimExtractor",
    "CommunityReportsExtractor",
    "GraphExtractionResult",
    "GraphExtractor",
]
# 这些名称可以让其他程序更容易地使用这个包里的功能和数据

