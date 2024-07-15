# 导入一些类，这些类是用来描述数据模型的
from .community import Community  # 导入社区类
from .community_report import CommunityReport  # 导入社区报告类
from .covariate import Covariate  # 导入协变量类
from .document import Document  # 导入文档类
from .entity import Entity  # 导入实体类
from .identified import Identified  # 导入已识别类
from .named import Named  # 导入命名类
from .relationship import Relationship  # 导入关系类
from .text_unit import TextUnit  # 导入文本单元类

# 这是微软公司的版权信息，表示代码的使用权
# Copyright (c) 2024 Microsoft Corporation.  # 微软公司2024年的版权
# Licensed under the MIT License  # 使用MIT许可证授权

# 这段文字说明了这个代码包是关于什么的
"""
GraphRAG知识模型包的根目录。

GraphRAG知识模型包含一组类，用于表示我们管道和分析工具的目标数据模型。
你可以根据需要扩展和整合这些模型到自己的数据基础设施中。
"""

# 再次导入之前的一些类，这看起来重复，但可能有特定用途，比如确保导出
from .community import Community
from .community_report import CommunityReport
from .covariate import Covariate
from .document import Document
from .entity import Entity
from .identified import Identified
from .named import Named
from .relationship import Relationship
from .text_unit import TextUnit

# 这个列表告诉别人这个包里有哪些重要的东西可以被外部使用
__all__ = [  # 所有公开的类名都在这里
    "Community",
    "CommunityReport",
    "Covariate",
    "Document",
    "Entity",
    "Identified",
    "Named",
    "Relationship",
    "TextUnit",
]

