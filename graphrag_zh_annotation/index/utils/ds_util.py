# 导入特定类型的函数，让代码更规范
from typing import cast
# 导入datashaper库中的两个类
from datashaper import TableContainer, VerbInput

# 这是微软公司的版权信息和许可说明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个工具模块，包含与datashaper相关的实用方法

# 从typing导入cast函数，用于安全类型转换
from typing import cast

# 从datashaper导入两个类：TableContainer（用于存储表格数据）和VerbInput（可能与处理数据的操作有关）

# 定义一个错误消息，当需要命名输入但没有提供时使用
_NAMED_INPUTS_REQUIRED = "需要指定名称的输入"

# 函数1：获取一个必需的输入表格
def get_required_input_table(input: VerbInput, name: str) -> TableContainer:
    # 返回通过cast函数转换后的get_named_input_table函数的结果，确保返回类型为TableContainer
    return cast(TableContainer, get_named_input_table(input, name, required=True))

# 函数2：根据名称获取输入表格，可选参数表示是否必需
def get_named_input_table(
    input: VerbInput,  # 输入的数据操作对象
    name: str,  # 输入表格的名称
    required: bool = False  # 是否必需存在该输入，默认为False
) -> TableContainer | None:
    # 获取输入的命名部分
    named_inputs = input.named
    # 如果没有命名输入，检查是否必需
    if named_inputs is None:
        # 如果不是必需的，直接返回None
        if not required:
            return None
        # 如果必需但没有命名输入，抛出错误
        else:
            raise ValueError(_NAMED_INPUTS_REQUIRED)

    # 从命名输入中获取指定名称的表格
    result = named_inputs.get(name)
    # 如果必需但找不到指定名称的表格，抛出错误
    if result is None and required:
        # 构造错误消息，指出需要的输入表格
        msg = f"输入 '{name}' 是必需的"
        raise ValueError(msg)
    # 否则，返回找到的表格（可能是None）
    return result

