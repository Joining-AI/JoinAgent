# 导入一些工具模块，这些模块帮助我们处理数据和错误
from graphrag.index.storage import PipelineStorage  # 用于存储数据的类
from graphrag.index.typing import ErrorHandlerFn  # 定义处理错误的函数类型

# 导入不同格式的数据发射器（将数据输出为特定格式的类）
from .csv_table_emitter import CSVTableEmitter  # CSV格式
from .json_table_emitter import JsonTableEmitter  # JSON格式
from .parquet_table_emitter import ParquetTableEmitter  # Parquet格式
from .table_emitter import TableEmitter  # 基础的数据发射器类
from .types import TableEmitterType  # 定义数据发射器类型的枚举

# 这是版权信息，表示代码由微软公司编写，遵循MIT许可证

# 这个文件是用来创建不同类型的表数据发射器的工厂

# 从graphrag.index.storage导入PipelineStorage
# 从graphrag.index.typing导入ErrorHandlerFn（错误处理函数的类型）

# 导入不同格式的数据发射器
# 从.csv_table_emitter导入CSVTableEmitter（用于CSV格式）
# 从.json_table_emitter导入JsonTableEmitter（用于JSON格式）
# 从.parquet_table_emitter导入ParquetTableEmitter（用于Parquet格式）
# 从.table_emitter导入TableEmitter（基础的数据发射器类）
# 从.types导入TableEmitterType（数据发射器类型的枚举）

# 创建一个特定类型的数据发射器
def create_table_emitter(
    emitter_type: TableEmitterType,  # 输入的数据发射器类型
    storage: PipelineStorage,  # 存储数据的地方
    on_error: ErrorHandlerFn,  # 发生错误时调用的函数
) -> TableEmitter:  # 返回的数据发射器对象
    """根据指定的类型创建一个数据发射器"""
    # 使用类型匹配来决定创建哪种数据发射器
    if emitter_type == TableEmitterType.Json:  # 如果是JSON类型
        return JsonTableEmitter(storage)  # 创建JSON数据发射器
    elif emitter_type == TableEmitterType.Parquet:  # 如果是Parquet类型
        return ParquetTableEmitter(storage, on_error)  # 创建Parquet数据发射器并传入错误处理函数
    elif emitter_type == TableEmitterType.CSV:  # 如果是CSV类型
        return CSVTableEmitter(storage)  # 创建CSV数据发射器
    else:  # 其他未支持的类型
        # 创建一个错误消息
        msg = f"不支持的数据发射器类型：{emitter_type}"
        # 抛出一个值错误
        raise ValueError(msg)

# 根据指定的类型列表创建多个数据发射器
def create_table_emitters(
    emitter_types: list[TableEmitterType],  # 输入的数据发射器类型列表
    storage: PipelineStorage,  # 存储数据的地方
    on_error: ErrorHandlerFn,  # 发生错误时调用的函数
) -> list[TableEmitter]:  # 返回的数据发射器对象列表
    """根据指定的类型列表创建一个数据发射器列表"""
    # 遍历类型列表，为每种类型创建一个数据发射器并添加到列表中
    return [
        create_table_emitter(emitter_type, storage, on_error)  # 创建并添加数据发射器
        for emitter_type in emitter_types  # 对于列表中的每个类型
    ]

