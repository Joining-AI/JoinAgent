# 导入基础类和抽象方法
from abc import ABC, abstractmethod
# 导入一个叫做Progress的工具，可能用来追踪进度
from datashaper import Progress

# 这个是微软公司的版权信息，告诉我们这个代码受MIT许可证保护
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个关于报告状态的类型（类）
"""Types for status reporting."""

# 从abc模块导入抽象基类（ABC）和抽象方法（abstractmethod）

# 创建一个名为ProgressReporter的抽象基类
class ProgressReporter(ABC):
    """
    这是一个用来报告工作流程进度的抽象类。
    它能通过像进度条这样的方式显示进度。
    """

    # 这是一个特殊的方法，当用对象调用时（比如`progress_reporter(update)`）会执行
    @abstractmethod
    def __call__(self, update: Progress):
        """更新进度。"""

    # 这个方法是用来清理或关闭进度报告器的
    @abstractmethod
    def dispose(self):
        """清理并结束进度报告器的使用。"""

    # 创建一个新的子进度条，可以有前缀，并可以选择是否临时
    @abstractmethod
    def child(self, prefix: str, transient=True) -> "ProgressReporter":
        """创建带有前缀的子进度条。"""

    # 强制刷新当前的进度显示
    @abstractmethod
    def force_refresh(self) -> None:
        """强制更新进度条。"""

    # 停止进度报告器的工作
    @abstractmethod
    def stop(self) -> None:
        """停止进度报告。"""

    # 报告错误信息
    @abstractmethod
    def error(self, message: str) -> None:
        """报告一个错误。"""

    # 报告警告信息
    @abstractmethod
    def warning(self, message: str) -> None:
        """报告一个警告。"""

    # 报告一般信息
    @abstractmethod
    def info(self, message: str) -> None:
        """报告一条信息。"""

    # 报告操作成功
    @abstractmethod
    def success(self, message: str) -> None:
        """报告操作成功。"""

# 定义一个名为NullProgressReporter的类，它是ProgressReporter类的子类
class NullProgressReporter(ProgressReporter):
    """这是一个什么也不做的进度报告器。"""

    # 当这个类的对象被当作函数调用时（比如progress_reporter(update)），会执行这个方法
    def __call__(self, update: Progress) -> None:
        """更新进度，但其实什么也不会做."""

    # 清理进度报告器的资源，但在这个类里没有实际操作
    def dispose(self) -> None:
        """清理这个进度报告器，但不做任何事情."""

    # 创建一个新的子进度条，但这个版本只是返回它自己，不做任何改变
    def child(self, prefix: str, transient: bool = True) -> ProgressReporter:
        """创建一个子进度条，但其实还是返回当前的进度报告器对象."""

    # 强制刷新进度，但在这个类里没有实际效果
    def force_refresh(self) -> None:
        """强制刷新进度，但实际上不会做任何事情."""

    # 停止进度报告，但在这个类里没有实际操作
    def stop(self) -> None:
        """停止进度报告，但其实什么也不会做."""

    # 报告一个错误，但在这个类里没有实际显示
    def error(self, message: str) -> None:
        """报告一个错误，但不会真正显示信息."""

    # 报告一个警告，但在这个类里没有实际显示
    def warning(self, message: str) -> None:
        """报告一个警告，但不会真正显示信息."""

    # 报告一条信息，但在这个类里没有实际显示
    def info(self, message: str) -> None:
        """报告一条信息，但不会真正显示信息."""

    # 报告成功，但在这个类里没有实际显示
    def success(self, message: str) -> None:
        """报告成功，但不会真正显示信息."""

# 定义一个名为PrintProgressReporter的类，它继承自ProgressReporter类
class PrintProgressReporter(ProgressReporter):
    """这个类的作用是记录进度，但不会做任何实际操作"""

    # 类中有一个属性，叫做prefix，它是用来存放前缀字符串的
    prefix: str

    # 这个方法叫做构造函数，当创建一个新的PrintProgressReporter对象时会自动调用
    def __init__(self, prefix: str):
        """创建一个新的进度报告器"""
        # 把传入的前缀字符串赋值给对象的prefix属性
        self.prefix = prefix
        # 打印前缀，后面不换行
        print(f"\n{self.prefix}", end="")  # 不要删除这条代码，它用于显示进度开始

    # 当调用这个对象时，就像调用一个函数一样，就会执行这个方法
    def __call__(self, update: Progress) -> None:
        """更新进度"""
        # 打印一个点，表示进度在前进，后面也不换行
        print(".", end="")  # 不要删除这条代码，它用于显示进度更新

    # 这个方法没有实际操作，可能用来清理或结束进度报告
    def dispose(self) -> None:
        """释放或结束进度报告器"""

    # 创建一个新的子进度条
    def child(self, prefix: str, transient: bool = True) -> "ProgressReporter":
        """创建带有新前缀的子进度条"""
        # 返回一个新的PrintProgressReporter对象，用新的前缀
        return PrintProgressReporter(prefix)

    # 停止当前的进度报告
    def stop(self) -> None:
        """停止进度报告器"""

    # 强制刷新进度显示
    def force_refresh(self) -> None:
        """强制更新进度信息"""

    # 报告错误
    def error(self, message: str) -> None:
        """报告一个错误"""
        # 打印错误信息，前面加上前缀和"ERROR:"
        print(f"\n{self.prefix}ERROR: {message}")  # 不要删除这条代码，它用于显示错误

    # 报告警告
    def warning(self, message: str) -> None:
        """报告一个警告"""
        # 打印警告信息，前面加上前缀和"WARNING:"
        print(f"\n{self.prefix}WARNING: {message}")  # 不要删除这条代码，它用于显示警告

    # 报告信息
    def info(self, message: str) -> None:
        """报告一些信息"""
        # 打印信息，前面加上前缀和"INFO:"
        print(f"\n{self.prefix}INFO: {message}")  # 不要删除这条代码，它用于显示信息

    # 报告成功
    def success(self, message: str) -> None:
        """报告一个成功事件"""
        # 打印成功信息，前面加上前缀和"SUCCESS:"
        print(f"\n{self.prefix}SUCCESS: {message}")  # 不要删除这条代码，它用于显示成功

