# 导入uuid模块，这个模块用来生成唯一的标识符
import uuid

# 导入Random类和getrandbits函数，它们来自random模块，用于生成随机数
from random import Random, getrandbits

# 这是代码的版权信息，表示2024年微软公司版权所有
# 并且这个代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个代码文件是关于UUID（唯一标识符）的一些工具函数
"""UUID工具函数库。"""

# 定义一个函数gen_uuid，它接受一个可选的Random对象作为参数rd，默认值为None
def gen_uuid(rd: Random | None = None):
    # 如果rd不是None，就用它来生成128位的随机整数
    # 如果rd是None，就直接用getrandbits函数生成128位随机整数
    int_value = rd.getrandbits(128) if rd is not None else getrandbits(128)
    
    # 使用生成的随机整数创建一个UUID版本4的对象
    # UUID版本4是基于随机数的
    random_uuid = uuid.UUID(int=int_value, version=4)
    
    # 返回这个UUID对象的16进制字符串形式
    return random_uuid.hex

