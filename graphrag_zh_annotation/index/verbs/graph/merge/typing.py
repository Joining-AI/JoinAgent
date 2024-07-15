# 导入数据类模块，用于创建有默认值的类
from dataclasses import dataclass
# 导入枚举模块，用于定义有限的、命名的常量集合
from enum import Enum

# 这是代码的作者和许可信息
# Copyright (c) 2024 Microsoft Corporation.  # 代码版权属于微软公司
# Licensed under the MIT License  # 使用MIT许可证授权

# 这个模块包含几个处理合并操作的类
"""一个模块，里面有一些用于处理合并操作的模型。"""

# 定义一个基本的合并操作类，它继承自字符串和枚举
class BasicMergeOperation(str, Enum):
    """基本的合并操作类。"""
    # 这里是两种可能的操作
    Replace = "替换"  # 如果有新的值，就用新值替换旧值
    Skip = "跳过"     # 如果有新的值，就忽略不合并


# 定义一个字符串操作类，也继承自字符串和枚举
class StringOperation(str, Enum):
    """字符串操作类。"""
    Concat = "连接"   # 把两个字符串连在一起
    Replace = "替换"  # 用新值替换旧值
    Skip = "跳过"     # 忽略不合并


# 定义一个数值操作类，同样继承自字符串和枚举
class NumericOperation(str, Enum):
    """数值操作类。"""
    Sum = "求和"       # 计算两个数的和
    Average = "平均"   # 计算两个数的平均值
    Max = "最大值"     # 取两个数中的较大值
    Min = "最小值"     # 取两个数中的较小值
    Multiply = "乘以"  # 两个数相乘
    Replace = "替换"   # 用新值替换旧值
    Skip = "跳过"      # 忽略不合并


# 使用数据类定义一个详细的属性合并操作类
@dataclass
class DetailedAttributeMergeOperation:
    """详细属性合并操作类。"""
    # 操作类型，可以是字符串操作或数值操作
    operation: str

    # 如果是连接字符串，可以指定分隔符
    separator: str | None = None
    # 如果是处理列表或数组，可以指定分隔符
    delimiter: str | None = None
    # 是否只保留唯一的元素（去除重复）
    distinct: bool = False


# 这是一个类型别名，代表属性合并操作可以是简单的字符串或详细的数据类
AttributeMergeOperation = str | DetailedAttributeMergeOperation

