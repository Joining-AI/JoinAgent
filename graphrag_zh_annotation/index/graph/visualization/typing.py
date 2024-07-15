# 导入一个叫做 'dataclass' 的工具，它能帮助我们创建类并自动处理一些初始化的工作
from dataclasses import dataclass

# 这是版权信息，表示这段代码由微软公司拥有，2024年有效
# 并且它遵循MIT许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块是为了存储一个叫做 'NodePosition' 的模型，暂时用这个代替其他方法
"""A module containing 'NodePosition' model."""

# 再次导入 'dataclass'，因为我们需要用它来定义我们的类
from dataclasses import dataclass


# 使用 '@dataclass' 装饰器创建一个类，叫做 'NodePosition'
@dataclass
class NodePosition:
    # 这个类是用来描述一个节点的位置
    """Node position class definition."""

    # 节点的标签，是个字符串
    label: str
    # 节点所属的集群，也是个字符串
    cluster: str
    # 节点的大小，是个浮点数
    size: float

    # 节点在x轴上的位置，浮点数
    x: float
    # 节点在y轴上的位置，浮点数
    y: float
    # 节点在z轴上的位置，可能为空（None），默认为 None
    z: float | None = None

    # 定义一个方法，将节点位置转换成可以被Pandas库使用的格式
    def to_pandas(self) -> tuple[str, float, float, str, float]:
        """To pandas method definition."""
        # 返回一个元组，包含节点的标签、x坐标、y坐标、集群和大小
        return self.label, self.x, self.y, self.cluster, self.size


# 定义一个类型别名，'GraphLayout' 是一个包含多个 'NodePosition' 类型元素的列表
GraphLayout = list[NodePosition]

