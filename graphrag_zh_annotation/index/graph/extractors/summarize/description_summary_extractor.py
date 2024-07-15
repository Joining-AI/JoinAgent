# 导入json模块，用于处理JSON格式的数据
import json

# 从dataclasses模块导入dataclass装饰器，用于定义数据类
from dataclasses import dataclass

# 从graphrag.index.typing模块导入ErrorHandlerFn，它是一个错误处理函数类型
from graphrag.index.typing import ErrorHandlerFn

# 从graphrag.index.utils.tokens模块导入num_tokens_from_string函数，计算字符串中的令牌数量
from graphrag.index.utils.tokens import num_tokens_from_string

# 从graphrag.llm模块导入CompletionLLM类，可能是一个语言模型完成类
from graphrag.llm import CompletionLLM

# 从当前模块的prompts子模块导入SUMMARIZE_PROMPT常量，可能是一个总结提示
from .prompts import SUMMARIZE_PROMPT

# 微软公司的版权声明，使用MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含'GraphExtractionResult'和'GraphExtractor'模型的代码

# 定义一个最大输入提示的令牌数
DEFAULT_MAX_INPUT_TOKENS = 4_000
# 定义最大语言模型答案的令牌数
DEFAULT_MAX_SUMMARY_LENGTH = 500

# 使用dataclass装饰器定义一个类'SummarizationResult'
@dataclass
class SummarizationResult:
    # 类中有一个名为'items'的属性，可以是字符串或字符串元组
    items: str | tuple[str, str]
    # 还有一个名为'description'的属性，是字符串类型
    description: str

# 定义一个名为SummarizeExtractor的类，它的作用是提取和总结信息
class SummarizeExtractor:
    # 这个类里有一些变量，它们用来存储不同的数据
    _llm: CompletionLLM          # 一个用于完成任务的语言模型
    _entity_name_key: str       # 关联实体名称的键
    _input_descriptions_key: str # 输入描述列表的键
    _summarization_prompt: str   # 总结提示语
    _on_error: ErrorHandlerFn    # 错误处理函数
    _max_summary_length: int     # 最大总结长度
    _max_input_tokens: int       # 最大输入令牌数

    # 类的初始化方法，用来设置这些变量的值
    def __init__(
        self,
        llm_invoker,               # 给定的语言模型调用器
        entity_name_key=None,      # 如果没有提供，实体名称键默认为"entity_name"
        input_descriptions_key=None, # 如果没有提供，输入描述键默认为"description_list"
        summarization_prompt=None,  # 如果没有提供，总结提示语默认为SUMMARIZE_PROMPT
        on_error=None,             # 如果没有提供，错误处理函数默认不做任何操作
        max_summary_length=None,   # 如果没有提供，最大总结长度默认为DEFAULT_MAX_SUMMARY_LENGTH
        max_input_tokens=None,     # 如果没有提供，最大输入令牌数默认为DEFAULT_MAX_INPUT_TOKENS
    ):
        # 设置变量的值
        self._llm = llm_invoker
        self._entity_name_key = entity_name_key or "entity_name"
        self._input_descriptions_key = input_descriptions_key or "description_list"
        self._summarization_prompt = summarization_prompt or SUMMARIZE_PROMPT
        self._on_error = on_error or (lambda _e, _s, _d: None)
        self._max_summary_length = max_summary_length or DEFAULT_MAX_SUMMARY_LENGTH
        self._max_input_tokens = max_input_tokens or DEFAULT_MAX_INPUT_TOKENS

    # 当我们像函数一样调用这个类的对象时，会执行这个方法
    async def __call__(
        self,
        items,                     # 可能是字符串或元组的物品
        descriptions,             # 描述物品的列表
    ):
        # 根据描述的数量返回不同的结果
        if len(descriptions) == 0:
            result = ""  # 没有描述时返回空字符串
        elif len(descriptions) == 1:
            result = descriptions[0]  # 只有一个描述时直接返回
        else:
            result = await self._summarize_descriptions(items, descriptions)  # 多个描述时进行总结

        # 返回一个包含物品和总结结果的对象
        return SummarizationResult(items, result or "")

    # 私有方法，用于总结多个描述
    async def _summarize_descriptions(
        self, items, descriptions
    ):
        # 对物品排序（如果是个列表）
        sorted_items = sorted(items) if isinstance(items, list) else items

        # 确保描述是一个列表
        if not isinstance(descriptions, list):
            descriptions = [descriptions]

        # 初始化一些变量
        usable_tokens = self._max_input_tokens - num_tokens_from_string(self._summarization_prompt)
        descriptions_collected = []
        result = ""

        # 遍历描述，直到达到最大输入令牌数
        for i, description in enumerate(descriptions):
            usable_tokens -= num_tokens_from_string(description)
            descriptions_collected.append(description)

            # 如果令牌数不足或所有描述都已添加，进行总结
            if (usable_tokens < 0 and len(descriptions_collected) > 1) or (i == len(descriptions) - 1):
                # 使用语言模型进行总结
                result = await self._summarize_descriptions_with_llm(sorted_items, descriptions_collected)

                # 如果还有描述需要处理，重置变量
                if i != len(descriptions) - 1:
                    descriptions_collected = [result]
                    usable_tokens = (
                        self._max_input_tokens
                        - num_tokens_from_string(self._summarization_prompt)
                        - num_tokens_from_string(result)
                    )

        # 返回总结结果
        return result

    # 私有方法，使用语言模型进行总结
    async def _summarize_descriptions_with_llm(
        self, items, descriptions
    ):
        # 使用语言模型进行总结，并获取结果
        response = await self._llm(
            self._summarization_prompt,
            name="summarize",
            variables={
                self._entity_name_key: json.dumps(items),
                self._input_descriptions_key: json.dumps(sorted(descriptions)),
            },
            model_parameters={"max_tokens": self._max_summary_length},
        )
        # 将结果转换为字符串并返回
        return str(response.output)

