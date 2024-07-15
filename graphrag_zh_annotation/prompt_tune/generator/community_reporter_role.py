# 导入需要的工具，这两个库帮助我们生成和处理文本
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt import (
    GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT,
)

# 这是微软公司的版权信息，告诉我们代码的许可协议是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块的说明，用来创建社区报告者角色，用于总结社区信息
"""Generate a community reporter role for community summarization."""

# 再次导入之前用到的工具，这样我们可以在函数里使用它们
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt import (
    GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT,
)


# 定义一个异步函数，用来生成社区报告者角色
async def generate_community_reporter_role(
    # 输入一个用于生成文本的智能模型
    llm: CompletionLLM,
    # 输入领域名称，比如“科学”或“艺术”
    domain: str,
    # 输入报告者的身份或特点
    persona: str,
    # 输入关于这个领域的信息，可以是一个字符串或一个字符串列表
    docs: str | list[str]
) -> str:
    """这个函数会用给定的信息创建一个角色描述。

    参数：
    - llm：我们要用的文本生成模型
    - domain：我们要描述的领域
    - persona：报告者的身份
    - docs：关于领域的文字资料

    返回：
    - 生成的领域角色描述（一个字符串）
    """
    # 如果输入的docs是一个列表，就把它合并成一个空格分隔的字符串
    docs_str = " ".join(docs) if isinstance(docs, list) else docs
    # 使用模板来构建我们要问模型的问题，包含领域、身份和文档信息
    domain_prompt = GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT.format(
        domain=domain, persona=persona, input_text=docs_str
    )

    # 使用模型生成回答
    response = await llm(domain_prompt)

    # 把模型的输出转换成字符串并返回
    return str(response.output)

