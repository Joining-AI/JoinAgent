# 导入两个Python库，它们帮助我们创建抽象类和定义数据类型
from abc import ABCMeta, abstractmethod
from typing import Any

# 这是一个版权信息，表示代码归微软公司所有，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块的描述，这个模块用于报告流程的状态
"""Status Reporter for orchestration."""

# 创建一个抽象类（Abstract Base Class），它的元类是ABCMeta
class StatusReporter(metaclass=ABCMeta):
    # 这个类提供了报告管道状态更新的方法

    # 定义一个抽象方法（必须在子类中实现）
    @abstractmethod
    def error(self, message: str, details: dict[str, Any] | None = None):
        # 报告一个错误
        pass

    # 另一个抽象方法
    @abstractmethod
    def warning(self, message: str, details: dict[str, Any] | None = None):
        # 报告一个警告
        pass

    # 再一个抽象方法
    @abstractmethod
    def log(self, message: str, details: dict[str, Any] | None = None):
        # 报告一条日志信息
        pass

# 创建一个具体类，继承自StatusReporter抽象类
class ConsoleStatusReporter(StatusReporter):
    # 这个类将状态报告到控制台

    # 实现error方法
    def error(self, message: str, details: dict[str, Any] | None = None):
        # 打印错误消息和详情（如果有的话）
        print(message, details)  # 注意：这里的"T201"是代码检查器的一个忽略标记

    # 实现warning方法
    def warning(self, message: str, details: dict[str, Any] | None = None):
        # 调用一个私有函数打印警告消息（用黄色高亮显示）
        _print_warning(message)

    # 实现log方法
    def log(self, message: str, details: dict[str, Any] | None = None):
        # 打印日志消息和详情（如果有的话）
        print(message, details)  # 注意：这里的"T201"是代码检查器的一个忽略标记

# 定义一个私有函数，用于打印带有黄色高亮的警告消息
def _print_warning(skk):
    # 使用特殊字符改变文本颜色（这里变为黄色）并打印警告消息
    print(f"\033[93m {skk}\033[00m")  # 注意：这里的"T201"是代码检查器的一个忽略标记

