# 导入必要的工具模块，让程序能处理数据和迭代器
from collections.abc import Iterator   # 引入Iterator接口，用于处理迭代器
from itertools import islice          # 引入islice函数，用于切片迭代器

# 引入tiktoken库，用于编码和解码文本
import tiktoken

# 以下代码是微软公司的一个文本处理工具包
# 使用MIT许可证授权

# 定义一个函数，计算文本中的令牌（单词或字符）数量
def num_tokens(text: str, token_encoder: tiktoken.Encoding | None = None) -> int:
    # 如果没有提供编码器，就用"cl100k_base"这个默认的
    if token_encoder is None:
        token_encoder = tiktoken.get_encoding("cl100k_base")
    # 用编码器编码文本，然后返回编码后的令牌数量
    return len(token_encoder.encode(text))  # 忽略类型检查警告

# 定义一个函数，将数据分批成大小为n的元组
# 最后一批可能小于n个元素
def batched(iterable: Iterator, n: int):
    # 检查n是否大于等于1，如果不是，则抛出错误
    if n < 1:
        raise ValueError("n必须至少为1")
    # 创建一个迭代器对象
    it = iter(iterable)
    # 使用islice函数切片迭代器，生成大小为n的批次，直到没有元素为止
    while batch := tuple(islice(it, n)):
        # 生成并返回批次元组
        yield batch

# 定义一个函数，根据令牌长度将文本分割成多个片段
def chunk_text(
    text: str, max_tokens: int, token_encoder: tiktoken.Encoding | None = None
):
    # 如果没有提供编码器，就用"cl100k_base"这个默认的
    if token_encoder is None:
        token_encoder = tiktoken.get_encoding("cl100k_base")
    # 用编码器编码文本
    tokens = token_encoder.encode(text)  # 忽略类型检查警告
    # 将令牌分批，每批最大max_tokens个
    chunk_iterator = batched(iter(tokens), max_tokens)
    # 生成并返回令牌批次
    yield from chunk_iterator

