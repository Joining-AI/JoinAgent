# 导入两个有用的库，numpy 和 pandas，它们帮助处理数字和表格数据
import numpy as np
import pandas as pd

# 这是微软公司的版权声明
# 版权所有 (c) 2024 微软公司。
# 根据 MIT 许可证授权

# 这个文件是用来加载和处理数据的一些工具函数

# 定义一个函数，把数据系列（Series）中的一个值转换成字符串
def to_str(data: pd.Series, column_name: str | None) -> str:
    # 如果列名是空的，就抛出一个错误
    if column_name is None:
        msg = "列名是空的"
        raise ValueError(msg)  # 抛出一个值错误

    # 如果列名在数据中，就把它转换成字符串并返回
    if column_name in data:
        return str(data[column_name])
    # 如果列名不在数据中，就抛出一个错误
    msg = f"找不到列 {column_name}"
    raise ValueError(msg)

# 定义一个函数，把数据系列中的一个值转换成可选的字符串
def to_optional_str(data: pd.Series, column_name: str | None) -> str | None:
    # 如果列名是空的，就抛出一个错误
    if column_name is None:
        msg = "列名是空的"
        raise ValueError(msg)

    # 如果列名在数据中，检查它的值，如果值是 None，则返回 None；否则转换成字符串并返回
    if column_name in data:
        value = data[column_name]
        if value is None:
            return None
        return str(data[column_name])
    # 如果列名不在数据中，就抛出一个错误
    msg = f"找不到列 {column_name}"
    raise ValueError(msg)

# 定义一个函数，把数据系列中的一个值转换成列表
def to_list(
    data: pd.Series, column_name: str | None, item_type: type | None = None
) -> list:
    # 如果列名是空的，就抛出一个错误
    if column_name is None:
        msg = "列名是空的"
        raise ValueError(msg)

    # 如果列名在数据中，获取该列的值
    if column_name in data:
        value = data[column_name]
        # 如果值是 numpy 数组，先转换成普通列表
        if isinstance(value, np.ndarray):
            value = value.tolist()

        # 检查值是否为列表，如果不是，抛出一个错误
        if not isinstance(value, list):
            msg = f"值不是列表：{value} ({type(value)})"
            raise ValueError(msg)

        # 如果指定了元素类型，检查列表中的每个元素是否符合这个类型
        if item_type is not None:
            for v in value:
                if not isinstance(v, item_type):
                    msg = f"列表中有不符合 {item_type} 类型的元素：{v} ({type(v)})"
                    raise TypeError(msg)
        # 如果一切正常，返回这个列表
        return value

    # 如果列名不在数据中，就抛出一个错误
    msg = f"找不到列 {column_name}"
    raise ValueError(msg)

# 定义一个函数，将数据转换并验证为可选列表
def to_optional_list(
    data: pd.Series,  # 接收一个pandas的Series类型数据
    column_name: str | None,  # 接收一个可能为None的字符串，表示列名
    item_type: type | None = None  # 接收一个可能为None的类型，用于检查列表元素类型，默认为None
) -> list | None:  # 函数返回值可能是列表或None

    """这个函数会把一个值转换成一个可选的列表，如果列名不存在或者值不是列表，就返回None"""
    
    # 如果列名是None，直接返回None
    if column_name is None:
        return None

    # 如果列名在数据中
    if column_name in data:
        # 获取该列的值
        value = data[column_name]  # 忽略类型检查，因为实际可能有其他类型
        # 如果值是None，也返回None
        if value is None:
            return None

        # 如果值是numpy数组，转换成列表
        if isinstance(value, np.ndarray):
            value = value.tolist()

        # 检查值是否为列表，如果不是，抛出错误
        if not isinstance(value, list):
            msg = f"这个值不是一个列表：{value} （{type(value)}）"
            raise ValueError(msg)

        # 如果指定了item_type，检查列表中的每个元素类型
        if item_type is not None:
            for v in value:
                # 如果元素类型不符合要求，抛出错误
                if not isinstance(v, item_type):
                    msg = f"列表里有一个元素不是{item_type}：{v} （{type(v)}）"
                    raise TypeError(msg)

        # 如果所有检查都通过，返回列表
        return value

    # 列名不在数据中，返回None
    return None

# 定义另一个函数，将数据转换并验证为整数
def to_int(data: pd.Series, column_name: str | None) -> int:
    """这个函数会把一个值转换成一个整数"""
    
    # 如果列名是None，抛出错误
    if column_name is None:
        msg = "列名是None"
        raise ValueError(msg)

    # 如果列名在数据中
    if column_name in data:
        # 获取该列的值
        value = data[column_name]
        # 如果值是浮点数，转换成整数
        if isinstance(value, float):
            value = int(value)
        # 检查值是否为整数，如果不是，抛出错误
        if not isinstance(value, int):
            msg = f"这个值不是一个整数：{value} （{type(value)}）"
            raise ValueError(msg)
    else:
        # 列名不在数据中，抛出错误
        msg = f"数据中找不到列：{column_name}"
        raise ValueError(msg)

    # 返回整数值
    return int(value)

# 定义一个函数，将数据转换并验证为可选的整数
def to_optional_int(data: pd.Series, column_name: str | None) -> int | None:
    # 如果列名是None，返回None
    if column_name is None:
        return None

    # 如果列名在数据中
    if column_name in data:
        # 获取该列的数据
        value = data[column_name]

        # 如果值是None，返回None
        if value is None:
            return None

        # 如果值是浮点数，转换为整数
        if isinstance(value, float):
            value = int(value)
        
        # 如果值不是整数，抛出错误
        if not isinstance(value, int):
            # 创建错误消息
            msg = f"value is not an int: {value} ({type(value)})"
            # 抛出错误
            raise ValueError(msg)
    else:
        # 如果列不在数据中，创建错误消息
        msg = f"Column {column_name} not found in data"
        # 抛出错误
        raise ValueError(msg)

    # 返回转换后的整数
    return int(value)

