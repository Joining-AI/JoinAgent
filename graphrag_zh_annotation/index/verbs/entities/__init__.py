# 导入名为entity_extract的函数，它来自.extraction模块
from .extraction import entity_extract

# 导入名为summarize_descriptions的函数，它来自.summarize模块
from .summarize import summarize_descriptions

# 这是微软公司2024年的版权信息
# 许可证遵循MIT License
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个程序包是关于索引引擎中的实体处理
# "Indexing Engine entities package root"可以理解为“实体处理程序包的根目录”

# 再次导入entity_extract和summarize_descriptions，这次是为了公开这两个函数
# "__all__"变量告诉别人这个模块导出哪些内容
__all__ = ["entity_extract", "summarize_descriptions"]

