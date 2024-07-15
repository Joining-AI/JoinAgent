# 导入一些必要的工具库
from collections.abc import Iterable  # 用于检查是否可以迭代的工具
from typing import Any  # 用于表示任何类型的变量
import tiktoken  # 一个处理文本编码的库
from datashaper import ProgressTicker  # 用于追踪进度的工具
import graphrag.config.defaults as defs  # 从graphrag获取默认配置
from graphrag.index.text_splitting import Tokenizer  # 用于分割文本的类
from graphrag.index.verbs.text.chunk.typing import TextChunk  # 定义文本块的数据类型

# 这段代码是微软公司写的，遵循MIT许可证
# """这是一个包含run和split_text_on_tokens方法定义的模块。"""

# 从collections.abc导入Iterable，用于检查是否可以迭代
# 从typing导入Any，用于表示任何类型的变量

# 导入tiktoken库，用于文本编码
# 导入ProgressTicker，用于显示进度条

# 导入graphrag的默认配置
# 导入Tokenizer类，用于文本分割
# 导入TextChunk，这是处理文本块的数据类型

# 定义一个名为run的函数，它接收三个参数：输入文本列表、参数字典和进度条
def run(
    input: list[str],  # 输入的字符串列表
    args: dict[str, Any],  # 包含各种设置的字典
    tick: ProgressTicker,  # 用于更新进度的工具
) -> Iterable[TextChunk]:  # 返回一个可迭代的文本块列表

    # 从参数字典中获取每个文本块的令牌数，默认值来自defs.CHUNK_SIZE
    tokens_per_chunk = args.get("chunk_size", defs.CHUNK_SIZE)
    # 获取文本块之间的重叠量，默认值来自defs.CHUNK_OVERLAP
    chunk_overlap = args.get("chunk_overlap", defs.CHUNK_OVERLAP)
    # 获取编码名称，默认值来自defs.ENCODING_MODEL
    encoding_name = args.get("encoding_name", defs.ENCODING_MODEL)
    # 使用tiktoken获取指定编码的编码器
    enc = tiktoken.get_encoding(encoding_name)

    # 定义一个函数，将文本转为整数列表
    def encode(text: str) -> list[int]:
        # 确保输入是字符串，如果不是，将其转换为字符串
        if not isinstance(text, str):
            text = f"{text}"
        # 使用编码器将文本编码为整数列表
        return enc.encode(text)

    # 定义一个函数，将整数列表转回文本
    def decode(tokens: list[int]) -> str:
        # 使用编码器将整数列表解码回文本
        return enc.decode(tokens)

    # 调用split_text_on_tokens函数，传入输入文本、Tokenizer实例和进度条
    # 返回一个分割后的文本块列表
    return split_text_on_tokens(
        input,
        Tokenizer(
            chunk_overlap=chunk_overlap,  # 文本块重叠量
            tokens_per_chunk=tokens_per_chunk,  # 每个块的令牌数
            encode=encode,  # 用于编码的函数
            decode=decode,  # 用于解码的函数
        ),
        tick,
    )

# 注释表明这段代码是从langchain项目改编的，以更好地控制文本分块过程

# 定义一个函数split_text_on_tokens，它接受三个参数：texts（一个包含字符串的列表），enc（一个分词器对象）和tick（一个进度指示器）
def split_text_on_tokens(
    texts: list[str], enc: Tokenizer, tick: ProgressTicker
) -> list[TextChunk]:
    """这个函数用来分割输入的文本并返回一个个文本块（chunks）"""
    # 初始化结果列表和一个用于存储映射ID的空列表
    result = []
    mapped_ids = []

    # 遍历文本列表
    for source_doc_idx, text in enumerate(texts):
        # 使用分词器编码文本
        encoded = enc.encode(text)
        # 更新进度指示器的进度
        tick(1)
        # 将文档索引和编码后的ID添加到映射ID列表中
        mapped_ids.append((source_doc_idx, encoded))

    # 创建一个新的列表，其中每个元素都是一个元组，包含文档索引和单个ID
    input_ids: list[tuple[int, int]] = [
        (source_doc_idx, id) for source_doc_idx, ids in mapped_ids for id in ids
    ]

    # 初始化开始索引和当前索引
    start_idx = 0
    cur_idx = min(start_idx + enc.tokens_per_chunk, len(input_ids))

    # 获取当前范围内的ID
    chunk_ids = input_ids[start_idx:cur_idx]

    # 当开始索引小于输入ID的长度时，循环继续
    while start_idx < len(input_ids):
        # 使用分词器解码当前范围内的ID，得到文本块
        chunk_text = enc.decode([id for _, id in chunk_ids])
        # 获取该文本块来自的原始文档索引
        doc_indices = list({doc_idx for doc_idx, _ in chunk_ids})
        # 创建一个TextChunk对象并添加到结果列表中
        result.append(
            TextChunk(
                text_chunk=chunk_text,
                source_doc_indices=doc_indices,
                n_tokens=len(chunk_ids),
            )
        )
        # 更新开始索引，为下一次循环准备
        start_idx += enc.tokens_per_chunk - enc.chunk_overlap
        # 计算下一个范围的结束索引
        cur_idx = min(start_idx + enc.tokens_per_chunk, len(input_ids))
        # 获取下一个范围内的ID
        chunk_ids = input_ids[start_idx:cur_idx]

    # 返回结果列表
    return result

