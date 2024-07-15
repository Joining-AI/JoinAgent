# 导入logging模块，它用于记录程序运行时的信息
import logging

# 导入Enum类，这是一个特殊的类，用来创建枚举类型
from enum import Enum

# 导入typing模块中的Any和cast，它们在编程中用于类型检查和转换
from typing import Any, cast

# 导入pandas库，它是处理数据表格的工具
import pandas as pd

# 导入datashaper库的一些组件，如TableContainer、VerbInput、VerbResult和verb装饰器
from datashaper import TableContainer, VerbInput, VerbResult, verb

# 从datashaper引擎的verbs.merge模块导入merge函数，重命名为ds_merge
from datashaper.engine.verbs.merge import merge as ds_merge

# 这两行是版权信息，表示代码由微软公司创作，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为MergeStrategyType的枚举类，它有两个成员：json和datashaper
class MergeStrategyType(str, Enum):
    # 枚举成员json，对应的值是"json"
    json = "json"
    # 枚举成员datashaper，对应的值是"datashaper"
    datashaper = "datashaper"

    # 当打印或显示枚举成员时，返回带引号的字符串形式
    def __repr__(self):
        return f'"{self.value}"'

# 这是一个待完成的函数，它被verb装饰器标记，名字叫"merge_override"
# 注意：这个函数的实现可能不完整，因为它有“TODO”注释，表示需要进一步改进
@verb(name="merge_override")

# 定义一个名为`merge`的函数，它接受一些参数
def merge(
    input: VerbInput,  # 输入的数据，类型是VerbInput
    to: str,  # 要合并到的新列名
    columns: list[str],  # 要合并的列名列表
    strategy: MergeStrategyType = MergeStrategyType.datashaper,  # 合并策略，默认是datashaper
    delimiter: str = "",  # 分隔符，默认为空字符串
    preserveSource: bool = False,  # 是否保留源列，默认为False
    unhot: bool = False,  # 是否取消独热编码，默认为False
    prefix: str = "",  # 前缀，默认为空字符串
    **_kwargs: dict,  # 其他可能的键值对参数，这里不做处理
) -> TableContainer | VerbResult:
    """这个函数是用来合并数据的方法"""
    
    # 定义一个输出变量output，类型是DataFrame
    output: pd.DataFrame
    
    # 根据给定的策略(strategy)进行不同的操作
    # 如果策略是MergeStrategyType.json
    match strategy:
        case MergeStrategyType.json:
            # 使用内部函数 `_merge_json` 进行合并，并将结果赋值给output
            output = _merge_json(input, to, columns)
            
            # 创建一个空列表，用于存放不匹配的列名
            filtered_list: list[str] = []
            
            # 遍历output的所有列名
            for col in output.columns:
                # 尝试在columns列表中找到当前列名
                try:
                    columns.index(col)
                # 如果找不到，捕获ValueError异常
                except ValueError:
                    # 打印错误日志，说明该列不在输入的列名中
                    log.exception("Column %s not found in input columns", col)
                    # 把找不到的列名添加到filtered_list
                    filtered_list.append(col)
                    
            # 如果不保留源列，从output中移除不匹配的列
            if not preserveSource:
                output = cast(Any, output[filtered_list])
                
            # 返回一个新的TableContainer对象，包含合并后的数据并重置索引
            return TableContainer(table=output.reset_index())
        
        # 如果策略不是MergeStrategyType.json，调用其他方法ds_merge处理
        case _:
            return ds_merge(
                input, to, columns, strategy, delimiter, preserveSource, unhot, prefix
            )

# 定义一个私有辅助函数`_merge_json`，它接受同样的参数
def _merge_json(
    input: VerbInput,
    to: str,
    columns: list[str],
) -> pd.DataFrame:
    # 获取输入数据input的数据框形式
    input_table = cast(pd.DataFrame, input.get_input())
    # 初始化输出数据框output，设置为input_table的副本
    output = input_table
    
    # 在output的每一行中，创建一个字典，包含columns列的所有值，然后添加到新列'to'中
    output[to] = output[columns].apply(
        lambda row: ({**row}),
        axis=1,
    )
    
    # 返回处理后的output数据框
    return output

