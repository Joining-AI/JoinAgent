# 导入必要的库，这些库帮助我们执行不同的任务
import asyncio       # 异步编程工具
import json          # 处理JSON数据
import logging       # 记录程序运行时的信息
import platform      # 获取操作系统信息
import sys           # 系统相关功能
import time          # 时间和日期操作
import warnings      # 发出警告信息
from pathlib import Path  # 处理文件路径

# 从graphrag库中导入特定模块和函数
from graphrag.config import create_graphrag_config
from graphrag.index import PipelineConfig, create_pipeline_config
from graphrag.index.cache import NoopPipelineCache
from graphrag.index.progress import (
    NullProgressReporter,  # 不显示进度报告
    PrintProgressReporter,  # 打印进度报告
    ProgressReporter,       # 进度报告基类
    RichProgressReporter,   # 丰富格式的进度报告
)
from graphrag.index.run import run_pipeline_with_config

# 导入自定义模块和类型
from .emit import TableEmitterType  # 输出表格类型
from .graph.extractors.claims.prompts import CLAIM_EXTRACTION_PROMPT
from .graph.extractors.community_reports.prompts import COMMUNITY_REPORT_PROMPT
from .graph.extractors.graph.prompts import GRAPH_EXTRACTION_PROMPT
from .graph.extractors.summarize.prompts import SUMMARIZE_PROMPT
from .init_content import INIT_DOTENV, INIT_YAML  # 初始化文件内容

# 不显示numba库的警告信息
warnings.filterwarnings("ignore", message=".*NumbaDeprecationWarning.*")

# 设置日志记录器，用于记录程序运行中的信息
log = logging.getLogger(__name__)

# 定义一个名为redact的函数，它接收一个字典作为输入，并返回一个字符串
def redact(input: dict) -> str:
    """这个函数用来清理配置的json，隐藏敏感信息"""

    # 定义一个内部函数redact_dict，它也接收一个字典作为输入，并返回一个处理后的字典
    def redact_dict(input: dict) -> dict:
        # 如果输入不是字典类型，就直接返回原样
        if not isinstance(input, dict):
            return input

        # 创建一个新的空字典result，用于存储处理后的数据
        result = {}

        # 遍历输入字典中的所有键值对
        for key, value in input.items():
            # 检查键是否包含敏感信息（如：api_key, connection_string等）
            if key in {
                "api_key",
                "connection_string",
                "container_name",
                "organization",
            }:
                # 如果值不为空，用"REDACTED, length N"替换，N是原始值的长度
                if value is not None:
                    result[key] = f"REDACTED, length {len(value)}"
            # 如果值是字典类型，递归调用redact_dict进行处理
            elif isinstance(value, dict):
                result[key] = redact_dict(value)
            # 如果值是列表类型，遍历列表并用redact_dict处理每个元素
            elif isinstance(value, list):
                result[key] = [redact_dict(i) for i in value]
            # 如果都不是以上情况，直接将原值存入新字典
            else:
                result[key] = value

        # 返回处理后的字典
        return result

    # 使用redact_dict函数处理输入的字典，并将结果存储在redacted_dict中
    redacted_dict = redact_dict(input)

    # 将处理后的字典转换成格式化的json字符串，缩进4个空格
    return json.dumps(redacted_dict, indent=4)

