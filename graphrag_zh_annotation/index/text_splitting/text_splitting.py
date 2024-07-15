# 导入一个用来处理JSON数据的库
import json

# 导入一个用于日志记录的库
import logging

# 从抽象基类模块导入ABC和abstractmethod，它们用于创建抽象类和方法
from abc import ABC, abstractmethod

# 从Python内置的集合抽象基类模块导入Callable、Collection和Iterable接口
from collections.abc import Callable, Collection, Iterable

# 从dataclasses模块导入dataclass装饰器，用于创建数据类
from dataclasses import dataclass

# 从枚举模块导入Enum类，用于创建枚举类型
from enum import Enum

# 从typing模块导入Any（表示任何类型）、Literal（表示字面量类型）和cast（类型转换函数）
from typing import Any, Literal, cast

# 导入pandas库，用于数据处理
import pandas as pd

# 导入tiktoken库，它可能用于处理特定的文本或令牌操作
import tiktoken

# 从graphrag.index.utils模块导入一个函数，用于计算字符串中的令牌数量
from graphrag.index.utils import num_tokens_from_string

# 提示这段代码的版权信息
# 它遵循MIT许可证发布

# 文档字符串描述了这个模块包含的类
"""这个模块包含 'Tokenizer', 'TextSplitter', 'NoopTextSplitter' 和 'TokenTextSplitter' 类。"""

# 定义一些自定义类型
EncodedText = list[int]  # 一个整数列表，代表编码后的文本
DecodeFn = Callable[[EncodedText], str]  # 接受整数列表并返回原始字符串的函数
EncodeFn = Callable[[str], EncodedText]  # 接受字符串并返回整数列表的函数
LengthFn = Callable[[str], int]  # 接受字符串并返回其长度的函数

# 初始化一个日志记录器，用于输出程序运行时的信息
log = logging.getLogger(__name__)

# 使用dataclass装饰器定义一个名为Tokenizer的类，它用于处理文本
@dataclass(frozen=True)
class Tokenizer:
    # 定义Tokenizer类的属性
    chunk_overlap: int  # 每个文本块与其他块之间重叠的字符数
    tokens_per_chunk: int  # 每个文本块的最大字符数
    decode: DecodeFn  # 用于将编码后的文本列表解码回原始字符串的函数
    encode: EncodeFn  # 用于将原始字符串编码为整数列表的函数

# 定义一个叫TextSplitter的类，它能帮助我们把大段的文本分成小块
class TextSplitter(ABC):
    """创建一个TextSplitter类，它的任务是把文本切割成小部分"""

    # 这里是一些变量，它们会帮助我们工作
    _chunk_size: int       # 块的大小，默认是8191个字符
    _chunk_overlap: int    # 块之间的重叠，默认是100个字符
    _length_function: LengthFn   # 测量长度的函数，默认用len函数
    _keep_separator: bool  # 是否保留分隔符，默认不保留
    _add_start_index: bool # 是否添加起始索引，默认不添加
    _strip_whitespace: bool # 是否去除空白，默认去除

    # 这个方法叫做__init__，当我们创建TextSplitter对象时会用到
    def __init__(
        self,
        chunk_size: int = 8191,  # 设置块的大小，默认是8191
        chunk_overlap: int = 100,  # 设置块之间重叠的字符数，默认是100
        length_function: LengthFn = len,  # 选择计算长度的函数，默认使用len
        keep_separator: bool = False,  # 决定是否保留分隔符，默认不保留
        add_start_index: bool = False,  # 是否在每个块前加索引，默认不加
        strip_whitespace: bool = True,  # 是否去除空白，默认去除
    ):
        # 把传入的参数赋值给上面定义的变量
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._length_function = length_function
        self._keep_separator = keep_separator
        self._add_start_index = add_start_index
        self._strip_whitespace = strip_whitespace

    # 这是一个需要子类去实现的方法，它告诉我们要怎么分割文本
    @abstractmethod
    def split_text(self, text: str | list[str]) -> Iterable[str]:
        """定义一个方法，用来分割文本，但具体怎么做要看子类怎么做"""


# 定义一个NoopTextSplitter类，它继承自TextSplitter
class NoopTextSplitter(TextSplitter):
    """创建一个NoopTextSplitter类，它不做任何分割，直接返回原文本"""

    # 实现split_text方法，如果输入的是字符串，就把它放到一个列表里返回
    # 如果输入的是列表，就直接返回这个列表
    def split_text(self, text: str | list[str]) -> Iterable[str]:
        """这个方法把文本原样返回，不做任何处理"""
        return [text] if isinstance(text, str) else text

