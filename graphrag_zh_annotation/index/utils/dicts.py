# 版权声明：这段代码由微软公司于2024年创作。
# 它遵循MIT许可证授权。

"""
这是一个工具模块，里面有一些检查和验证字典类型的方法。
"""

# 定义一个名为dict_has_keys_with_types的函数，它接受两个参数：
# 1. 一个叫data的字典
# 2. 一个包含键值对（字符串和类型）的列表，叫做expected_fields

def dict_has_keys_with_types(
    data: dict,  # 接收一个字典
    expected_fields: list[tuple[str, type]]  # 接收一个列表，列表里的元素是字符串和类型的元组
) -> bool:  # 函数返回一个布尔值（True或False）

    # 遍历expected_fields列表中的每个键值对（field, field_type）
    for field, field_type in expected_fields:

        # 如果字典data中没有当前的field（键），返回False
        if field not in data:
            return False

        # 获取字典data中field对应的值，存储在变量value里
        value = data[field]

        # 检查value是否是field_type（类型）的实例，如果不是，返回False
        if not isinstance(value, field_type):
            return False

    # 如果所有键值对都匹配，最后返回True
    return True

