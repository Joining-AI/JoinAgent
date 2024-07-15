# 导入logging模块，它用来记录程序运行时的信息
import logging

# 导入pandas库，这是一个用于数据处理的库
import pandas as pd

# 从graphrag.index.storage导入PipelineStorage类，这个类可能用于存储数据管道
from graphrag.index.storage import PipelineStorage

# 从当前模块的.table_emitter导入TableEmitter类，这个类可能负责数据的发送
from .table_emitter import TableEmitter

# 这是微软公司的版权声明和许可证信息，不影响代码运行
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义CSVTableEmitter模块，里面有一个类

# 初始化日志模块，获取名为'__name__'（即当前模块名）的日志器
log = logging.getLogger(__name__)

# 定义一个名为CSVTableEmitter的类，它是TableEmitter类的子类
class CSVTableEmitter(TableEmitter):
    # _storage是一个类变量，类型是PipelineStorage，用于存储数据
    _storage: PipelineStorage

    # 构造函数，用于创建CSVTableEmitter对象
    def __init__(self, storage: PipelineStorage):
        # 将传入的storage参数赋值给类变量_self._storage
        self._storage = storage

    # 定义一个异步方法emit，用于发送数据框（DataFrame）到存储
    async def emit(self, name: str, data: pd.DataFrame) -> None:
        # 根据名字生成CSV文件的名称
        filename = f"{name}.csv"
        # 使用日志器记录信息，表示正在发送CSV表格
        log.info("emitting CSV table %s", filename)
        # 异步设置存储，将数据框转换成CSV格式并保存到存储中
        await self._storage.set(
            filename,  # 文件名
            data.to_csv(),  # 将DataFrame转换成CSV字符串
        )

