# 导入必要的模块，让程序能处理数据
from collections.abc import Callable  # 从Python标准库导入Callable接口，检查是否为可调用对象
from typing import Any, cast  # 从Python类型提示库导入Any（任何类型）和cast（类型转换）
import pandas as pd  # 导入Pandas库，用于数据处理
from pandas._typing import MergeHow  # 导入Pandas内部的MergeHow类型，用于指定合并方式

# 版权信息
# 注释：这个模块包含一些用于操作DataFrame的工具函数

# 定义一个函数，删除DataFrame中的列
def drop_columns(df: pd.DataFrame, *column: str) -> pd.DataFrame:
    """删除DataFrame中指定的列"""
    # 使用drop方法删除列，参数axis=1表示按列删除
    return df.drop(list(column), axis=1)

# 定义一个函数，返回一个只包含指定列等于特定值的DataFrame
def where_column_equals(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    """返回一个筛选后的DataFrame，其中指定列的值等于给定值"""
    # 使用条件筛选出满足条件的行
    return cast(pd.DataFrame, df[df[column] == value])

# 定义一个函数，执行反连接操作（排除指定数据）
def antijoin(df: pd.DataFrame, exclude: pd.DataFrame, column: str) -> pd.DataFrame:
    """返回一个反连接后的DataFrame，即排除指定DataFrame中的行"""
    # 使用merge方法进行外连接，并添加一个指示符列 "_merge"
    result = df.merge(exclude[[column]], on=column, how="outer", indicator=True)
    # 如果结果中有"_merge"列，筛选出left_only的行并删除"_merge"列
    if "_merge" in result.columns:
        result = result[result["_merge"] == "left_only"].drop("_merge", axis=1)
    # 返回转换后的DataFrame
    return cast(pd.DataFrame, result)

# 定义一个函数，对Series应用一个转换函数
def transform_series(series: pd.Series, fn: Callable[[Any], Any]) -> pd.Series:
    """将一个函数应用到Series的每个元素上"""
    # 使用apply方法应用函数，并返回新的Series
    return cast(pd.Series, series.apply(fn))

# 定义一个函数，执行两个DataFrame的连接操作
def join(left: pd.DataFrame, right: pd.DataFrame, key: str, strategy: MergeHow = "left") -> pd.DataFrame:
    """执行两个DataFrame之间的连接操作"""
    # 使用merge方法连接DataFrame，指定连接键和策略（默认为左连接）
    return left.merge(right, on=key, how=strategy)

# 定义一个函数，合并多个DataFrame
def union(*frames: pd.DataFrame) -> pd.DataFrame:
    """合并给定的DataFrame集合"""
    # 使用concat方法将所有DataFrame水平堆叠在一起
    return pd.concat(list(frames))

# 定义一个函数，从DataFrame选择指定的列
def select(df: pd.DataFrame, *columns: str) -> pd.DataFrame:
    """从DataFrame中选择指定的列"""
    # 返回只包含指定列的新DataFrame
    return cast(pd.DataFrame, df[list(columns)])

