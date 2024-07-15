# 导入一个叫做 SummarizationStrategy 的类，它来自当前模块内的 'typing' 子模块。
from .typing import SummarizationStrategy

# 这是版权声明，表示这段代码由微软公司于2024年创建。
# 它遵循的是 MIT 许可证的规定。
# 注：MIT 许可证是一种开源软件许可证，允许他人自由使用、修改和分发代码。

# 这个模块的文档字符串，描述了这是一个关于索引引擎中摘要策略的包。
"""这是一个索引引擎 - 摘要策略的包。"""

# 从 'typing' 中导入的 SummarizationStrategy 类，将会被其他使用这个包的代码所看到。
# '__all__' 变量告诉Python，当其他地方使用 "from package_name import *" 时，
# 应该导出哪些公开的（或可见的）名字。
__all__ = ["SummarizationStrategy"]

