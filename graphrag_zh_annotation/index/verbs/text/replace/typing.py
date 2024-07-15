# 导入一个叫做"dataclass"的工具，它能帮助我们创建类并自动添加一些默认的方法
from dataclasses import dataclass

# 这是一个版权声明，说明这段代码是微软公司2024年的作品
# 并且它遵循MIT许可证的规定，允许他人在一定条件下使用

# 这个文件是一个模块，里面有一个名为'Replacement'的模型
# 模块是一种组织代码的方式，可以把它想象成一个小图书馆

# 再次导入"dataclass"，因为我们需要用到它来定义我们的类
from dataclasses import dataclass


# 使用"dataclass"装饰器定义一个名为'Replacement'的类
@dataclass
class Replacement:
    # 在这个类里面，我们有两个东西，叫做"pattern"和"replacement"
    # "pattern"是一个字符串，用来存放要替换的文本模式
    pattern: str

    # "replacement"也是一个字符串，用来存放替换后的新文本
    replacement: str

