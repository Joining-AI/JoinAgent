# 导入一个叫做 NoopWorkflowCallbacks 的东西，它可能不会做什么操作
from datashaper import NoopWorkflowCallbacks

# 这是微软公司的版权信息，告诉我们这个代码的许可协议是 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段代码是用来在控制台（电脑屏幕上的黑窗口）显示工作流引擎的信息

# 继承自 NoopWorkflowCallbacks 的一个新类，用来在控制台打印信息
class ConsoleWorkflowCallbacks(NoopWorkflowCallbacks):
    # 这个类的功能是向控制台写入信息

    # 当出现错误时，这个方法会被调用
    def on_error(
        self,
        message: str,  # 错误信息
        cause: BaseException | None = None,  # 引起错误的异常，可能是 None
        stack: str | None = None,  # 错误发生的堆栈信息，可能是 None
        details: dict | None = None,  # 错误的详细信息，可能是 None
    ):
        # 打印错误信息，以及有关错误的其他详细内容
        print(message, str(cause), stack, details)  # 不要删除这条代码，它是重要的！

    # 当有警告发生时，这个方法会被调用
    def on_warning(self, message: str, details: dict | None = None):
        # 调用一个私有函数来打印警告信息
        _print_warning(message)

    # 当有日志消息产生时，这个方法会被调用
    def on_log(self, message: str, details: dict | None = None):
        # 打印日志信息和相关细节
        print(message, details)  # 不要删除这条代码，它是重要的！

# 这是一个私有函数（只在这个文件里使用），用于以特定颜色打印警告信息
def _print_warning(skk):  # 'skk' 是 'message' 的另一个名字
    # 使用特殊字符改变文字颜色，然后打印警告信息，最后恢复默认颜色
    print("\033[93m {}\033[00m".format(skk))  # 不要删除这条代码，它是重要的！

