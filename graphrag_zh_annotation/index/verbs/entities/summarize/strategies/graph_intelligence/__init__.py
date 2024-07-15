# 导入名为run的函数，它来自同一目录下的run_graph_intelligence模块
from .run_graph_intelligence import run

# 这是一个版权声明，表示这段代码的版权归2024年的微软公司所有
# Licensed under the MIT License 表示这个代码遵循MIT许可证的规定

# 这个文件是Entity Resolution图形智能包的根目录，它是一个用来做实体解析的程序

# 再次从.run_graph_intelligence导入run函数，这样在这个文件的其他地方可以直接使用run
from .run_graph_intelligence import run

# '__all__'是一个特殊变量，这里它被设置为["run"]
# 这意味着当其他地方使用"from entity_resolution import *"时，只会导入并公开"run"这个名称
__all__ = ["run"]

