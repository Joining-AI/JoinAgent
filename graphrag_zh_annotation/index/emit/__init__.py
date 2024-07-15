# 导入csv_table_emitter模块中的CSVTableEmitter类
from .csv_table_emitter import CSVTableEmitter

# 导入factories模块中的create_table_emitter和create_table_emitters函数
from .factories import create_table_emitter, create_table_emitters

# 导入json_table_emitter模块中的JsonTableEmitter类
from .json_table_emitter import JsonTableEmitter

# 导入parquet_table_emitter模块中的ParquetTableEmitter类
from .parquet_table_emitter import ParquetTableEmitter

# 导入table_emitter模块中的TableEmitter类
from .table_emitter import TableEmitter

# 导入types模块中的TableEmitterType枚举类型
from .types import TableEmitterType

# 这是微软公司的版权信息，表示代码的使用权受MIT许可证限制
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对这个文件功能的简单描述
"""定义了将管道艺术品（可能是数据）存储到存储区的方法。"""

# 再次导入相同的模块，但在这里是为了指定对外公开的接口（这些可以被其他程序使用）
from .csv_table_emitter import CSVTableEmitter
from .factories import create_table_emitter, create_table_emitters
from .json_table_emitter import JsonTableEmitter
from .parquet_table_emitter import ParquetTableEmitter
from .table_emitter import TableEmitter
from .types import TableEmitterType

# 这是一个列表，包含了所有对外公开的类和函数
__all__ = [
    "CSVTableEmitter",   # CSV格式的数据发射器类
    "JsonTableEmitter",  # JSON格式的数据发射器类
    "ParquetTableEmitter",  # Parquet格式的数据发射器类
    "TableEmitter",     # 基础的数据发射器类
    "TableEmitterType",  # 数据发射器类型的枚举
    "create_table_emitter",  # 创建单个数据发射器的函数
    "create_table_emitters",  # 创建多个数据发射器的函数
]

