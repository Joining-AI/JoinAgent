# 导入一个叫做Path的模块，它帮助我们处理文件路径
from pathlib import Path

# 导入graphrag配置中的默认设置
import graphrag.config.defaults as defs

# 从graphrag.index.utils.tokens模块中导入一个函数，这个函数可以计算字符串里的令牌（比如单词）数量
from graphrag.index.utils.tokens import num_tokens_from_string

# 从graphrag.prompt_tune.template模块中导入多个模板，这些模板用于生成提示信息
from graphrag.prompt_tune.template import (
    EXAMPLE_EXTRACTION_TEMPLATE,  # 一个示例提取的模板
    GRAPH_EXTRACTION_JSON_PROMPT,  # 用于图形提取的JSON格式的提示
    GRAPH_EXTRACTION_PROMPT,  # 用于图形提取的普通提示
    UNTYPED_EXAMPLE_EXTRACTION_TEMPLATE,  # 未指定类型的示例提取模板
    UNTYPED_GRAPH_EXTRACTION_PROMPT,  # 未指定类型的图形提取提示
)

# 这是一个版权信息，表示代码由微软公司2024年创建，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个模块的文档字符串，描述了这个模块是做什么的
"""实体提取提示生成器模块。"""

# 定义一个变量，它的值是"entity_extraction.txt"，这可能是要保存或读取的文件名
ENTITY_EXTRACTION_FILENAME = "entity_extraction.txt"

# 定义一个函数，创建实体提取的提示
def create_entity_extraction_prompt(
    # 参数1：要提取的实体类型，可以是字符串、列表或None
    entity_types: str | list[str] | None,
    # 参数2：包含要提取实体的文档列表
    docs: list[str],
    # 参数3：用于实体提取的例子列表
    examples: list[str],
    # 参数4：输入和输出的语言
    language: str,
    # 参数5：提示中最大允许的单词数
    max_token_count: int,
    # 参数6：用于计算单词数的模型名称，默认值
    encoding_model: str = defs.ENCODING_MODEL,
    # 参数7：是否使用JSON模式，默认为False
    json_mode: bool = False,
    # 参数8：写入提示的文件路径，如果为None，则不写入文件，默认为None
    output_path: Path | None = None,
) -> str:
    """
    创建一个用于实体提取的提示。

    参数
    ------
    - entity_types (str | list[str]): 要提取的实体类型
    - docs (list[str]): 提取实体的文档列表
    - examples (list[str]): 用于实体提取的例子
    - language (str): 输入和输出的语言
    - encoding_model (str): 计算单词数的模型名称
    - max_token_count (int): 提示中的最大单词数
    - json_mode (bool): 是否使用JSON模式，默认为False
    - output_path (Path | None): 写入提示的文件路径，默认为None，不写入文件
    返回
    ------
    - str: 实体提取提示
    """
    
    # 根据json_mode选择提示模板
    prompt = (
        (GRAPH_EXTRACTION_JSON_PROMPT if json_mode else GRAPH_EXTRACTION_PROMPT)
        if entity_types
        else UNTYPED_GRAPH_EXTRACTION_PROMPT
    )

    # 如果entity_types是列表，将其转换为逗号分隔的字符串
    if isinstance(entity_types, list):
        entity_types = ", ".join(entity_types)

    # 计算剩余的单词数
    tokens_left = (
        max_token_count
        - num_tokens_from_string(prompt, model=encoding_model)
        - num_tokens_from_string(entity_types, model=encoding_model)
        if entity_types
        else 0
    )

    # 初始化例子的提示部分
    examples_prompt = ""

    # 遍历例子，直到没有单词数或例子用完
    for i, output in enumerate(examples):
        input = docs[i]
        # 根据entity_types是否有值，格式化例子
        example_formatted = (
            EXAMPLE_EXTRACTION_TEMPLATE.format(
                n=i + 1, input_text=input, entity_types=entity_types, output=output
            )
            if entity_types
            else UNTYPED_EXAMPLE_EXTRACTION_TEMPLATE.format(
                n=i + 1, input_text=input, output=output
            )
        )

        # 计算格式化例子的单词数
        example_tokens = num_tokens_from_string(example_formatted, model=encoding_model)

        # 如果单词数超过剩余的，跳出循环
        if i > 0 and example_tokens > tokens_left:
            break

        # 添加格式化例子到例子提示部分，并减少剩余的单词数
        examples_prompt += example_formatted
        tokens_left -= example_tokens

    # 格式化最终的提示
    prompt = (
        prompt.format(
            entity_types=entity_types, examples=examples_prompt, language=language
        )
        if entity_types
        else prompt.format(examples=examples_prompt, language=language)
    )

    # 如果有输出路径，创建目录并写入文件
    if output_path:
        output_path.mkdir(parents=True, exist_ok=True)

        output_path = output_path / ENTITY_EXTRACTION_FILENAME
        # 打开文件并写入提示
        with output_path.open("w") as file:
            file.write(prompt)

    # 返回最终的提示
    return prompt

