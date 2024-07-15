# 这段代码是用来运行一种叫做"图智能"的程序的。它有三个主要的功能：run_gi、run_resolve_entities和_create_text_list_splitter。

# 首先，它导入了一些必要的库和模块，这些库和模块帮助处理数据、设置选项、缓存处理结果等。
from datashaper import VerbCallbacks            # 导入VerbCallbacks，用于处理任务的回调函数
from graphrag.config.enums import LLMType       # 导入LLMType，这是一个定义了不同类型的LLM（语言逻辑模型）的枚举类型
from graphrag.index.cache import PipelineCache   # 导入PipelineCache，用于存储处理管道的结果
from graphrag.index.graph.extractors.summarize import SummarizeExtractor  # 导入SummarizeExtractor，用于提取信息
from graphrag.index.llm import load_llm         # 导入load_llm，用于加载LLM
from graphrag.index.verbs.entities.summarize.strategies.typing import (
    StrategyConfig,
    SummarizedDescriptionResult,
) # 导入策略配置和总结描述结果的数据结构
from graphrag.llm import CompletionLLM          # 导入CompletionLLM，完成型的语言逻辑模型
from .defaults import DEFAULT_LLM_CONFIG       # 导入默认的LLM配置

# 下面是版权声明，表示这段代码的版权属于微软公司，并遵循MIT许可证。

# 定义了一个名为"run"的异步函数，这个函数用于执行图智能的实体提取策略。
async def run(
    described_items: str | tuple[str, str],  # 输入的被描述的项目，可以是字符串或字符串对
    descriptions: list[str],                 # 描述列表
    reporter: VerbCallbacks,                 # 回调函数，用于报告任务进度
    pipeline_cache: PipelineCache,           # 处理管道的缓存
    args: StrategyConfig,                    # 策略配置对象
) -> SummarizedDescriptionResult:            # 返回总结后的描述结果

    # 从策略配置中获取LLM的配置，如果没有就使用默认配置
    llm_config = args.get("llm", DEFAULT_LLM_CONFIG)

    # 根据配置获取LLM的类型，如果没有就用默认类型（StaticResponse）
    llm_type = llm_config.get("type", LLMType.StaticResponse)

    # 加载对应的LLM，根据类型、报告器、缓存和配置
    llm = load_llm(
        "summarize_descriptions", llm_type, reporter, pipeline_cache, llm_config
    )

    # 调用run_summarize_descriptions函数，传入LLM和其他参数，返回总结后的描述结果
    return await run_summarize_descriptions(
        llm, described_items, descriptions, reporter, args
    )

# 定义一个异步函数，用于运行摘要和提取描述的程序
async def run_summarize_descriptions(
    llm: CompletionLLM,  # 输入一个能完成任务的语言模型
    items: str | tuple[str, str],  # 输入可以是字符串或包含两个字符串的元组
    descriptions: list[str],  # 输入是一串描述的列表
    reporter: VerbCallbacks,  # 输入一个用于报告进度和错误的对象
    args: StrategyConfig,  # 输入包含策略配置的字典
) -> SummarizedDescriptionResult:  # 函数返回一个总结后的描述结果

    """这个函数是用来执行实体提取的流程。"""
    
    # 从配置中获取提取参数
    summarize_prompt = args.get("summarize_prompt", None)  # 获取摘要提示，如果没有就设为None
    entity_name_key = args.get("entity_name_key", "entity_name")  # 获取实体名称的键，默认是"entity_name"
    input_descriptions_key = args.get("input_descriptions_key", "description_list")  # 获取输入描述的键，默认是"description_list"
    max_tokens = args.get("max_tokens", None)  # 获取最大令牌数，如果没有就设为None

    # 创建一个用于摘要和提取的类实例
    extractor = SummarizeExtractor(
        llm_invoker=llm,  # 使用前面的语言模型
        summarization_prompt=summarize_prompt,  # 设置摘要提示
        entity_name_key=entity_name_key,  # 设置实体名称的键
        input_descriptions_key=input_descriptions_key,  # 设置输入描述的键
        on_error=lambda e, stack, details: (  # 当出错时，报告错误
            reporter.error("Entity Extraction Error", e, stack, details)
            if reporter
            else None
        ),
        max_summary_length=args.get("max_summary_length", None),  # 设置最大摘要长度
        max_input_tokens=max_tokens,  # 设置最大输入令牌数
    )

    # 调用提取器的方法处理输入
    result = await extractor(items=items, descriptions=descriptions)  # 等待异步处理完成

    # 返回一个包含处理后项目的结构化结果
    return SummarizedDescriptionResult(
        items=result.items,  # 结果中的项目
        description=result.description  # 结果中的描述
    )

