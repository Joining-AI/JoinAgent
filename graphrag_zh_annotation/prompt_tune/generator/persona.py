# 导入需要的库，它们帮助我们生成个性化的文本
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.generator.defaults import DEFAULT_TASK
from graphrag.prompt_tune.prompt import GENERATE_PERSONA_PROMPT

# 这是微软公司的版权信息，告诉我们代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块用来创建用于GraphRAG提示的个性化角色

# 从graphrag导入我们需要的类和常量
from graphrag.llm.types.llm_types import CompletionLLM
from graphrag.prompt_tune.generator.defaults import DEFAULT_TASK
from graphrag.prompt_tune.prompt import GENERATE_PERSONA_PROMPT


# 定义一个异步函数，用来生成个性化的角色
async def generate_persona(llm, domain, task=DEFAULT_TASK):
    # 这个函数的作用是用特定的LLM（语言模型）生成一个用于GraphRAG的个性角色

    # 根据给定的领域，格式化任务字符串
    formatted_task = task.format(domain=domain)

    # 创建一个用于生成个性角色的提示，把格式化的任务加入其中
    persona_prompt = GENERATE_PERSONA_PROMPT.format(sample_task=formatted_task)

    # 使用LLM来响应这个提示，得到生成的文本
    response = await llm(persona_prompt)

    # 将LLM的输出转换成字符串并返回
    return str(response.output)

