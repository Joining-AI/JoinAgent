# 导入两个特别的工具，它们帮助我们处理语言和提示
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt import DETECT_LANGUAGE_PROMPT

# 这是微软公司2024年的版权信息，它告诉我们这个代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件是用来检测GraphRAG提示的语言的

# 再次导入之前提到的两个工具，确保我们能用它们
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt import DETECT_LANGUAGE_PROMPT


# 定义一个函数，叫做detect_language，它会找出用于GraphRAG提示的语言
async def detect_language(llm: CompletionLLM, docs: str | list[str]) -> str:
    # 这个函数需要两个东西：一个叫llm的工具，用来生成文字；另一样是docs，可以是一段文字或是一串文字列表
    # 函数会返回检测到的语言

    # 如果docs是个列表，我们就把所有文字连接成一个长句子
    docs_str = " ".join(docs) if isinstance(docs, list) else docs
    # 使用一个特别的模板（DETECT_LANGUAGE_PROMPT）来创建一个检测语言的提示，把要检测的文字放进去
    language_prompt = DETECT_LANGUAGE_PROMPT.format(input_text=docs_str)

    # 让llm工具根据提示生成一个响应
    response = await llm(language_prompt)

    # 最后，从响应中取出检测到的语言并以字符串形式返回
    return str(response.output)

