# 导入一个叫做Path的工具，它帮助我们处理文件路径
from pathlib import Path
# 从graphrag.prompt_tune.template模块中导入一个叫做COMMUNITY_REPORT_SUMMARIZATION_PROMPT的变量
from graphrag.prompt_tune.template import COMMUNITY_REPORT_SUMMARIZATION_PROMPT
# 这是微软公司2024年的版权信息，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块是用来生成社区报告摘要的提示的
"""Module for generating prompts for community report summarization."""

# 再次导入Path，确保我们能用到这个工具
from pathlib import Path

# 使用之前导入的COMMUNITY_REPORT_SUMMARIZATION_PROMPT模板
from graphrag.prompt_tune.template import COMMUNITY_REPORT_SUMMARIZATION_PROMPT

# 定义一个文件名，用于存储社区报告摘要
COMMUNITY_SUMMARIZATION_FILENAME = "community_report.txt"

# 定义一个函数，用来创建社区报告摘要的提示
def create_community_summarization_prompt(
    # 输入参数1：代表提示中的人物性格
    persona: str,
    # 输入参数2：代表提示中的角色
    role: str,
    # 输入参数3：描述报告评分的短语
    report_rating_description: str,
    # 输入参数4：使用的语言
    language: str,
    # 输入参数5（可选）：保存提示的文件路径。默认为None，表示不保存到文件
    output_path: Path | None = None,
) -> str:
    # 使用模板填充参数，生成社区报告摘要的提示
    prompt = COMMUNITY_REPORT_SUMMARIZATION_PROMPT.format(
        persona=persona,
        role=role,
        report_rating_description=report_rating_description,
        language=language,
    )

    # 如果提供了输出路径
    if output_path:
        # 创建路径所需的目录，如果已经存在则不报错
        output_path.mkdir(parents=True, exist_ok=True)

        # 构建完整的文件路径
        output_path = output_path / COMMUNITY_SUMMARIZATION_FILENAME
        # 将提示写入到文件中
        with output_path.open("w") as file:
            file.write(prompt)

    # 返回生成的社区报告摘要提示
    return prompt

