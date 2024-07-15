# 导入两个有用的工具类，它们来自.description_summary_extractor模块
from .description_summary_extractor import (
    SummarizationResult,  # 这是一个用来存储总结结果的类
    SummarizeExtractor,  # 这是一个用来做总结的工具类
)

# 导入一个特定的提示（prompt），它来自.prompts模块
from .prompts import SUMMARIZE_PROMPT  # 这是一个用于提示总结的字符串

# 这是微软公司2024年的版权信息
# 它遵循MIT许可证，意味着你可以自由使用，但需要遵守一些规则

# 这个文件是"索引引擎单部分图包"的根目录描述

# 再次导入相同的两个工具类（可能是为了确保它们在其他地方可以被直接使用）
from .description_summary_extractor import (
    SummarizationResult,
    SummarizeExtractor,
)

# 定义一个公开的变量列表，这样其他文件可以通过这个名字访问这些工具
__all__ = ["SUMMARIZE_PROMPT", "SummarizationResult", "SummarizeExtractor"]