# 定义一个名为TokenTextSplitter的类，它是TextSplitter类的子类
class TokenTextSplitter(TextSplitter):
    """创建一个TokenTextSplitter，用于处理文本的特殊字符。"""

    # 这两个变量用于存储允许和不允许的特殊字符
    _allowed_special: Literal["all"] | set[str]  # 可以是"all"或一个字符串集合
    _disallowed_special: Literal["all"] | Collection[str]  # 可以是"all"或一个字符串集合

    # 初始化TokenTextSplitter
    def __init__(
        self,
        encoding_name: str = "cl100k_base",  # 默认的编码名称
        model_name: str | None = None,  # 模型名称，可以为空
        allowed_special: Literal["all"] | set[str] | None = None,  # 允许的特殊字符，默认为空
        disallowed_special: Literal["all"] | Collection[str] = "all",  # 不允许的特殊字符，默认为"all"
        **kwargs: Any,  # 其他任意参数
    ):
        # 调用父类的初始化方法
        super().__init__(**kwargs)

        # 如果提供了模型名称
        if model_name is not None:
            # 尝试获取该模型的编码
            try:
                enc = tiktoken.encoding_for_model(model_name)
            # 如果找不到模型
            except KeyError:
                # 打印错误日志并使用默认编码
                log.exception("Model %s not found, using %s", model_name, encoding_name)
                enc = tiktoken.get_encoding(encoding_name)
        # 如果没有提供模型名称，直接使用默认编码
        else:
            enc = tiktoken.get_encoding(encoding_name)

        # 设置分词器
        self._tokenizer = enc
        # 如果没有指定允许的特殊字符，设置为空集
        self._allowed_special = allowed_special or set()
        # 如果没有指定不允许的特殊字符，设置为"all"
        self._disallowed_special = disallowed_special

    # 将文本编码为整数列表
    def encode(self, text: str) -> list[int]:
        """将文本转换成数字列表."""
        return self._tokenizer.encode(
            text,
            allowed_special=self._allowed_special,
            disallowed_special=self._disallowed_special,
        )

    # 返回文本中的字符数量
    def num_tokens(self, text: str) -> int:
        """计算文本中字符的数量."""
        return len(self.encode(text))

    # 分割文本
    def split_text(self, text: str | list[str]) -> list[str]:
        """将文本分割成多个部分."""
        # 如果文本是空的或者为None，返回空列表
        if cast(bool, pd.isna(text)) or text == "":
            return []

        # 如果文本是列表，先将它们合并成一个字符串
        if isinstance(text, list):
            text = " ".join(text)

        # 确保文本是字符串类型
        if not isinstance(text, str):
            # 抛出错误，因为尝试分割非字符串类型的数据
            msg = f"试图分割非字符串值，实际类型为 {type(text)}"
            raise TypeError(msg)

        # 创建一个分词器对象
        tokenizer = Tokenizer(
            chunk_overlap=self._chunk_overlap,  # 分块重叠部分
            tokens_per_chunk=self._chunk_size,  # 每个分块的令牌数
            decode=self._tokenizer.decode,  # 使用分词器解码
            encode=lambda text: self.encode(text),  # 使用当前类的编码方法
        )

        # 使用分词器分割文本
        return split_text_on_tokens(text=text, tokenizer=tokenizer)

# 定义一个名为TextListSplitterType的特殊类，它同时继承自str（字符串）和Enum（枚举）
class TextListSplitterType(str, Enum):
    # 这个类是一个枚举，用来表示TextListSplitter的不同的类型，就像一个选择列表
    # ""里面是这个类的描述，告诉人们它的用途
    """定义一个枚举类TextListSplitterType，表示TextListSplitter的类型。"""

    # 这里定义了两种类型，每种类型都有一个名字和对应的值
    # 第一种类型叫DELIMITED_STRING，它的值是"delimited_string"
    DELIMITED_STRING = "delimited_string"
    # 第二种类型叫JSON，它的值是"json"
    JSON = "json"

