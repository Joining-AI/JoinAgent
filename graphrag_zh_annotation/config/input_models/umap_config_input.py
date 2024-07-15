# 导入一个叫做NotRequired和TypedDict的特殊工具，它们帮助我们定义更清楚的数据类型
from typing_extensions import NotRequired, TypedDict

# 这段文字是版权信息，告诉我们这个代码是微软公司在2024年写的
# 并且它遵循MIT许可证的规则，但对我们现在的理解不重要

# 这是一个描述，说明下面的代码是用来设置默认配置参数的
"""Parameterization settings for the default configuration."""

# 再次导入NotRequired和TypedDict，确保我们有它们，即使前面已经导入了
from typing_extensions import NotRequired, TypedDict


# 定义一个叫做UmapConfigInput的类，它是一个特殊的字典，专门用来存储UMAP的设置
class UmapConfigInput(TypedDict):
    # 这个类里面有一个键叫做"enabled"
    """Configuration section for UMAP."""
    
    # "enabled"的值可以是不需要（NotRequired）、布尔值（True或False）、字符串或者None
    enabled: NotRequired[bool | str | None]

