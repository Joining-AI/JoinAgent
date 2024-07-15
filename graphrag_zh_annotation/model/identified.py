# 导入一个叫做"dataclass"的工具，它能帮助我们创建类并自动处理一些数据存储的事情。
from dataclasses import dataclass

# 这是代码的作者和版权信息，表示这段代码是微软公司2024年的作品。
# 它遵循MIT许可证，意味着你可以自由使用，但需要遵守一定的规则。
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个描述性文字，告诉我们这个代码包包含了'Identified'协议。
# "protocol"在这里可以理解为一种标准或约定。
"""

A package containing the 'Identified' protocol.

"""

# 再次导入"dataclass"，确保我们有这个工具来创建我们的类。
from dataclasses import dataclass


# 使用"dataclass"装饰器创建一个名为'Identified'的类，它是一个具有ID的项目协议。
@dataclass
class Identified:
    # 定义一个属性'id'，它是一个字符串，代表项目的唯一标识。
    id: str
    """这个字符串是项目的ID，用来唯一地识别它。"""

    # 定义另一个属性'short_id'，它可能是一个字符串，也可能为空（None）。
    # 这个ID是给人读的，比如在报告里显示，让用户更容易理解（可选的）。
    short_id: str | None
    """这是个人可以阅读的ID，用于在提示或显示给用户的文本中引用此项目，比如在报告文本里（可选）。"""

