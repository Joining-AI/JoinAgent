# 导入路径模块，用来处理文件路径
from pathlib import Path

# 导入NoopVerbCallbacks，它可能是一个不做任何操作的回调函数类
from datashaper import NoopVerbCallbacks

# 导入GraphRagConfig类，它是图形推理配置的一部分
from graphrag.config.models.graph_rag_config import GraphRagConfig

# 导入load_llm函数，用于加载语言模型
from graphrag.index.llm import load_llm

# 导入PrintProgressReporter类，用于显示进度报告
from graphrag.index.progress import PrintProgressReporter
from graphrag.index.progress.types import ProgressReporter

# 导入CompletionLLM类，可能与完成语言模型相关
from graphrag.llm.types.llm_types import CompletionLLM

# 导入prompt_tune模块的各种生成器函数，用于创建提示
from graphrag.prompt_tune.generator import (
    MAX_TOKEN_COUNT,  # 定义最大令牌数
    create_community_summarization_prompt,  # 创建社区总结提示
    create_entity_extraction_prompt,  # 创建实体提取提示
    create_entity_summarization_prompt,  # 创建实体总结提示
    detect_language,  # 检测文本语言
    generate_community_report_rating,  # 生成社区报告评分
    generate_community_reporter_role,  # 生成社区报告者角色
    generate_domain,  # 生成领域信息
    generate_entity_relationship_examples,  # 生成实体关系示例
    generate_entity_types,  # 生成实体类型
    generate_persona,  # 生成人物描述
)

# 导入prompt_tune模块的加载器函数，用于加载文档和读取配置参数
from graphrag.prompt_tune.loader import (
    MIN_CHUNK_SIZE,  # 定义最小块大小
    load_docs_in_chunks,  # 分块加载文档
    read_config_parameters,  # 读取配置参数
)

# 这是代码的版权信息，表示2024年微软公司的作品
# 并遵循MIT许可证
# 注释中的三引号表示这是一个多行字符串，通常用于文档说明
# 在这里，它定义了这个模块的命令行界面

# 定义一个异步函数（可以同时执行多个任务），叫做 fine_tune
async def fine_tune(
    # 根目录，存放数据的地方
    root: str,
    # 领域，比如科学、艺术等，用来分类输入文档
    domain: str,
    # 选择方法，默认是"random"，决定如何选取数据块
    select: str = "random",
    # 限制加载的数据块数量，默认15个
    limit: int = 15,
    # 提取实体时最大使用的词汇数，不能超过MAX_TOKEN_COUNT这个常量
    max_tokens: int = MAX_TOKEN_COUNT,
    # 数据块的单词大小，默认是最小值MIN_CHUNK_SIZE
    chunk_size: int = MIN_CHUNK_SIZE,
    # 语言选项，如果不需要可以留空
    language: str | None = None,
    # 是否跳过生成实体类型，默认是False，即不跳过
    skip_entity_types: bool = False,
    # 输出文件夹，保存生成的提示信息
    output: str = "prompts",
):
    # 创建一个进度报告器，用于显示操作进度
    reporter = PrintProgressReporter("")
    
    # 读取根目录下的配置参数，并使用报告器来显示进度
    config = read_config_parameters(root, reporter)

    # 使用配置参数进行微调（模型学习），并传入所有前面的参数和报告器
    # 这个函数也是异步的，会在后台运行
    await fine_tune_with_config(
        root,
        config,
        domain,
        select,
        limit,
        max_tokens,
        chunk_size,
        language,
        skip_entity_types,
        output,
        reporter,
    )

# 定义一个异步函数，用于用配置微调模型
async def fine_tune_with_config(
    # 根目录，存储所有文件的地方
    root: str,
    # GraphRag的配置对象，包含微调的详细设置
    config: GraphRagConfig,
    # 输入文档要映射到的领域
    domain: str,
    # 选择文档块的方法，可以是"random"或其他方式
    select: str = "random",
    # 加载的文档块的最大数量
    limit: int = 15,
    # 提取实体时使用的最大令牌数
    max_tokens: int = MAX_TOKEN_COUNT,
    # 输入文本单元的块大小
    chunk_size: int = MIN_CHUNK_SIZE,
    # 可选的语言，如果不设置则为None
    language: str | None = None,
    # 是否跳过生成实体类型
    skip_entity_types: bool = False,
    # 存储提示的输出文件夹
    output: str = "prompts",
    # 进度报告器，如果没有会创建一个
    reporter: ProgressReporter | None = None,
):

    # 如果没有提供进度报告器，就创建一个打印进度的报告器
    if not reporter:
        reporter = PrintProgressReporter("")

    # 计算输出路径，位于配置的根目录下
    output_path = Path(config.root_dir) / output

    # 异步加载文档块
    doc_list = await load_docs_in_chunks(
        # 根目录
        root=root,
        # 配置
        config=config,
        # 加载限制
        limit=limit,
        # 选择方法
        select_method=select,
        # 进度报告器
        reporter=reporter,
        # 块大小
        chunk_size=chunk_size,
    )

    # 根据配置创建语言模型
    llm = load_llm(
        # 模型用途
        "fine_tuning",
        # 语言模型类型
        config.llm.type,
        # 不执行任何操作的动词回调
        NoopVerbCallbacks(),
        # 没有特定的模型实例
        None,
        # 使用配置中的模型文件
        config.llm.model_dump(),
    )

    # 生成索引提示
    await generate_indexing_prompts(
        # 语言模型
        llm,
        # 配置
        config,
        # 文档列表
        doc_list,
        # 输出路径
        output_path,
        # 进度报告器
        reporter,
        # 领域
        domain,
        # 语言
        language,
        # 最大令牌数
        max_tokens,
        # 是否跳过生成实体类型
        skip_entity_types,
    )

