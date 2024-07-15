# 导入需要的库，typing库用于类型注解，pandas库用于数据处理，datashaper库用于数据操作
from typing import cast
import pandas as pd
from datashaper import TableContainer, VerbInput, verb

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个包含ds_zip方法定义的模块
# from typing import cast 保持不变，这是Python的类型注解库
# import pandas as pd 保持不变，这是Python的数据处理库Pandas
# from datashaper import TableContainer, VerbInput, verb 保持不变，这是datashaper库的数据操作相关类和装饰器

# 定义一个名为"zip"的verb（数据操作）
@verb(name="zip")
def zip_verb(  # 这个函数用于合并列
    input: VerbInput,  # 输入数据
    to: str,  # 新列的名称
    columns: list[str],  # 要合并的列名列表
    type: str | None = None,  # 合并方式，默认为None
    **_kwargs: dict,  # 其他未命名的参数，这里我们不需要用到
) -> TableContainer:  # 函数返回一个新的TableContainer对象

    # 获取输入数据，转换为DataFrame格式
    table = cast(pd.DataFrame, input.get_input())

    # 如果没有指定合并方式（type为None），则使用默认方式
    if type is None:
        # 使用内置的zip函数将所有指定列按行合并，严格模式确保每列长度相同
        table[to] = list(zip(*[table[col] for col in columns], strict=True))

    # 如果指定合并方式为"dict"（字典）
    elif type == "dict":
        # 确保只有两列需要合并
        if len(columns) != 2:
            # 如果不是两列，抛出错误
            msg = f"预期正好两列用于字典，但得到 {columns}"
            raise ValueError(msg)
        # 分别存储键列和值列
        key_col, value_col = columns

        # 创建一个空的结果列表
        results = []

        # 遍历每一行数据
        for _, row in table.iterrows():
            # 提取键和值
            keys = row[key_col]
            values = row[value_col]

            # 创建一个字典，将键值对添加进去
            output = {}
            if len(keys) != len(values):
                # 如果键和值的数量不同，抛出错误
                msg = f"预期相同的键和值数量，但得到 {len(keys)} 个键和 {len(values)} 个值"
                raise ValueError(msg)
            for idx, key in enumerate(keys):
                # 将每个键对应的值添加到字典中
                output[key] = values[idx]

            # 将处理后的字典添加到结果列表中
            results.append(output)

        # 将处理后的字典列表添加为新的列
        table[to] = results

    # 返回一个新的DataFrame，移除原来的索引
    return TableContainer(table=table.reset_index(drop=True))

