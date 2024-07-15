# 导入一个名为run的函数，它来自同一目录下的run_gi_extract_claims模块
from .run_gi_extract_claims import run

# 这是一个版权声明，意味着2024年及以后，微软公司拥有这个代码的版权
# 版权信息后面跟着的是许可证类型，这里使用的是MIT许可证，允许他人自由使用、修改和分发代码，但需要保留原作者的版权信息

"""这是一个关于"Indexing Engine"的描述，它是处理文本并提取声明的策略包的根目录。
   "Graph Intelligence"可能指的是使用图形算法来理解信息。

# 下面这一行是告诉Python，当我们从这个包中导入时，只公开"run"这个函数，这样其他地方就可以直接使用它了
from .run_gi_extract_claims import run

# 这个 "__all__" 变量是一个列表，里面列出了我们想在"from package_name import *"时导出的模块成员
# 在这里，我们只想导出"run"，所以列表里只有一个"run"
__all__ = ["run"]