# 定义一个函数叫做 index_cli，它接收多个参数
def index_cli(
    # 根目录，存放项目文件的地方
    root: str,
    # 如果是 true，初始化项目
    init: bool,
    # 如果是 true，显示更多运行信息
    verbose: bool,
    # 如果有值，恢复之前中断的运行
    resume: str | None,
    # 如果是 true，记录内存使用情况
    memprofile: bool,
    # 如果是 true，不使用缓存
    nocache: bool,
    # 报告进度的方式，可以是文本、图形等
    reporter: str | None,
    # 配置文件路径，如果有的话
    config: str | None,
    # 输出类型，比如表格，多个用逗号分隔
    emit: str | None,
    # 如果是 true，只预览不执行
    dryrun: bool,
    # 如果是 true，使用默认配置覆盖已有配置
    overlay_defaults: bool,
    # 如果是 true，表明从命令行运行
    cli: bool = False,
):
    """这个函数用来运行一个管道流程，根据给定的配置"""
    
    # 如果有恢复运行的 ID 就用它，没有就用当前时间创建一个
    run_id = resume or time.strftime("%Y%m%d-%H%M%S")
    
    # 设置日志系统，根据 verbose 参数决定是否显示更多信息
    _enable_logging(root, run_id, verbose)
    
    # 获取进度报告器，根据 reporter 参数选择报告方式
    progress_reporter = _get_progress_reporter(reporter)
    
    # 如果 init 为 true，初始化项目并退出
    if init:
        _initialize_project_at(root, progress_reporter)
        sys.exit(0)
    
    # 如果 overlay_defaults 为 true，创建默认配置
    # 否则，如果没有用户提供的配置文件，则使用默认配置
    if overlay_defaults:
        pipeline_config = _create_default_config(
            root, config, verbose, dryrun or False, progress_reporter
        )
    else:
        pipeline_config = config or _create_default_config(
            root, None, verbose, dryrun or False, progress_reporter
        )
    
    # 如果 nocache 为 true，使用空操作缓存，否则不设置缓存
    cache = NoopPipelineCache() if nocache else None
    
    # 分割 emit 参数，得到输出类型列表
    pipeline_emit = emit.split(",") if emit else None
    
    # 初始化错误标志
    encountered_errors = False

    # 定义一个异步运行工作流的函数
    def _run_workflow_async() -> None:
        # 引入信号处理模块
        import signal

        # 当收到特定信号时，执行的处理函数
        def handle_signal(signum, _):
            # 显示接收到的信号并退出
            progress_reporter.info(f"Received signal {signum}, exiting...")
            progress_reporter.dispose()
            # 取消所有任务
            for task in asyncio.all_tasks():
                task.cancel()
            progress_reporter.info("All tasks cancelled. Exiting...")

        # 注册信号处理器，处理 SIGINT（键盘中断）和 SIGHUP（挂起）
        signal.signal(signal.SIGINT, handle_signal)

        # 如果不是 Windows 系统，也处理 SIGHUP
        if sys.platform != "win32":
            signal.signal(signal.SIGHUP, handle_signal)

        # 定义执行工作流的异步函数
        async def execute():
            nonlocal encountered_errors
            # 运行管道流程，根据给定的参数
            async for output in run_pipeline_with_config(
                pipeline_config,
                run_id=run_id,
                memory_profile=memprofile,
                cache=cache,
                progress_reporter=progress_reporter,
                emit=(TableEmitterType(e) for e in pipeline_emit) if pipeline_emit else None,
                is_resume_run=bool(resume),
            ):
                # 如果有错误，标记错误并报告
                if output.errors and len(output.errors) > 0:
                    encountered_errors = True
                    progress_reporter.error(output.workflow)
                # 没有错误，报告成功
                else:
                    progress_reporter.success(output.workflow)

                # 显示结果信息
                progress_reporter.info(str(output.result))

        # 根据操作系统选择合适的异步运行方式
        if platform.system() == "Windows":
            # 在 Windows 上处理异步问题
            import nest_asyncio

            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(execute())
        elif sys.version_info >= (3, 11):
            # Python 3.11 及以上版本，使用 uvloop 提高性能
            import uvloop

            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(execute())
        else:
            # 其他版本，先安装 uvloop 再运行
            import uvloop

            uvloop.install()
            asyncio.run(execute())

    # 调用异步工作流函数开始执行
    _run_workflow_async()

    # 停止进度报告器
    progress_reporter.stop()

    # 如果有错误，报告并退出
    if encountered_errors:
        progress_reporter.error(
            "Errors occurred during the pipeline run, see logs for more details."
        )
    else:
        # 没有错误，报告成功
        progress_reporter.success("All workflows completed successfully.")

    # 如果从命令行运行，根据是否有错误决定退出状态码
    if cli:
        sys.exit(1 if encountered_errors else 0)

