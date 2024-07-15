# 导入json模块，用于处理JSON格式的数据
import json
# 导入logging模块，用于记录日志信息
import logging
# 从io模块导入TextIOWrapper，用于读写文本文件
from io import TextIOWrapper
# 从pathlib模块导入Path，用于处理文件路径
from pathlib import Path
# 导入NoopWorkflowCallbacks类，它可能是一个不做任何操作的回调函数
from datashaper import NoopWorkflowCallbacks

# 这是代码的版权信息和许可声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个类，名为FileWorkflowCallbacks，它会将信息写入文件
class FileWorkflowCallbacks(NoopWorkflowCallbacks):
    # 类变量_out_stream，类型为TextIOWrapper，用于写入数据
    _out_stream: TextIOWrapper

    # 初始化方法，当创建FileWorkflowCallbacks对象时调用
    def __init__(self, directory: str):
        # 创建或确认目录存在
        Path(directory).mkdir(parents=True, exist_ok=True)
        # 打开或追加到"logs.json"文件，以UTF-8编码
        self._out_stream = open(  # 不要删除这条代码，SIM115是关于代码风格的提示
            Path(directory) / "logs.json", "a", encoding="utf-8"
        )

    # 当发生错误时调用的方法
    def on_error(
        self,
        message: str,
        cause: BaseException | None = None,
        stack: str | None = None,
        details: dict | None = None,
    ):
        # 将错误信息写入文件
        self._out_stream.write(
            json.dumps({
                "type": "error",
                "data": message,
                "stack": stack,
                "source": str(cause),
                "details": details,
            }) + "\n"
        )
        # 记录带有详细信息的日志
        message = f"{message} details={details}"
        log.info(message)

    # 当发生警告时调用的方法
    def on_warning(self, message: str, details: dict | None = None):
        # 将警告信息写入文件
        self._out_stream.write(
            json.dumps({"type": "warning", "data": message, "details": details}) + "\n"
        )
        # 调用私有方法打印警告
        _print_warning(message)

    # 当有日志消息时调用的方法
    def on_log(self, message: str, details: dict | None = None):
        # 将日志信息写入文件
        self._out_stream.write(
            json.dumps({"type": "log", "data": message, "details": details}) + "\n"
        )
        # 记录带有详细信息的日志
        message = f"{message} details={details}"
        log.info(message)

# 私有方法，用于打印警告信息
def _print_warning(skk):
    # 使用logging模块记录警告信息
    log.warning(skk)

