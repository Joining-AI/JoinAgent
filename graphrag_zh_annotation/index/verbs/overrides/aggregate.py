# 导入必要的库，让程序可以处理数据和类型
from dataclasses import dataclass
from typing import Any, cast
import pandas as pd
from datashaper import (
    FieldAggregateOperation,
    Progress,
    TableContainer,
    VerbCallbacks,
    VerbInput,
    aggregate_operation_mapping,
    verb,
)

# 这是微软公司的版权信息，表明代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含一个叫做'Aggregation'的模型
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 列出了一些数组聚合操作的类型
ARRAY_AGGREGATIONS = [
    FieldAggregateOperation.ArrayAgg,
    FieldAggregateOperation.ArrayAggDistinct,
]

# 定义了一个名为"aggregate_override"的函数，它会执行数据聚合
# 注意：这个函数可能有点复杂，而且与原始的aggregate函数有些不同
@verb(name="aggregate_override")
def aggregate(
    # 输入的数据
    input: VerbInput,
    # 回调函数，用于更新进度
    callbacks: VerbCallbacks,
    # 聚合操作的列表，每个操作都是一个字典
    aggregations: list[dict[str, Any]],
    # 分组的列名，可选
    groupby: list[str] | None = None,
    # 其他未使用的参数
    **_kwargs: dict,
) -> TableContainer:
    """这个函数用来做数据聚合操作"""
    
    # 加载并准备要应用的聚合操作
    aggregations_to_apply = _load_aggregations(aggregations)
    
    # 将聚合操作转换成Pandas能理解的形式
    df_aggregations = {
        agg.column: _get_pandas_agg_operation(agg)
        for agg in aggregations_to_apply.values()
    }
    
    # 获取输入数据
    input_table = input.get_input()
    
    # 更新进度条为0%
    callbacks.progress(Progress(percent=0))

    # 如果没有分组列，则对所有数据进行分组
    if groupby is None:
        output_grouped = input_table.groupby(lambda _x: True)
    # 如果有分组列，按这些列进行分组
    else:
        output_grouped = input_table.groupby(groupby, sort=False)
    
    # 对每个分组应用聚合操作
    output = cast(pd.DataFrame, output_grouped.agg(df_aggregations))
    
    # 重命名列名，根据聚合操作的'to'属性
    output.rename(
        columns={agg.column: agg.to for agg in aggregations_to_apply.values()},
        inplace=True,
    )
    
    # 用'to'属性的值作为新的列名
    output.columns = [agg.to for agg in aggregations_to_apply.values()]
    
    # 更新进度条为100%
    callbacks.progress(Progress(percent=1))

    # 返回处理后的数据，重置索引
    return TableContainer(table=output.reset_index())

# 使用'dataclass'定义一个类，用于存储数据
@dataclass

# 定义一个名为Aggregation的类
class Aggregation:
    """这是Aggregation类的说明，用来描述这个类的功能"""
    
    # 类中的变量，column表示列名，可能是字符串或没有（None）
    column: str | None
    # operation表示操作类型，也是字符串
    operation: str
    # to表示结果要保存到的列名
    to: str

    # 这个变量只在"concat"操作时有用，用于连接字符串的分隔符，默认是逗号（如果没有设置）
    separator: str | None = None


# 这是一个函数，获取pandas的聚合操作方法
def _get_pandas_agg_operation(agg: Aggregation) -> Any:
    # 待办事项：把这个功能合并到datashaper里
    # 如果操作是"string_concat"（字符串连接）
    if agg.operation == "string_concat":
        # 使用分隔符（如果没有就用逗号）来连接字符串
        return (agg.separator or ",").join
    # 否则，从一个映射表中找到对应的操作方法
    return aggregate_operation_mapping[FieldAggregateOperation(agg.operation)]


# 这也是一个函数，加载聚合操作列表并转换成Aggregation对象的字典
def _load_aggregations(
    aggregations: list[dict[str, Any]],
) -> dict[str, Aggregation]:
    # 遍历aggregations列表中的每一个聚合操作
    return {
        # 每个操作的"column"值作为字典的键
        aggregation["column"]: Aggregation(
            # 创建一个新的Aggregation对象，传入列名、操作和目标列名
            aggregation["column"], aggregation["operation"], aggregation["to"]
        )
        # 对列表中的每一个聚合操作执行上述操作
        for aggregation in aggregations
    }

