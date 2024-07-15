# 导入名为 'layout_graph' 的函数来自同一目录下的 'layout_graph' 模块
from .layout_graph import layout_graph

# 这一行是版权声明，告诉我们这段代码的版权属于2024年的微软公司
# Licensed under the MIT License 表示这个代码使用了MIT许可证，允许他人自由使用、修改和分享，只要保留原作者的版权信息

# 这个模块的文档字符串，简单描述这是一个图形布局包的根目录
"""这个是索引引擎图形布局包的根模块。"""

# 再次导入 'layout_graph'，确保它在这个模块中可以被外部访问
from .layout_graph import layout_graph

# '__all__' 是一个特殊变量，这里列出的 ['layout_graph'] 表示当别人从这个模块导入时，只公开 'layout_graph' 这个名字
__all__ = ["layout_graph"]