# 定义一个叫做TextListSplitter的类，它来自TextSplitter类
class TextListSplitter(TextSplitter):
    """创建一个TextListSplitter，用于处理文本列表的分割"""

    # 当我们创建这个类的实例时，运行这个方法
    def __init__(
        self,
        chunk_size: int,         # 块的大小（比如每个部分的长度）
        splitter_type: TextListSplitterType = TextListSplitterType.JSON,  # 分割类型，默认是JSON
        input_delimiter: str | None = None,   # 输入文本的分隔符
        output_delimiter: str | None = None,  # 输出文本的分隔符，默认是换行符
        model_name: str | None = None,     # 模型名称，用于计算文本长度
        encoding_name: str | None = None,   # 编码名称，用于计算文本长度
    ):
        # 调用父类的初始化方法，设置块的重叠为0
        super().__init__(chunk_size, chunk_overlap=0)
        # 存储分割类型
        self._type = splitter_type
        # 存储输入分隔符
        self._input_delimiter = input_delimiter
        # 如果没有提供输出分隔符，则设置为换行符
        self._output_delimiter = output_delimiter or "\n"
        # 定义一个函数来计算文本长度
        self._length_function = lambda x: num_tokens_from_string(
            x, model=model_name, encoding_name=encoding_name
        )

    # 这个方法将文本或文本列表分割成多个小块
    def split_text(self, text: str | list[str]) -> Iterable[str]:
        # 如果没有文本，返回空列表
        if not text:
            return []

        # 初始化结果列表和当前块
        result = []
        current_chunk = []
        # 计算空块的长度（包括括号）
        current_length = self._length_function("[]")

        # 将输入的文本转换为列表
        string_list = self._load_text_list(text)

        # 如果只有一个元素，直接返回
        if len(string_list) == 1:
            return string_list

        # 遍历文本列表
        for item in string_list:
            # 计算当前项的长度（包括逗号）
            item_length = self._length_function(f"{item},")
            
            # 如果加上当前项后超过了块的大小
            if current_length + item_length > self._chunk_size:
                # 如果当前块有内容，将其添加到结果中
                if current_chunk and len(current_chunk) > 0:
                    self._append_to_result(result, current_chunk)
                    # 重新开始一个新的块
                    current_chunk = [item]
                    # 更新长度，只包含当前项
                    current_length = item_length
            else:
                # 将当前项添加到当前块
                current_chunk.append(item)
                # 更新长度，包括逗号
                current_length += item_length

        # 最后，将最后一个块添加到结果中
        self._append_to_result(result, current_chunk)

        # 返回分割后的结果
        return result

    # 根据分割类型加载文本列表
    def _load_text_list(self, text: str | list[str]):
        # 如果已经是列表，直接返回
        if isinstance(text, list):
            string_list = text
        # 如果是JSON格式，解析为列表
        elif self._type == TextListSplitterType.JSON:
            string_list = json.loads(text)
        # 否则，使用输入分隔符分割文本
        else:
            string_list = text.split(self._input_delimiter)
        # 返回处理后的列表
        return string_list

    # 将当前块添加到结果列表，根据分割类型处理
    def _append_to_result(self, chunk_list: list[str], new_chunk: list[str]):
        # 如果当前块有内容
        if new_chunk and len(new_chunk) > 0:
            # 如果是JSON类型，将块转为JSON字符串并添加
            if self._type == TextListSplitterType.JSON:
                chunk_list.append(json.dumps(new_chunk))
            # 否则，使用输出分隔符连接块的元素并添加
            else:
                chunk_list.append(self._output_delimiter.join(new_chunk))

# 定义一个函数，名字叫split_text_on_tokens，它接受两个参数：一个叫text的字符串和一个叫tokenizer的对象
def split_text_on_tokens(*, text: str, tokenizer: Tokenizer) -> list[str]:
    # 这个函数的目的是用tokenizer把输入的文本分割成小块，然后返回这些小块
    """使用tokenizer将输入的文本分割成小块并返回。"""
    # 创建一个空列表，用来存放分割后的小块文本
    splits: list[str] = []
    # 使用tokenizer的encode方法，把输入的text转换成一组数字（叫做input_ids）
    input_ids = tokenizer.encode(text)
    # 初始化一个起始索引，设为0
    start_idx = 0
    # 计算当前索引，它是起始索引加上每块的最大令牌数，但不超过input_ids的长度
    cur_idx = min(start_idx + tokenizer.tokens_per_chunk, len(input_ids))
    # 根据起始索引和当前索引取出一块令牌
    chunk_ids = input_ids[start_idx:cur_idx]
    # 当起始索引小于input_ids的长度时，继续循环
    while start_idx < len(input_ids):
        # 把这一块令牌转换回文本，添加到splits列表中
        splits.append(tokenizer.decode(chunk_ids))
        # 更新起始索引，增加每块令牌数减去块之间的重叠数
        start_idx += tokenizer.tokens_per_chunk - tokenizer.chunk_overlap
        # 计算新的当前索引，与之前相同的方式
        cur_idx = min(start_idx + tokenizer.tokens_per_chunk, len(input_ids))
        # 更新chunk_ids，取新的令牌块
        chunk_ids = input_ids[start_idx:cur_idx]
    # 循环结束后，返回分割好的文本小块列表
    return splits

