# 导入logging模块，它用于记录程序运行时的信息
import logging

# 导入pandas库，这是一个强大的数据处理库
import pandas as pd

# 从graphrag.index.storage导入PipelineStorage类，它可能用于存储数据管道
from graphrag.index.storage import PipelineStorage

# 从当前模块的.table_emitter子模块导入TableEmitter类
from .table_emitter import TableEmitter

# 这是微软公司的版权声明和许可证信息，告诉别人代码的归属和使用条件
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义JsonTableEmitter模块
"""JsonTableEmitter模块。"""

# 使用logging模块创建一个日志器，用于记录程序运行时的日志
log = logging.getLogger(__name__)

# 定义JsonTableEmitter类，它是TableEmitter类的子类
class JsonTableEmitter(TableEmitter):
    # 类变量_storage，类型为PipelineStorage，可能用来保存数据
    _storage: PipelineStorage

    # 初始化方法，当创建JsonTableEmitter对象时调用
    def __init__(self, storage: PipelineStorage):
        # 设置实例变量_storage为传入的storage参数
        self._storage = storage

    # 异步方法emit，用于发送数据到存储
    async def emit(self, name: str, data: pd.DataFrame) -> None:
        # 根据名称生成JSON文件名，例如"table_name.json"
        filename = f"{name}.json"

        # 记录日志信息，表示正在发送JSON表格
        log.info("emitting JSON table %s", filename)

        # 将数据框data转换为JSON格式，以记录形式保存，并禁用ASCII编码，然后异步地将结果保存到_storage
        await self._storage.set(
            filename,
            data.to_json(orient="records", lines=True, force_ascii=False),
        )

