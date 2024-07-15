# 导入两个特别的工具，它们帮助我们生成和处理文本
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt.domain import GENERATE_DOMAIN_PROMPT

# 这是微软公司的版权信息，告诉我们代码是他们的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块是关于为GraphRAG提示生成领域内容的

# 再次导入需要的工具，确保我们不会丢失任何东西
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt.domain import GENERATE_DOMAIN_PROMPT


# 定义一个异步函数，它会帮我们生成一个用于GraphRAG提示的领域人格
async def generate_domain(llm, docs):
    """用给定的信息生成一个用于GraphRAG提示的领域描述。

    参数：
    - llm (CompletionLLM): 用来生成文本的智能助手
    - docs (字符串或列表): 我们要基于其生成领域描述的信息

    返回：
    - 字符串: 生成的领域提示响应。
    """
    # 如果输入的docs是个列表，我们就把所有内容连成一个字符串
    docs_str = " ".join(docs) if isinstance(docs, list) else docs

    # 使用一个模板来创建领域提示，模板里的input_text会被替换为输入文档的内容
    domain_prompt = GENERATE_DOMAIN_PROMPT.format(input_text=docs_str)

    # 让智能助手llm根据提示生成回复
    response = await llm(domain_prompt)

    # 将智能助手的回复转换为字符串并返回
    return str(response.output)