# 定义一个函数，叫做 "_initialize_project_at"，它接受两个参数：一个路径（字符串类型）和一个进度报告器（ProgressReporter 类型）
def _initialize_project_at(path: str, reporter: ProgressReporter) -> None:
    # 这个函数的作用是初始化在给定路径下的项目
    reporter.info(f"初始化项目在 {path} 位置")

    # 把路径转换成一个 Path 对象，方便后续操作
    root = Path(path)

    # 检查路径是否存在，如果不存在就创建它，包括它的所有父目录，如果已经存在也不会报错
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)

    # 检查是否存在名为 "settings.yaml" 的文件
    settings_yaml = root / "settings.yaml"
    if settings_yaml.exists():
        # 如果文件存在，说明项目已经初始化过了，抛出一个错误信息
        msg = f"项目已在 {root} 处初始化"
        raise ValueError(msg)

    # 检查是否存在名为 ".env" 的文件
    dotenv = root / ".env"
    if not dotenv.exists():
        # 如果文件不存在，就写入一些初始内容
        with settings_yaml.open("w") as file:
            file.write(INIT_YAML)  # 这里假设 INIT_YAML 是一个预定义的字符串

    # 再次打开 ".env" 文件，写入另一些初始内容
    with dotenv.open("w") as file:
        file.write(INIT_DOTENV)  # 这里假设 INIT_DOTENV 也是一个预定义的字符串

    # 创建一个名为 "prompts" 的目录，如果不存在的话
    prompts_dir = root / "prompts"
    if not prompts_dir.exists():
        prompts_dir.mkdir(parents=True, exist_ok=True)

    # 在 "prompts" 目录下创建一个名为 "entity_extraction.txt" 的文件，如果不存在的话
    entity_extraction = prompts_dir / "entity_extraction.txt"
    if not entity_extraction.exists():
        with entity_extraction.open("w") as file:
            file.write(GRAPH_EXTRACTION_PROMPT)  # 假设 GRAPH_EXTRACTION_PROMPT 是一个预定义的文本

    # 创建一个名为 "summarize_descriptions.txt" 的文件，如果不存在的话
    summarize_descriptions = prompts_dir / "summarize_descriptions.txt"
    if not summarize_descriptions.exists():
        with summarize_descriptions.open("w") as file:
            file.write(SUMMARIZE_PROMPT)  # 假设 SUMMARIZE_PROMPT 是一个预定义的文本

    # 创建一个名为 "claim_extraction.txt" 的文件，如果不存在的话
    claim_extraction = prompts_dir / "claim_extraction.txt"
    if not claim_extraction.exists():
        with claim_extraction.open("w") as file:
            file.write(CLAIM_EXTRACTION_PROMPT)  # 假设 CLAIM_EXTRACTION_PROMPT 是一个预定义的文本

    # 创建一个名为 "community_report.txt" 的文件，如果不存在的话
    community_report = prompts_dir / "community_report.txt"
    if not community_report.exists():
        with community_report.open("w") as file:
            file.write(COMMUNITY_REPORT_PROMPT)  # 假设 COMMUNITY_REPORT_PROMPT 是一个预定义的文本

# 定义一个函数_create_default_config，它接受5个参数：
# root：一个字符串，表示根目录的位置
# config：可以是字符串或None，表示配置文件的路径
# verbose：一个布尔值，如果为True，会显示详细信息
# dryrun：一个布尔值，如果为True，只会模拟运行，不会真正执行
# reporter：一个ProgressReporter对象，用来报告进度和信息

def _create_default_config(
    root: str,
    config: str | None,
    verbose: bool,
    dryrun: bool,
    reporter: ProgressReporter,
) -> PipelineConfig:

    # 如果配置文件路径存在并且提供的配置文件不存在
    if config and not Path(config).exists():
        # 提示错误信息并抛出ValueError异常
        msg = f"Configuration file {config} does not exist"
        raise ValueError(msg)

    # 如果根目录不存在
    if not Path(root).exists():
        # 提示错误信息并抛出ValueError异常
        msg = f"Root directory {root} does not exist"
        raise ValueError(msg)

    # 从根目录和配置文件中读取参数，使用reporter报告进度
    parameters = _read_config_parameters(root, config, reporter)

    # 使用日志记录器显示使用默认配置的信息（部分敏感信息会被隐藏）
    log.info(
        "using default configuration: %s",
        redact(parameters.model_dump()),
    )

    # 如果verbose或dryrun为真，使用reporter显示使用默认配置的信息（部分敏感信息会被隐藏）
    if verbose or dryrun:
        reporter.info(f"Using default configuration: {redact(parameters.model_dump())}")

    # 根据参数创建PipelineConfig对象
    result = create_pipeline_config(parameters, verbose)

    # 如果verbose或dryrun为真，使用reporter显示最终配置信息（部分敏感信息会被隐藏）
    if verbose or dryrun:
        reporter.info(f"Final Config: {redact(result.model_dump())}")

    # 如果是dryrun模式，报告模拟运行完成，然后退出程序
    if dryrun:
        reporter.info("dry run complete, exiting...")
        sys.exit(0)

    # 最后，如果没有在dryrun模式下，返回创建的PipelineConfig对象
    return result

