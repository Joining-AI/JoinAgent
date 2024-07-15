# 导入logging模块，它用于记录程序运行时的信息
import logging
# 导入tiktoken模块，这个模块可能用于处理特定的编码或令牌
import tiktoken
# 这是一个版权声明，表示代码归微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件包含一些处理令牌的工具函数
"""Utilities for working with tokens."""

# 再次导入logging模块，创建一个名为__name__的日志记录器（这里应该是当前模块的名字）
import logging

# 再次导入tiktoken模块，确保我们有它的功能
import tiktoken

# 定义一个默认的编码名称
DEFAULT_ENCODING_NAME = "cl100k_base"
# 设置日志记录器，这样程序在遇到问题时可以打印警告或错误信息
log = logging.getLogger(__name__)

# 定义一个函数，计算字符串中的令牌数量
def num_tokens_from_string(
    # 输入一个字符串
    string: str,
    # 可选参数，提供模型名称，用于获取特定编码
    model: str | None = None,
    # 可选参数，提供编码名称
    encoding_name: str | None = None
) -> int:
    """返回文本字符串中的令牌数."""
    # 如果提供了模型名称
    if model is not None:
        # 尝试根据模型获取编码
        try:
            encoding = tiktoken.encoding_for_model(model)
        # 如果找不到对应模型的编码，捕获KeyError异常
        except KeyError:
            # 打印警告信息，使用默认编码代替
            msg = f"未能为{model}获取编码，用于num_tokens_from_string。将回退到默认编码{DEFAULT_ENCODING_NAME}"
            log.warning(msg)
            # 使用默认编码
            encoding = tiktoken.get_encoding(DEFAULT_ENCODING_NAME)
    # 如果没有提供模型，但提供了编码名称
    else:
        # 直接使用提供的编码名称或默认编码
        encoding = tiktoken.get_encoding(encoding_name or DEFAULT_ENCODING_NAME)
    # 返回编码后的字符串长度，即令牌数
    return len(encoding.encode(string))

# 定义一个函数，从令牌列表中恢复成文本字符串
def string_from_tokens(
    # 输入一个整数列表，代表令牌
    tokens: list[int],
    # 可选参数，提供模型名称
    model: str | None = None,
    # 可选参数，提供编码名称
    encoding_name: str | None = None
) -> str:
    """从令牌列表返回文本字符串."""
    # 如果提供了模型名称
    if model is not None:
        # 根据模型获取编码
        encoding = tiktoken.encoding_for_model(model)
    # 如果只提供了编码名称
    elif encoding_name is not None:
        # 直接使用提供的编码名称
        encoding = tiktoken.get_encoding(encoding_name)
    # 如果两个参数都没有提供，抛出一个错误
    else:
        # 提示必须指定模型或编码名称
        msg = "Either model or encoding_name must be specified."
        raise ValueError(msg)
    # 使用编码将令牌列表解码为字符串
    return encoding.decode(tokens)

