# 导入必要的模块，这些模块帮助我们处理数据和进度条
from collections.abc import Iterable  # 一个接口，表示可以迭代的对象，像列表或集合
from typing import Any  # 表示任何类型的变量
import nltk  # 一个用于自然语言处理的库
from datashaper import ProgressTicker  # 用于显示进度的工具
from .typing import TextChunk  # 自定义的数据类型，代表文本片段

# 这段代码的版权信息，是微软公司的，并遵循MIT许可证

# 定义一个模块，里面有一个run方法
def run(
    # 输入参数：一个字符串列表
    input: list[str], 
    # 其他参数，是一个字典，键是字符串，值可以是任何类型
    _args: dict[str, Any], 
    # 进度条对象，用来追踪进度
    tick: ProgressTicker
) -> Iterable[TextChunk]: 
    """这个方法会把大段文本分成多个小段。就像流水线上的一个步骤。"""
    
    # 遍历输入的每一段文本
    for doc_idx, text in enumerate(input):
        # 使用nltk库，将文本分割成句子
        sentences = nltk.sent_tokenize(text)
        
        # 再次遍历每句话
        for sentence in sentences:
            # 创建一个TextChunk对象，包含句子内容和它来自的原文索引
            yield TextChunk(
                text_chunk=sentence,  # 句子内容
                source_doc_indices=[doc_idx],  # 来源文档的索引
            )
        
        # 每处理完一段文本，更新进度条
        tick(1)  # 告诉进度条我们已经完成了一个单位的工作

