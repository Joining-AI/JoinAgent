# 导入两个特殊类型的模块，用于定义字典里的数据类型
from typing_extensions import NotRequired, TypedDict
# 这是版权信息，意味着这个代码由微软公司在2024年拥有
# 并且遵循MIT许可证的规定

# 这个文档字符串描述了这段代码的作用，关于默认配置的参数设置
"""

# 再次导入NotRequired和TypedDict，确保它们在下面的类中可以使用
from typing_extensions import NotRequired, TypedDict


# 定义一个类，叫做SnapshotsConfigInput，它是一个特殊的字典，用来存储快照的配置信息
class SnapshotsConfigInput(TypedDict):
    # 这个注释说明了这一部分配置是关于快照的
    """快照相关的配置设置"""

    # 定义字典中的一个键，叫做graphml，它的值可以是不需要（NotRequired）、布尔值、字符串或None
    graphml: NotRequired[bool | str | None]

    # 定义字典中的另一个键，叫做raw_entities，它的值也可以是不需要（NotRequired）、布尔值、字符串或None
    raw_entities: NotRequired[bool | str | None]

    # 定义字典中的第三个键，叫做top_level_nodes，同样可以是不需要（NotRequired）、布尔值、字符串或None
    top_level_nodes: NotRequired[bool | str | None]

