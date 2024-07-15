# 导入来自另一个模块的特定提示信息
from .community_report_rating import GENERATE_REPORT_RATING_PROMPT  # 引入社区报告评分提示
from .community_reporter_role import GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT  # 引入社区报告者角色提示
from .domain import GENERATE_DOMAIN_PROMPT  # 引入领域生成提示
from .entity_relationship import (  # 关于实体关系的提示
    ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT,
    ENTITY_RELATIONSHIPS_GENERATION_PROMPT,
    UNTYPED_ENTITY_RELATIONSHIPS_GENERATION_PROMPT,
)
from .entity_types import (  # 关于实体类型的提示
    ENTITY_TYPE_GENERATION_JSON_PROMPT,
    ENTITY_TYPE_GENERATION_PROMPT,
)
from .language import DETECT_LANGUAGE_PROMPT  # 引入检测语言提示
from .persona import GENERATE_PERSONA_PROMPT  # 引入生成人物设定提示

# 这个模块的注释：包含了关于生成人物、实体类型、关系和领域等的提示信息
# 版权声明：2024年微软公司，根据MIT许可证授权

# 把之前导入的所有提示信息列出来，方便其他地方使用
__all__ = [
    "DETECT_LANGUAGE_PROMPT",  # 检测语言提示
    "ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT",  # 实体关系JSON生成提示
    "ENTITY_RELATIONSHIPS_GENERATION_PROMPT",  # 实体关系生成提示
    "ENTITY_TYPE_GENERATION_JSON_PROMPT",  # 实体类型JSON生成提示
    "ENTITY_TYPE_GENERATION_PROMPT",  # 实体类型生成提示
    "GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT",  # 社区报告者角色生成提示
    "GENERATE_DOMAIN_PROMPT",  # 领域生成提示
    "GENERATE_PERSONA_PROMPT",  # 人物设定生成提示
    "GENERATE_REPORT_RATING_PROMPT",  # 报告评分生成提示
    "UNTYPED_ENTITY_RELATIONSHIPS_GENERATION_PROMPT",  # 未分类实体关系生成提示
]