# 定义一个函数，将数据转换并验证为浮点数
def to_float(data: pd.Series, column_name: str | None) -> float:
    # 如果列名是None，抛出错误
    if column_name is None:
        msg = "Column name is None"
        # 抛出错误
        raise ValueError(msg)

    # 如果列名在数据中
    if column_name in data:
        # 获取该列的数据
        value = data[column_name]
        
        # 如果值不是浮点数，抛出错误
        if not isinstance(value, float):
            # 创建错误消息
            msg = f"value is not a float: {value} ({type(value)})"
            # 抛出错误
            raise ValueError(msg)
    else:
        # 如果列不在数据中，创建错误消息
        msg = f"Column {column_name} not found in data"
        # 抛出错误
        raise ValueError(msg)

    # 返回转换后的浮点数
    return float(value)

# 定义一个函数，将数据转换并验证为可选的浮点数
def to_optional_float(data: pd.Series, column_name: str | None) -> float | None:
    # 如果列名是None，返回None
    if column_name is None:
        return None

    # 如果列名在数据中
    if column_name in data:
        # 获取该列的数据
        value = data[column_name]

        # 如果值是None，返回None
        if value is None:
            return None
        
        # 如果值不是浮点数，抛出错误
        if not isinstance(value, float):
            # 创建错误消息
            msg = f"value is not a float: {value} ({type(value)})"
            # 抛出错误
            raise ValueError(msg)
    else:
        # 如果列不在数据中，创建错误消息
        msg = f"Column {column_name} not found in data"
        # 抛出错误
        raise ValueError(msg)

    # 返回转换后的浮点数
    return float(value)

# 定义一个名为to_dict的函数，它接受四个参数：
# data：一个pandas的Series（类似一列数据）
# column_name：可能有的列名，如果有的话
# key_type：可能指定的字典键的类型
# value_type：可能指定的字典值的类型
def to_dict(
    data: pd.Series,
    column_name: str | None,  # 列名可以是字符串或None
    key_type: type | None = None,  # 键的类型可以是任何类型，默认为None
    value_type: type | None = None,  # 值的类型也可以是任何类型，默认为None
) -> dict:  # 函数返回一个字典

    # 如果列名是None，抛出一个ValueError（错误）并附带信息
    if column_name is None:
        msg = "Column name is None"
        raise ValueError(msg)

    # 如果列名在data中
    if column_name in data:
        # 获取该列的数据
        value = data[column_name]
        
        # 检查数据是否为字典，如果不是，抛出ValueError
        if not isinstance(value, dict):
            msg = f"value is not a dict: {value} ({type(value)})"
            raise ValueError(msg)

        # 如果指定了键的类型，检查字典中的每个键是否符合
        if key_type is not None:
            for v in value:
                if not isinstance(v, key_type):
                    msg = f"dict key has item that is not {key_type}: {v} ({type(v)})"
                    raise TypeError(msg)

        # 如果指定了值的类型，检查字典中的每个值是否符合
        if value_type is not None:
            for v in value.values():
                if not isinstance(v, value_type):
                    msg = (
                        f"dict value has item that is not {value_type}: {v} ({type(v)})"
                    )
                    raise TypeError(msg)

        # 如果所有检查都通过，返回字典
        return value

    # 如果列名不在data中，抛出ValueError并附带信息
    msg = f"Column {column_name} not found in data"
    raise ValueError(msg)

# 定义一个名为to_optional_dict的函数，它接受四个参数
def to_optional_dict(
    # 参数data是一个pandas Series（数据列）
    data: pd.Series,
    # 参数column_name是可能为None的字符串，表示要查找的列名
    column_name: str | None,
    # 参数key_type是可能为None的类型，用于检查字典中的键类型
    key_type: type | None = None,
    # 参数value_type是可能为None的类型，用于检查字典中的值类型
    value_type: type | None = None,
) -> dict | None:
    """这个函数会将一个值转换并验证为可选的字典。"""

    # 如果column_name是None，直接返回None
    if column_name is None:
        return None

    # 检查column_name是否在data中
    if column_name in data:
        # 获取该列的数据
        value = data[column_name]
        
        # 如果值是None，返回None
        if value is None:
            return None

        # 如果值不是字典，抛出错误
        if not isinstance(value, dict):
            # 错误信息：值不是一个字典
            msg = f"value is not a dict: {value} ({type(value)})"
            raise TypeError(msg)

        # 如果指定了key_type，检查字典的每个键是否符合该类型
        if key_type is not None:
            for v in value:
                if not isinstance(v, key_type):
                    # 错误信息：字典的键包含了不符合key_type的项
                    msg = f"dict key has item that is not {key_type}: {v} ({type(v)})"
                    raise TypeError(msg)

        # 如果指定了value_type，检查字典的每个值是否符合该类型
        if value_type is not None:
            for v in value.values():
                if not isinstance(v, value_type):
                    # 错误信息：字典的值包含了不符合value_type的项
                    msg = (
                        f"dict value has item that is not {value_type}: {v} ({type(v)})"
                    )
                    raise TypeError(msg)

        # 如果所有检查都通过，返回这个字典
        return value

    # 如果column_name不在data中，抛出错误
    msg = f"Column {column_name} not found in data"
    raise ValueError(msg)

