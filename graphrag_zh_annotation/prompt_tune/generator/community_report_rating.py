# 导入两个库，它们包含我们需要的工具
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.prompt import (
    GENERATE_REPORT_RATING_PROMPT,
)

# 这是一个版权信息，告诉我们这个代码是微软公司的，并且遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个异步函数（需要等待结果的函数），用于生成社区报告评级的描述
async def generate_community_report_rating(
    llm: CompletionLLM,  # 输入：一个用于生成内容的语言模型
    domain: str,  # 输入：要为其生成评级的领域（比如“环保”）
    persona: str,  # 输入：生成评级时使用的角色或身份
    docs: str | list[str]  # 输入：提供上下文的文档，可以是单个字符串或字符串列表
) -> str:  # 返回：生成的评级描述

    # 如果输入的文档是列表，将它们合并成一个空格分隔的字符串
    docs_str = " ".join(docs) if isinstance(docs, list) else docs

    # 使用模板来构建一个提示，包含领域、角色和文档信息
    domain_prompt = GENERATE_REPORT_RATING_PROMPT.format(
        domain=domain, persona=persona, input_text=docs_str
    )

    # 使用语言模型处理这个提示，获取响应
    response = await llm(domain_prompt)

    # 从响应中提取输出文本，去除两侧的空白字符，然后返回
    return str(response.output).strip()

