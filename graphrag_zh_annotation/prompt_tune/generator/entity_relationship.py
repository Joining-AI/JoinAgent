# 这段代码是用Python写的，它做了一些关于生成实体关系的例子的事情。
# 让我们逐行解释一下：

# 第1行：导入一个叫做asyncio的库，这个库帮助我们处理异步操作，就像在等待事情完成时可以先做其他事情。
# 第2行：导入json库，这个库用来处理和读写JSON格式的数据，一种常见的数据交换格式。
# 第3行：从graphrag.llm.types.llm_types模块导入CompletionLLM类，这个类可能用于完成某种任务。
# 第4-7行：从graphrag.prompt_tune.prompt模块导入了三个常量，它们是生成实体关系的提示字符串。

# 第8-10行：这是版权信息，告诉我们这段代码是由微软公司2024年写的，使用的是MIT许可证。

# 第11行：定义了一个名为"Entity relationship example generation module."的字符串，虽然不执行任何操作，但可能是对代码功能的描述。

# 第12行：再次导入asyncio，确保我们可以在下面的代码中使用它。
# 第13行：再次导入json，同样是为了在后面使用。

# 第14行：从graphrag.llm.types.llm_types导入CompletionLLM，和上面一样。
# 第15-17行：再次导入那些提示字符串，这可能是因为它们在代码中被多次使用。

# 第18行：定义了一个变量MAX_EXAMPLES，它的值是5，表示最多生成5个例子。

# 定义一个异步函数generate_entity_relationship_examples，接收几个参数
async def generate_entity_relationship_examples(
    # llm：一个用于完成任务的语言模型
    llm: CompletionLLM,
    # persona：代表角色的字符串
    persona: str,
    # entity_types：可以是单个字符串、字符串列表或None，表示实体类型
    entity_types: str | list[str] | None,
    # docs：可以是单个字符串或字符串列表，包含要处理的文本
    docs: str | list[str],
    # language：使用的语言
    language: str,
    # json_mode：默认为False，决定输出是JSON格式还是其他格式
    json_mode: bool = False,
) -> list[str]:
    """生成用于创建实体配置的实体/关系示例列表。

    根据json_mode参数，返回的结果可能是JSON格式或分隔符格式。
    """
    
    # 如果docs是一个字符串，将其转换为列表
    docs_list = [docs] if isinstance(docs, str) else docs
    # 创建历史记录，第一条记录是系统角色和persona内容
    history = [{"role": "system", "content": persona}]

    # 如果提供了entity_types
    if entity_types:
        # 如果entity_types是字符串，直接使用；如果是列表，用逗号连接成字符串
        entity_types_str = entity_types if isinstance(entity_types, str) else ", ".join(entity_types)

        # 根据json_mode，构建不同提示信息的列表
        messages = [
            (
                # JSON模式的提示
                ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT
                if json_mode
                else ENTITY_RELATIONSHIPS_GENERATION_PROMPT
            ).format(  # 提示信息中包含实体类型、输入文本和语言
                entity_types=entity_types_str, input_text=doc, language=language
            )
            for doc in docs_list
        ]
    else:
        # 没有提供entity_types时，使用另一种提示信息
        messages = [
            UNTYPED_ENTITY_RELATIONSHIPS_GENERATION_PROMPT.format(
                input_text=doc, language=language
            )
            for doc in docs_list
        ]

    # 取前MAX_EXAMPLES个消息
    messages = messages[:MAX_EXAMPLES]

    # 使用llm模型处理每个消息，创建任务列表
    tasks = [llm(message, history=history, json=json_mode) for message in messages]

    # 异步执行所有任务并获取响应
    responses = await asyncio.gather(*tasks)

    # 根据json_mode，将响应转换为JSON字符串或普通字符串，然后放入列表返回
    return [
        json.dumps(response.json or "") if json_mode else str(response.output)
        for response in responses
    ]

