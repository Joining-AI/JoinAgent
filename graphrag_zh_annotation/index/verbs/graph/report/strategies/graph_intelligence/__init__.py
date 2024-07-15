# 导入一个名为run的函数，它来自同一目录下的run_graph_intelligence模块。
from .run_graph_intelligence import run

# 这是一个版权声明，意味着2024年及以后，这个代码归微软公司所有。
# 版权许可遵循MIT许可证的规定。
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对这个代码包的描述，它是关于索引引擎图形报告策略的图形智能包的根目录。
"""The Indexing Engine graph report strategies graph intelligence package root."""

# 这一行告诉Python，我们希望这个模块外部可以访问'run'函数。
# 这样其他文件就可以通过导入这个包来使用run函数了。
from .run_graph_intelligence import run

# '__all__'变量告诉Python，当有人使用'*'从这个模块导入时，
# 只需要导出'run'这个名称。这样可以控制别人能访问哪些公开功能。
__all__ = ["run"]

