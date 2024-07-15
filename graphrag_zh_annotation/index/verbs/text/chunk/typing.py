# 导入一个叫做 'dataclass' 的工具，它帮助我们创建带有默认值和自动初始化的类
from dataclasses import dataclass

# 这是一个版权声明，说明这段代码由微软公司编写，2024年版权有效
# 并且代码遵循MIT许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件包含一个名为'TextChunk'的模块，里面有一个数据模型

# 再次导入 'dataclass'，因为我们需要在下面定义类时使用它
from dataclasses import dataclass


# 使用 'dataclass' 定义一个类，叫做 'TextChunk'
@dataclass
class TextChunk:
    # 这个类是用来存储文本块信息的
    # 'text_chunk' 是一个字符串，保存文本内容
    text_chunk: str
    # 'source_doc_indices' 是一个整数列表，记录文本在原文档中的位置索引
    source_doc_indices: list[int]
    # 'n_tokens' 是一个可选的整数，表示文本中的单词数量，可能为None
    n_tokens: int | None = None


# 定义一个类型别名 'ChunkInput'
# 这可以是：
# - 一个字符串
# - 一个字符串列表
# - 一个包含(id, text)元组的列表
ChunkInput = str | list[str] | list[tuple[str, str]]
# 这是分块策略的输入，可以是单个字符串，多个字符串，或者带有标识符和文本的元组列表

