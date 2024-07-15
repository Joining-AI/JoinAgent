# 导入一些特别的代码片段，它们来自其他文件
from .community_report_summarization import COMMUNITY_REPORT_SUMMARIZATION_PROMPT  # 从社区报告总结模块导入一个提示
from .entity_extraction import (  # 从实体提取模块导入几个东西
    EXAMPLE_EXTRACTION_TEMPLATE,  # 示例提取模板
    GRAPH_EXTRACTION_JSON_PROMPT,  # 图形提取的JSON提示
    GRAPH_EXTRACTION_PROMPT,  # 图形提取提示
    UNTYPED_EXAMPLE_EXTRACTION_TEMPLATE,  # 未分类的示例提取模板
    UNTYPED_GRAPH_EXTRACTION_PROMPT,  # 未分类的图形提取提示
)
from .entity_summarization import ENTITY_SUMMARIZATION_PROMPT  # 从实体总结模块导入一个提示

# 这是微软公司的代码，遵循MIT许可证
# """这段文字是对这个代码块的简单描述，说明它做什么（用于提取和总结信息）"""

# 再次导入之前导入的那些东西，这样其他代码可以很容易地使用它们
from .community_report_summarization import COMMUNITY_REPORT_SUMMARIZATION_PROMPT
from .entity_extraction import (
    EXAMPLE_EXTRACTION_TEMPLATE,
    GRAPH_EXTRACTION_JSON_PROMPT,
    GRAPH_EXTRACTION_PROMPT,
    UNTYPED_EXAMPLE_EXTRACTION_TEMPLATE,
    UNTYPED_GRAPH_EXTRACTION_PROMPT,
)
from .entity_summarization import ENTITY_SUMMARIZATION_PROMPT

# 这个列表告诉其他人，这些是这个文件中可以使用的公共（重要）变量
__all__ = [  # 所有人都可以使用的代码片段列表
    "COMMUNITY_REPORT_SUMMARIZATION_PROMPT",
    "ENTITY_SUMMARIZATION_PROMPT",
    "EXAMPLE_EXTRACTION_TEMPLATE",
    "GRAPH_EXTRACTION_JSON_PROMPT",
    "GRAPH_EXTRACTION_PROMPT",
    "UNTYPED_EXAMPLE_EXTRACTION_TEMPLATE",
    "UNTYPED_GRAPH_EXTRACTION_PROMPT",
]