# 定义一个函数，用于读取配置参数
def _read_config_parameters(root: str, config: str | None, reporter: ProgressReporter):
    # 将根目录字符串转换为Path对象
    _root = Path(root)
    
    # 如果config存在并且后缀是.yaml或.yml，设置settings_yaml为该路径
    # 否则，设置为根目录下的"settings.yaml"
    settings_yaml = (
        Path(config)
        if config and Path(config).suffix in [".yaml", ".yml"]
        else _root / "settings.yaml"
    )
    
    # 如果settings_yaml不存在，尝试设置为根目录下的"settings.yml"
    if not settings_yaml.exists():
        settings_yaml = _root / "settings.yml"

    # 如果config存在并且后缀是.json，设置settings_json为该路径
    # 否则，设置为根目录下的"settings.json"
    settings_json = (
        Path(config)
        if config and Path(config).suffix == ".json"
        else _root / "settings.json"
    )

    # 如果settings_yaml文件存在
    if settings_yaml.exists():
        # 通过reporter报告成功消息，显示正在从哪个文件读取设置
        reporter.success(f"Reading settings from {settings_yaml}")
        # 打开settings_yaml文件并以只读模式读取
        with settings_yaml.open("r") as file:
            # 导入yaml库
            import yaml
            # 安全地加载yaml文件内容到data
            data = yaml.safe_load(file)
            # 使用data和root创建graphrag配置并返回
            return create_graphrag_config(data, root)

    # 如果settings_json文件存在
    if settings_json.exists():
        # 通过reporter报告成功消息，显示正在从哪个文件读取设置
        reporter.success(f"Reading settings from {settings_json}")
        # 打开settings_json文件并以只读模式读取
        with settings_json.open("r") as file:
            # 导入json库
            import json
            # 解析json文件内容到data
            data = json.loads(file.read())
            # 使用data和root创建graphrag配置并返回
            return create_graphrag_config(data, root)

    # 如果没有找到文件，从环境变量中读取设置
    reporter.success("Reading settings from environment variables")
    # 使用root_dir=root创建graphrag配置并返回
    return create_graphrag_config(root_dir=root)

# 定义一个函数，根据参数返回不同类型的进度报告器
def _get_progress_reporter(reporter_type: str | None) -> ProgressReporter:
    # 如果reporter_type为空或等于"rich"，返回RichProgressReporter
    if reporter_type is None or reporter_type == "rich":
        return RichProgressReporter("GraphRAG Indexer ")
    # 如果reporter_type等于"print"，返回PrintProgressReporter
    elif reporter_type == "print":
        return PrintProgressReporter("GraphRAG Indexer ")
    # 如果reporter_type等于"none"，返回NullProgressReporter
    elif reporter_type == "none":
        return NullProgressReporter()

    # 如果reporter_type无效，抛出ValueError并给出错误信息
    msg = f"Invalid progress reporter type: {reporter_type}"
    raise ValueError(msg)

# 定义一个函数，叫做_enable_logging，它需要三个参数：root_dir（根目录），run_id（运行ID）和verbose（是否详细输出）
def _enable_logging(root_dir: str, run_id: str, verbose: bool) -> None:

    # 创建一个变量logging_file，表示日志文件的路径
    logging_file = (
        Path(root_dir) / "output" / run_id / "reports" / "indexing-engine.log"
    )

    # 确保日志文件的上级目录存在，如果不存在就创建，如果已经存在则没问题
    logging_file.parent.mkdir(parents=True, exist_ok=True)

    # 如果日志文件不存在，就创建一个空文件
    logging_file.touch(exist_ok=True)

    # 设置日志的基本配置
    # 指定日志写入到logging_file这个文件中
    logging.basicConfig(
        # 文件名用字符串形式表示
        filename=str(logging_file),
        # 文件模式为追加（不会覆盖已有内容）
        filemode="a",
        # 日志格式，包括时间、毫秒、模块名、级别和信息
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        # 时间格式为小时:分钟:秒
        datefmt="%H:%M:%S",
        # 如果verbose为True，日志级别设为DEBUG，否则设为INFO
        level=logging.DEBUG if verbose else logging.INFO,
    )

