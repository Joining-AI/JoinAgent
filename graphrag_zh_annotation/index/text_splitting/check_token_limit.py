# 导入一个叫做TokenTextSplitter的工具，它能帮助我们分割文本
from .text_splitting import TokenTextSplitter

# 这是版权信息，说明代码由微软公司2024年创建，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个关于令牌（token）限制的方法
"""Token limit method definition."""

# 再次导入TokenTextSplitter，确保我们可以使用这个工具
from .text_splitting import TokenTextSplitter

# 定义一个函数，叫做check_token_limit，它有两个参数：一段文本和最大令牌数
def check_token_limit(text, max_token):
    # 创建一个TokenTextSplitter对象，设定每个片段的最大大小为max_token，片段之间没有重叠
    text_splitter = TokenTextSplitter(chunk_size=max_token, chunk_overlap=0)
    # 使用这个工具把文本分割成多个部分，存到一个列表docs里
    docs = text_splitter.split_text(text)
    # 如果分割后的列表有超过1个元素，说明文本超过了最大令牌数
    if len(docs) > 1:
        # 返回0，表示文本超限了
        return 0
    # 如果列表只有1个元素，说明文本没超限，返回1
    return 1

