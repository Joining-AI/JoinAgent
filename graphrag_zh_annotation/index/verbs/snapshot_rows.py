# 导入json模块，用于处理JSON格式的数据
import json

# 导入dataclass装饰器，用于定义数据类
from dataclasses import dataclass

# 导入Any类型提示，表示可以是任何类型
from typing import Any

# 导入TableContainer、VerbInput和verb，它们是数据处理相关的类和装饰器
from datashaper import TableContainer, VerbInput, verb

# 导入PipelineStorage，用于存储数据管道
from graphrag.index.storage import PipelineStorage

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为'FormatSpecifier'的模块，包含一个数据类

# 数据类定义，用于存储格式和扩展名
@dataclass
class FormatSpecifier:
    # 格式字符串
    format: str
    # 文件扩展名
    extension: str

# 定义一个名为'snapshot_rows'的异步函数，用于按行保存表格数据
@verb(name="snapshot_rows")  # 装饰器，表示这是一个数据处理操作
async def snapshot_rows(
    input: VerbInput,  # 输入的数据
    column: str | None,  # 指定要保存的列名，可选
    base_name: str,  # 基础文件名
    storage: PipelineStorage,  # 存储对象
    formats: list[str | dict[str, Any]],  # 保存数据的格式列表
    row_name_column: str | None = None,  # 用于生成行名的列名，可选，默认为None
    **_kwargs: dict,  # 其他关键字参数，这里不使用
) -> TableContainer:  # 返回值类型为TableContainer
    # 获取输入数据
    data = input.get_input()
    # 解析格式列表
    parsed_formats = _parse_formats(formats)
    # 计算数据行数
    num_rows = len(data)

    # 定义一个函数，根据行数据和索引生成行名
    def get_row_name(row: Any, row_idx: Any):
        if row_name_column is None:
            # 如果没有指定行名列，当只有一行时返回基础名，否则返回基础名加索引
            return base_name if num_rows == 1 else f"{base_name}.{row_idx}"
        # 如果指定了行名列，返回基础名加该列的值
        return f"{base_name}.{row[row_name_column]}"

    # 遍历每一行
    for row_idx, row in data.iterrows():
        # 遍历每一种格式
        for fmt in parsed_formats:
            # 使用上面的函数生成行名
            row_name = get_row_name(row, row_idx)
            # 获取当前格式的扩展名
            extension = fmt.extension
            # 如果格式是"json"，保存列数据或整个行数据到存储
            if fmt.format == "json":
                # 如果指定了列名，保存该列的JSON数据，否则保存整个行的JSON数据
                await storage.set(
                    f"{row_name}.{extension}",
                    json.dumps(row[column]) if column is not None else json.dumps(row.to_dict()),
                )
            # 如果格式是"text"，保存列数据（必须指定列名）
            elif fmt.format == "text":
                if column is None:
                    # 如果没有指定列名，抛出错误
                    msg = "column must be specified for text format"
                    raise ValueError(msg)
                # 保存指定列的文本数据
                await storage.set(f"{row_name}.{extension}", str(row[column]))

    # 返回原始数据表格
    return TableContainer(table=data)

# 定义一个函数，名为_parse_formats，接收一个参数formats，它是一个包含字符串或字典的列表
def _parse_formats(formats: list[str | dict[str, Any]]) -> list[FormatSpecifier]:
    # 这个函数的作用是将格式列表转换成一个FormatSpecifier对象的列表
    """将格式解析成FormatSpecifier对象的列表."""
    # 使用for循环遍历列表中的每个fmt
    return [
        # 如果fmt是一个字典，就用星号(*)展开它，创建一个新的FormatSpecifier对象
        FormatSpecifier(**fmt)
        # 如果fmt不是一个字典，而是一个字符串，那么创建FormatSpecifier对象，设置format属性为fmt，extension属性通过_get_format_extension函数获取
        if isinstance(fmt, dict)
        else FormatSpecifier(format=fmt, extension=_get_format_extension(fmt))
        # 这里结束for循环的条件语句
        for fmt in formats
    ]

# 定义另一个函数，名为_get_format_extension，接收一个参数fmt，它是一个字符串
def _get_format_extension(fmt: str) -> str:
    # 这个函数的作用是根据给定的格式返回对应的文件扩展名
    """根据给定的格式获取文件扩展名."""
    # 如果fmt是"json"，返回"json"作为扩展名
    if fmt == "json":
        return "json"
    # 如果fmt是"text"，返回"txt"作为扩展名
    if fmt == "text":
        return "txt"
    # 如果fmt是"parquet"，返回"parquet"作为扩展名
    if fmt == "parquet":
        return "parquet"
    # 如果fmt是"csv"，返回"csv"作为扩展名
    if fmt == "csv":
        return "csv"
    # 如果fmt不是以上四种格式，构造一个错误消息并抛出ValueError异常
    msg = f"未知的格式：{fmt}"
    raise ValueError(msg)

