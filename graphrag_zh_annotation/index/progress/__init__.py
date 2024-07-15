# 导入模块中的类，这些类可以帮助我们报告进度
from .types import NullProgressReporter, PrintProgressReporter, ProgressReporter

# 这是版权声明，说明代码的版权归2024年的微软公司所有
# Licensed under the MIT License 表示代码遵循MIT许可证，允许他人使用和修改，但需要遵守一定的规则

# 这段文字是对这个代码文件的描述，它说这里是关于进度报告的组件
"""Progress-reporting components."""

# 这一行告诉Python，当其他人导入这个模块时，他们可以使用这三个类
# NullProgressReporter: 不显示任何进度的报告器
# PrintProgressReporter: 打印进度到屏幕的报告器
# ProgressReporter: 一个通用的进度报告器类
__all__ = ["NullProgressReporter", "PrintProgressReporter", "ProgressReporter"]

