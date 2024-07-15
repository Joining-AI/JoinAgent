# 导入Callable模块，这是一个Python内置的抽象基类，代表一个可以调用的对象，比如函数
from collections.abc import Callable

# 导入TypeAlias模块，这是Python的类型注解工具，用来创建类型别名
from typing import TypeAlias

# 这是一个版权声明，表示这段代码的版权属于2024年的微软公司
# 并且遵循MIT许可证的规定

# 这是一个文档字符串，描述了这个模块的功能
"""这是一个包含'LLMtype'模型的模块。"""

# 定义一个类型别名TextSplitter，它代表一个接受一个字符串并返回一个字符串列表的函数
TextSplitter: TypeAlias = Callable[[str], list[str]]

# 定义另一个类型别名TextListSplitter，它代表一个接受一个字符串列表并返回一个字符串列表的函数
TextListSplitter: TypeAlias = Callable[[list[str]], list[str]]

