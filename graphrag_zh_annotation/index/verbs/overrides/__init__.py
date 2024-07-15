# 导入aggregate模块，这个模块有关于数据聚合的功能
from .aggregate import aggregate

# 导入concat模块，这个模块用于连接或组合数据
from .concat import concat

# 导入merge模块，这个模块帮助合并不同的数据集
from .merge import merge

# 这是一个版权声明，表示代码由微软公司创作，2024年时有效
# 并且遵循MIT许可证的规定

# 这段文字是对这个包的描述，它说这个"Indexing Engine"包覆盖了主要功能

# 再次导入aggregate, concat, merge，确保这些函数可以在包的外部被直接使用
from .aggregate import aggregate
from .concat import concat
from .merge import merge

# 这个列表(__all__)告诉Python，哪些名字（如aggregate, concat, merge）应该在引入这个包时导出
# 这样别人使用时可以直接写"import package_name"而不必写具体的函数名
__all__ = ["aggregate", "concat", "merge"]

