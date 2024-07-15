# 导入一些函数，帮助我们生成不同的信息
from .community_report_rating import generate_community_report_rating
# 这个函数是用来给社区报告打分的

from .community_report_summarization import create_community_summarization_prompt
# 这个函数创建一个提示，用来总结社区报告

from .community_reporter_role import generate_community_reporter_role
# 这个函数生成关于社区报告者角色的信息

from .defaults import MAX_TOKEN_COUNT
# 从这里导入一个常量，表示最大的单词计数

from .domain import generate_domain
# 这个函数帮助我们生成一个领域或主题

from .entity_extraction_prompt import create_entity_extraction_prompt
# 创建一个提示，用于提取文本中的关键信息（实体）

from .entity_relationship import generate_entity_relationship_examples
# 生成示例，展示实体之间的关系

from .entity_summarization_prompt import create_entity_summarization_prompt
# 创建一个提示，用于总结文本中的实体

from .entity_types import generate_entity_types
# 这个函数可以生成不同类型的实体

from .language import detect_language
# 这个函数检测文本的语言

from .persona import generate_persona
# 生成一个人物角色的描述

# 这是一个版权信息，告诉我们这个代码由微软公司拥有
# 并且遵循MIT许可证

# 这个模块的文档字符串，描述了它的用途
"""这是一个用于生成提示的模块。"""

# 将这些函数公开，让其他地方的代码可以使用
__all__ = [
    "MAX_TOKEN_COUNT",
    "create_community_summarization_prompt",
    "create_entity_extraction_prompt",
    "create_entity_summarization_prompt",
    "detect_language",
    "generate_community_report_rating",
    "generate_community_reporter_role",
    "generate_domain",
    "generate_entity_relationship_examples",
    "generate_entity_types",
    "generate_persona",
]
# 这里列出的是模块对外提供的功能列表