# 定义一个异步函数，用于生成索引提示
async def generate_indexing_prompts(
    # 使用的LLM模型
    llm: CompletionLLM,
    # 图形RAG配置
    config: GraphRagConfig,
    # 要使用的文档列表
    doc_list: list[str],
    # 存储提示的路径
    output_path: Path,
    # 进度报告器
    reporter: ProgressReporter,
    # 可选的领域
    domain: str | None = None,
    # 可选的语言
    language: str | None = None,
    # 提示中最大令牌数
    max_tokens: int = MAX_TOKEN_COUNT,
    # 是否跳过实体类型生成
    skip_entity_types: bool = False,
):
    """
    生成索引提示。

    参数:
    - llm: 使用的LLM模型。
    - config: 图形RAG配置。
    - doc_list: 使用的文档列表。
    - output_path: 存储提示的文件夹。
    - reporter: 报告进度的对象。
    - domain: 文档所属的领域，可选。
    - max_tokens: 提示中的最大单词数，可选。
    - skip_entity_types: 是否跳过生成实体类型，可选。
    """

    # 如果没有指定领域，就去生成领域
    if not domain:
        reporter.info("正在生成领域...")
        domain = await generate_domain(llm, doc_list)
        reporter.info(f"生成的领域: {domain}")

    # 如果没有指定语言，就去检测语言
    if not language:
        reporter.info("正在检测语言...")
        language = await detect_language(llm, doc_list)
        reporter.info(f"检测到的语言: {language}")

    # 生成个性
    reporter.info("正在生成个性...")
    persona = await generate_persona(llm, domain)
    reporter.info(f"生成的个性: {persona}")

    # 生成社区报告排名描述
    reporter.info("正在生成社区报告排名描述...")
    community_report_ranking = await generate_community_report_rating(
        llm, domain=domain, persona=persona, docs=doc_list
    )
    reporter.info(
        f"生成的社区报告排名描述: {community_report_ranking}"
    )

    # 如果没有跳过实体类型，就去生成实体类型
    entity_types = None
    if not skip_entity_types:
        reporter.info("正在生成实体类型...")
        entity_types = await generate_entity_types(
            llm,
            domain=domain,
            persona=persona,
            docs=doc_list,
            json_mode=config.llm.model_supports_json or False,
        )
        reporter.info(f"生成的实体类型: {entity_types}")

    # 生成实体关系示例
    reporter.info("正在生成实体关系示例...")
    examples = await generate_entity_relationship_examples(
        llm,
        persona=persona,
        entity_types=entity_types,
        docs=doc_list,
        language=language,
        json_mode=False,  # 应该根据config.llm.model_supports_json使用，但这里提示被索引引擎非json方式使用
    )
    reporter.info("完成生成实体关系示例")

    # 生成实体提取提示
    reporter.info("正在生成实体提取提示...")
    create_entity_extraction_prompt(
        entity_types=entity_types,
        docs=doc_list,
        examples=examples,
        language=language,
        json_mode=False,  # 应该根据config.llm.model_supports_json使用，但这里提示被索引引擎非json方式使用
        output_path=output_path,
        encoding_model=config.encoding_model,
        max_token_count=max_tokens,
    )
    reporter.info(f"生成的实体提取提示已存储在文件夹 {output_path}")

    # 生成实体摘要提示
    reporter.info("正在生成实体摘要提示...")
    create_entity_summarization_prompt(
        persona=persona,
        language=language,
        output_path=output_path,
    )
    reporter.info(
        f"生成的实体摘要提示已存储在文件夹 {output_path}"
    )

    # 生成社区报告者角色
    reporter.info("正在生成社区报告者角色...")
    community_reporter_role = await generate_community_reporter_role(
        llm, domain=domain, persona=persona, docs=doc_list
    )
    reporter.info(f"生成的社区报告者角色: {community_reporter_role}")

    # 生成社区摘要提示
    reporter.info("正在生成社区摘要提示...")
    create_community_summarization_prompt(
        persona=persona,
        role=community_reporter_role,
        report_rating_description=community_report_ranking,
        language=language,
        output_path=output_path,
    )
    reporter.info(
        f"生成的社区摘要提示已存储在文件夹 {output_path}"
    )

