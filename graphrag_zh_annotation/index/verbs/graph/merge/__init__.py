# 导入一个叫做 'merge_graphs' 的函数，它来自同一目录下的 'merge_graphs' 模块。
from .merge_graphs import merge_graphs

# 这是一个版权声明，意味着这个代码由微软公司创建，时间是2024年。
# 它遵循的是 MIT 许可证，这是一个允许他人自由使用、修改和分享代码的许可协议。

# 这个模块的文档字符串，简单说明这是一个关于图合并的索引引擎图形包的根目录。
# "Indexing Engine" 可能是一个程序的一部分，用来处理和合并图形数据。

# 再次导入 'merge_graphs' 函数，这样其他使用这个包的代码可以通过 'from indexing_engine.graph_merge import merge_graphs' 来访问它。
from .merge_graphs import merge_graphs

# '__all__' 是一个特殊变量，告诉 Python 当别人从这个模块导入 *（通配符导入）时，
# 应该只导出 'merge_graphs' 这个名字。这样可以防止意外导入模块中的其他内容。
__all__ = ["merge_graphs"]

