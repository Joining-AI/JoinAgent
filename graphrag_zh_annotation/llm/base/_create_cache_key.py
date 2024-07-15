# 导入一个叫做 hashlib 的模块，它能帮助我们计算字符串的哈希值
import hashlib

# 这段代码的版权属于微软公司，并遵循 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一些关于缓存键生成工具的说明
"""Cache key generation utils."""

# 定义一个函数，输入是一个字典，返回一个排序后的字符串
def _llm_string(params: dict) -> str:
    # 如果字典里有 "max_tokens" 但没有 "n"，我们给 "n" 赋值为 None
    # 这样做是为了确保同样的提示不会生成不同的缓存键
    if "max_tokens" in params and "n" not in params:
        params["n"] = None
    # 将字典里的键值对按顺序转换成字符串并返回
    return str(sorted((k, v) for k, v in params.items()))

# 定义另一个函数，输入是一个字符串，返回其哈希值（一种特殊的字符串）
def _hash(_input: str) -> str:
    """用确定性的哈希方法来计算字符串的唯一标识符"""
    # 使用 hashlib.md5() 计算字符串的哈希值，并将其转换成 16 进制字符串
    return hashlib.md5(_input.encode()).hexdigest()  # 注意：这行代码是为了避免安全警告

# 最后，定义一个主要的函数，输入是操作名、提示文本和设置字典，返回一个缓存键
def create_hash_key(operation: str, prompt: str, parameters: dict) -> str:
    # 先调用上面的函数，根据设置字典生成字符串
    llm_string = _llm_string(parameters)
    # 将操作名、提示文本和设置字符串拼接起来，然后计算哈希值
    # 最后，以特定格式返回这个哈希值作为缓存键
    return f"{operation}-{_hash(prompt + llm_string)}"

