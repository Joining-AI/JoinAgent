# 导入一个叫做 'dataclass' 的工具，它帮助我们创建类时自动添加默认构造函数和其他功能
from dataclasses import dataclass

# 从当前文件夹中的 'identified' 模块导入 'Identified' 类
from .identified import Identified

# 这是版权声明，说明代码由微软公司拥有，使用了 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个描述性文字，告诉我们这个包包含了 'Named' 协议
# """A package containing the 'Named' protocol."""

# 再次导入 'dataclass' 工具，确保我们不会忘记
from dataclasses import dataclass

# 从 'identified' 模块导入 'Identified' 类（这是重复的，但保留以保持原样）
from .identified import Identified

# 使用 'dataclass' 装饰器创建一个新的类 'Named'，它继承自 'Identified' 类
@dataclass
class Named(Identified):
    # 这个类表示一个有名字或标题的物品
    # 'title' 是一个字符串类型的属性，代表物品的名字或标题
    title: str
    # 这是 'title' 属性的描述，告诉别人这个属性是关于什么的
    """The name/title of the item."""

