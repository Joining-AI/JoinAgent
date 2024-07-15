# 导入一个叫做Path的工具，它帮助我们处理文件路径
from pathlib import Path
# 从graphrag.prompt_tune.template模块中导入一个名为ENTITY_SUMMARIZATION_PROMPT的字符串模板
from graphrag.prompt_tune.template import ENTITY_SUMMARIZATION_PROMPT

# 这段代码的版权属于2024年的微软公司
# 并且遵循MIT许可证的规定
# """后面的文字是模块的描述，说明这是一个实体总结提示生成模块

# 定义一个文件名，用于保存实体总结的提示
ENTITY_SUMMARIZATION_FILENAME = "summarize_descriptions.txt"

# 定义一个函数，用来创建实体总结的提示
def create_entity_summarization_prompt(
    # 输入参数：代表要用于提示的人物描述
    persona: str,
    # 输入参数：代表要使用的语言
    language: str,
    # 输入参数（可选）：如果提供，将提示写入这个路径的文件
    output_path: Path | None = None,
) -> str:
    # 使用ENTITY_SUMMARIZATION_PROMPT模板，替换persona和language的值，生成提示
    prompt = ENTITY_SUMMARIZATION_PROMPT.format(persona=persona, language=language)

    # 如果提供了output_path
    if output_path:
        # 确保output_path所在的目录存在，如果不存在则创建，如果已存在则不报错
        output_path.mkdir(parents=True, exist_ok=True)

        # 构建完整的文件路径
        output_path = output_path / ENTITY_SUMMARIZATION_FILENAME
        # 打开文件，准备写入
        with output_path.open("w") as file:
            # 将生成的提示写入文件
            file.write(prompt)

    # 返回生成的提示
    return prompt

