# 导入日志模块，用于记录程序运行信息
import logging

# 导入traceback模块，用于处理和打印异常堆栈信息
import traceback

# 导入pandas库，这是一个强大的数据处理库
import pandas as pd

# 从pyarrow库的lib模块导入两个错误类型，用于捕获可能的错误
from pyarrow.lib import ArrowInvalid, ArrowTypeError

# 导入PipelineStorage类，它可能是一个数据存储工具
from graphrag.index.storage import PipelineStorage

# 导入ErrorHandlerFn，它可能是一个错误处理函数的类型定义
from graphrag.index.typing import ErrorHandlerFn

# 导入TableEmitter类，可能是用于数据发布的基类
from .table_emitter import TableEmitter

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义ParquetTableEmitter模块

# 再次导入logging模块，创建一个名为当前模块名的日志记录器
log = logging.getLogger(__name__)

# 定义一个名为ParquetTableEmitter的类，继承自TableEmitter
class ParquetTableEmitter(TableEmitter):
    # 类内部的两个属性，分别存储PipelineStorage实例和错误处理函数
    _storage: PipelineStorage
    _on_error: ErrorHandlerFn

    # 初始化方法，当创建新对象时调用
    def __init__(self, storage: PipelineStorage, on_error: ErrorHandlerFn):
        # 将传入的存储对象和错误处理函数赋值给类的属性
        self._storage = storage
        self._on_error = on_error

    # 定义一个异步方法emit，用于将数据框（DataFrame）发送到存储
    async def emit(self, name: str, data: pd.DataFrame) -> None:
        # 生成一个.parquet格式的文件名
        filename = f"{name}.parquet"
        # 记录日志信息，表示正在发送parquet表格
        log.info("emitting parquet table %s", filename)

        # 尝试将数据框转换为parquet格式并保存到存储中
        try:
            await self._storage.set(filename, data.to_parquet())
        # 如果遇到ArrowTypeError，捕获并处理
        except ArrowTypeError as e:
            # 记录并打印异常信息
            log.exception("Error while emitting parquet table")
            # 调用错误处理函数，传递异常和堆栈信息
            self._on_error(e, traceback.format_exc(), None)
        # 如果遇到ArrowInvalid，同样捕获并处理
        except ArrowInvalid as e:
            # 记录并打印异常信息
            log.exception("Error while emitting parquet table")
            # 调用错误处理函数，传递异常和堆栈信息
            self._on_error(e, traceback.format_exc(), None)

