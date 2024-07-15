# 导入一个名为check_token_limit的函数，它可能用来检查令牌（比如单词）的数量是否超过了限制
from .check_token_limit import check_token_limit

# 导入一系列与文本分割相关的类和函数
from .text_splitting import (
    # DecodeFn：一个用于将编码后的文本解码回原始形式的函数
    DecodeFn,

    # EncodedText：可能是一个表示已编码文本的数据类型
    EncodedText,

    # EncodeFn：一个用于将原始文本编码的函数
    EncodeFn,

    # LengthFn：可能是一个计算文本长度的函数
    LengthFn,

    # NoopTextSplitter：不做任何处理的文本分割器，就像什么都没做一样
    NoopTextSplitter,

    # TextListSplitter：用于将文本列表分割的类
    TextListSplitter,

    # TextListSplitterType：可能是文本列表分割器类型的枚举或常量
    TextListSplitterType,

    # TextSplitter：一个通用的文本分割器类
    TextSplitter,

    # Tokenizer：将文本分割成单词或令牌的类
    Tokenizer,

    # TokenTextSplitter：基于令牌进行文本分割的类
    TokenTextSplitter,

    # split_text_on_tokens：一个函数，根据令牌来分割文本
    split_text_on_tokens,
)

# 这个版权信息告诉我们这个代码是微软公司2024年的作品，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块导出的所有类和函数，这样其他文件可以通过导入这个包来使用它们
__all__ = [
    "DecodeFn",
    "EncodeFn",
    "EncodedText",
    "LengthFn",
    "NoopTextSplitter",
    "TextListSplitter",
    "TextListSplitterType",
    "TextSplitter",
    "TokenTextSplitter",
    "Tokenizer",
    "check_token_limit",
    "split_text_on_tokens",
]

