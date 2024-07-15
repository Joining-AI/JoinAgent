# 导入两个特殊类型的模块，它们帮助我们定义数据结构
from typing_extensions import NotRequired, TypedDict
# 这是版权信息，表示代码归微软公司所有，2024年
# 许可证是MIT License，允许他人自由使用和修改代码，只要保留原作者信息

# 这是一个文档字符串，描述了这段代码的作用
"""这是默认配置的参数设置模块。"""

# 再次导入NotRequired和TypedDict，确保它们被正确使用
from typing_extensions import NotRequired, TypedDict


# 定义一个类，叫做ClusterGraphConfigInput，它是一个字典类型的数据结构
class ClusterGraphConfigInput(TypedDict):
    # 这个类里有一个键叫'max_cluster_size'
    # 其对应的值可以是不需要（NotRequired）的整数或None
    max_cluster_size: NotRequired[int | None]

    # 另一个键是'strategy'
    # 它的值也可以是不需要（NotRequired）的字典或None
    strategy: NotRequired[dict | None]

