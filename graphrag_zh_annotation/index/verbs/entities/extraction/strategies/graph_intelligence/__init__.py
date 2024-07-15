# 导入名为run_gi的函数，它来自同一目录下的run_graph_intelligence模块
from .run_graph_intelligence import run_gi

# 这是一个版权声明，说明代码的版权属于2024年的微软公司
# 并且代码遵循MIT许可证的规定，这是一种允许他人自由使用、修改和分享代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对这个代码包的简单描述，它说这是一个关于图智能索引引擎的包
"""The Indexing Engine graph intelligence package root."""

# 再次导入run_graph_intelligence中的run_gi函数，这样其他使用这个包的代码可以直接通过这个文件访问到它
from .run_graph_intelligence import run_gi

# 这个列表告诉其他程序，这个模块中可以公开使用的部分（导出的）只有"run_gi"这个函数
__all__ = ["run_gi"]

