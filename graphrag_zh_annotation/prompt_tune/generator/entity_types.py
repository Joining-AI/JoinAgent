# 导入必要的库，这些库可以帮助我们处理语言和生成文本
from graphrag.llm.types.llm_types import CompletionLLM  # 引入用于完成任务的语言模型类
from graphrag.prompt_tune.generator.defaults import DEFAULT_TASK  # 引入默认任务设置
from graphrag.prompt_tune.prompt.entity_types import (
    ENTITY_TYPE_GENERATION_JSON_PROMPT,  # JSON模式下的实体类型提示
    ENTITY_TYPE_GENERATION_PROMPT,  # 非JSON模式下的实体类型提示
)

# 版权信息，表示这是微软公司的代码，遵循MIT许可证
# """这是一个用于微调实体类型生成的模块。"""

# 定义一个异步函数，用于从文档中生成实体类型类别
async def generate_entity_types(
    llm: CompletionLLM,  # 输入：完成任务的语言模型
    domain: str,  # 输入：领域名称，例如“历史”或“科学”
    persona: str,  # 输入：角色设定，描述对话中的“身份”
    docs: str | list[str],  # 输入：文档或文档列表，可以是单个字符串或多个字符串
    task: str = DEFAULT_TASK,  # 输入：任务模板，默认使用默认任务
    json_mode: bool = False,  # 输入：是否以JSON格式返回结果，默认为False
) -> str | list[str]:  # 输出：生成的实体类型，可能是字符串（非JSON）或列表（JSON）

    # 格式化任务模板，将领域名插入其中
    formatted_task = task.format(domain=domain)

    # 如果输入的文档是列表，将它们合并成一个字符串，用换行符分隔
    docs_str = "\n".join(docs) if isinstance(docs, list) else docs

    # 根据json_mode选择合适的实体类型提示
    entity_types_prompt = (
        ENTITY_TYPE_GENERATION_JSON_PROMPT
        if json_mode
        else ENTITY_TYPE_GENERATION_PROMPT
    ).format(task=formatted_task, input_text=docs_str)

    # 创建历史记录，包含系统角色和角色设定
    history = [{"role": "system", "content": persona}]

    # 使用语言模型处理提示并获取响应
    response = await llm(entity_types_prompt, history=history, json=json_mode)

    # 如果是JSON模式，返回解析后的"entity_types"部分，如果没有则返回空列表
    if json_mode:
        return (response.json or {}).get("entity_types", [])

    # 如果不是JSON模式，返回响应的输出文本
    return str(response.output)

