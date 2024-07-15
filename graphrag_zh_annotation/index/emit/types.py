# 导入一个叫做 'Enum' 的特殊类，它帮助我们创建自己的枚举类型
from enum import Enum

# 这是一个注释，告诉我们这段代码的版权属于微软公司，2024年
# 并且代码使用了 MIT 许可证，这是一种允许他人自由使用、修改和分享代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是对下面定义的类的一个描述
# "Table Emitter Types" 意味着这是关于表格数据输出方式的类型

# 使用 'Enum' 类来创建一个新的类 'TableEmitterType'
# 这个类是基于字符串（str）的，同时也是一个枚举（Enum）
class TableEmitterType(str, Enum):
    # 这个类的说明，也是关于表格发射器的类型
    """Table Emitter Types."""

    # 定义枚举的成员，每个成员都是一个表格数据的输出格式
    # 'Json' 表示 JSON 格式
    Json = "json"
    # 'Parquet' 表示 Parquet 格式
    Parquet = "parquet"
    # 'CSV' 表示逗号分隔值（CSV）格式
    CSV = "csv"

