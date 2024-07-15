# 导入一些必要的工具库
from collections.abc import Iterable  # 用于检查是否可以迭代（比如列表、元组）
from hashlib import md5  # 用来计算MD5哈希值的函数
from typing import Any  # 表示可以是任何类型的变量

# 这段代码的版权信息，由微软公司所有
# 并遵循MIT许可证

# 这里是一些关于哈希处理的辅助函数
"""哈希工具模块。"""

# 定义一个函数gen_md5_hash，它接受两个参数
def gen_md5_hash(item: dict[str, Any], hashcode: Iterable[str]):
    # item是一个键为字符串，值可以是任何类型的字典
    # hashcode是一个包含要用于哈希的列名的字符串列表或元组

    # 遍历hashcode中的每一列
    hashed = "".join([str(item[column]) for column in hashcode])
    # 把字典中对应列的值转换为字符串，然后连接起来
    # 注意：这里我们只使用了str类型的数据，确保所有内容都可以加入到哈希计算中

    # 计算连接后的字符串的MD5哈希值
    # 使用utf-8编码，设置usedforsecurity=False是为了安全提示
    hashed_value = md5(hashed.encode('utf-8'), usedforsecurity=False).hexdigest()
    
    # 返回哈希值，以16进制的形式显示
    return f"{hashed_value}"

