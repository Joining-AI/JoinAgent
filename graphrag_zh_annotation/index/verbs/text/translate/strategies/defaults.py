# 这行代码是版权信息，表示这个代码归2024年的微软公司所有。
# Copyright (c) 2024 Microsoft Corporation.

# 这是一个许可证声明，代码基于MIT许可证授权，允许他人在一定条件下使用这段代码。
# Licensed under the MIT License

# 这是一个文档字符串，用来解释这个文件的作用。
# 它告诉人们这个文件包含了TRANSLATION_PROMPT变量的定义。
"""这是一个包含TRANSLATION_PROMPT值定义的文件。"""

# 定义了一个变量名为TRANSLATION_PROMPT，它是一个很长的字符串。
TRANSLATION_PROMPT = """
    你是一个乐于助人的助手。请将以下文字翻译成{language}，确保所有文字都是用{language}书写的。
    """.strip()

# 这里的.strip()函数是用来去掉字符串开头和结尾的空白字符（比如空格或换行符）。
# 所以这行代码是为了让输出的文本更整洁，没有多余的空格或换行。

