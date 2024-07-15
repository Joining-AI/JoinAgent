# 导入日志模块，用于记录程序运行信息
import logging

# 导入numbers模块，用于处理数字类型
import numbers

# 导入正则表达式模块，用于文本匹配和操作
import re

# 导入traceback模块，用于处理异常堆栈信息
import traceback

# 从collections.abc导入Mapping，这是一个抽象基类，表示键值对的数据结构
from collections.abc import Mapping

# 从dataclasses模块导入dataclass装饰器，用于创建数据类
from dataclasses import dataclass

# 导入typing模块中的Any类型，表示任何类型
from typing import Any

# 导入networkx模块，用于处理图数据结构
import networkx as nx

# 导入tiktoken模块，可能是一个自定义的文本处理库
import tiktoken

# 导入默认配置
import graphrag.config.defaults as defs

# 从graphrag.index相关的模块导入错误处理函数类型和工具函数
from graphrag.index.typing import ErrorHandlerFn
from graphrag.index.utils import clean_str

# 导入CompletionLLM类，可能是一个语言模型完成任务的类
from graphrag.llm import CompletionLLM

# 导入提示字符串
from .prompts import CONTINUE_PROMPT, GRAPH_EXTRACTION_PROMPT, LOOP_PROMPT

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了'GraphExtractionResult'和'GraphExtractor'两个模型的定义

# 定义默认的分隔符常量
DEFAULT_TUPLE_DELIMITER = "<|>"
DEFAULT_RECORD_DELIMITER = "##"
DEFAULT_COMPLETION_DELIMITER = "<|COMPLETE|>"
DEFAULT_ENTITY_TYPES = ["organization", "person", "geo", "event"]


# 使用dataclass装饰器创建一个类，表示单一方形图提取的结果
@dataclass
class GraphExtractionResult:
    # 结果是一个networkx的图对象
    output: nx.Graph
    # 源文档，字典类型，键和值可以是任何类型
    source_docs: dict[Any, Any]



# 定义一个名为_unpack_descriptions的函数，它接受一个像字典的东西（Mapping）作为参数，返回值是一个字符串列表
def _unpack_descriptions(data: Mapping) -> list[str]:
    # 从data中尝试获取"描述"（description）这个键对应的值，如果没有就返回None
    value = data.get("description", None)
    # 如果value是None，那么返回一个空列表
    return [] if value is None else value.split("\n")  # 如果value不是None，就把它按换行符("\n")分割成多个字符串，然后返回这个列表

# 定义一个名为_unpack_source_ids的函数，它也接受一个像字典的东西（Mapping）作为参数，返回值是一个字符串列表
def _unpack_source_ids(data: Mapping) -> list[str]:
    # 从data中尝试获取"源ID"（source_id）这个键对应的值，如果没有就返回None
    value = data.get("source_id", None)
    # 如果value是None，那么返回一个空列表
    return [] if value is None else value.split(", ")  # 如果value不是None，就把它按逗号和空格(", ")分割成多个字符串，然后返回这个列表

