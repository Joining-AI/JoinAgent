# 导入垃圾回收模块，用于清理不再使用的内存
import gc

# 导入json模块，用于处理JSON格式的数据
import json

# 导入日志模块，用于记录程序运行时的信息
import logging

# 导入时间模块，获取或操作时间
import time

# 导入追踪堆栈信息的traceback模块，用于错误处理
import traceback

# 从collections.abc模块导入AsyncIterable接口，表示异步可迭代对象
from collections.abc import AsyncIterable

# 从dataclasses模块导入asdict函数，将数据类转换为字典
from dataclasses import asdict

# 从io模块导入BytesIO类，用于处理二进制数据流
from io import BytesIO

# 从pathlib模块导入Path类，用于处理文件路径
from pathlib import Path

# 从string模块导入Template类，用于创建和操作字符串模板
from string import Template

# 从typing模块导入cast函数，用于类型转换
from typing import cast

# 导入pandas库，用于数据处理
import pandas as pd

# 从datashaper库导入多个类和常量
from datashaper import (
    DEFAULT_INPUT_NAME,
    MemoryProfile,
    Workflow,
    WorkflowCallbacks,
    WorkflowCallbacksManager,
    WorkflowRunResult,
)

# 从当前模块的.cache子模块导入缓存相关类
from .cache import InMemoryCache, PipelineCache, load_cache

# 从当前模块的.config子模块导入配置相关类
from .config import (
    # 多个配置类的定义，这里省略了详细解释
)

# 从当前模块的.context子模块导入运行上下文和统计信息类
from .context import PipelineRunContext, PipelineRunStats

# 从当前模块的.emit子模块导入表发射器类型和创建发射器的函数
from .emit import TableEmitterType, create_table_emitters

# 从当前模块的.input子模块导入加载输入数据的函数
from .input import load_input

# 从当前模块的.load_pipeline_config子模块导入加载管道配置的函数
from .load_pipeline_config import load_pipeline_config

# 从当前模块的.progress子模块导入进度报告器类和空进度报告器
from .progress import NullProgressReporter, ProgressReporter

# 从当前模块的.reporting子模块导入报告相关的类和函数
from .reporting import (
    ConsoleWorkflowCallbacks,
    ProgressWorkflowCallbacks,
    load_pipeline_reporter,
)

# 从当前模块的.storage子模块导入存储相关类和加载存储的函数
from .storage import MemoryPipelineStorage, PipelineStorage, load_storage

# 再次从当前模块导入PipelineRunResult类，确保其在当前命名空间可用
from .typing import PipelineRunResult

# 从当前模块的.verbs子模块导入所有动词（操作）定义，以便使用
from .verbs import *  # noqa

# 从当前模块的.workflows子模块导入工作流定义相关的类和函数
from .workflows import (
    VerbDefinitions,
    WorkflowDefinitions,
    create_workflow,
    load_workflows,
)

# 这段代码是微软公司的一个项目，用于管理数据处理流程
# 它使用了MIT许可证

# 注释：定义这个模块中所有代码的版权归属和许可证信息
# Copyright (c) 2024 Microsoft Corporation. # 版权归微软公司所有
# Licensed under the MIT License # 使用MIT许可证

# 这个模块包含了运行数据管道的不同方法
"""Different methods to run the pipeline."""

# 导入所需的各种Python库
import gc # 用于垃圾回收
import json # 处理JSON格式的数据
import logging # 记录日志信息
import time # 处理时间
import traceback # 错误追踪
from collections.abc import AsyncIterable # 异步可迭代对象的抽象基类
from dataclasses import asdict # 将数据类转换为字典
from io import BytesIO # 二进制数据流
from pathlib import Path # 路径操作
from string import Template # 字符串模板
from typing import cast # 类型转换

# 数据处理相关的库
import pandas as pd # 数据分析库
from datashaper import (
    DEFAULT_INPUT_NAME, # 默认输入名称
    MemoryProfile, # 内存使用概况
    Workflow, # 工作流类
    WorkflowCallbacks, # 工作流回调接口
    WorkflowCallbacksManager, # 工作流回调管理器
    WorkflowRunResult, # 工作流运行结果
)

# 项目自定义的库
from .cache import InMemoryCache, PipelineCache, load_cache # 缓存管理
from .config import ( # 配置类
    # 省略了多个配置类的导入，它们定义了各种配置选项
)
from .context import PipelineRunContext, PipelineRunStats # 运行上下文和统计信息
from .emit import TableEmitterType, create_table_emitters # 输出表的类型和创建方法
from .input import load_input # 加载输入数据
from .load_pipeline_config import load_pipeline_config # 加载管道配置
from .progress import NullProgressReporter, ProgressReporter # 进度报告器
from .reporting import ( # 报告相关
    ConsoleWorkflowCallbacks, # 控制台回调
    ProgressWorkflowCallbacks, # 进度回调
    load_pipeline_reporter, # 加载报告器
)
from .storage import MemoryPipelineStorage, PipelineStorage, load_storage # 存储管理
from .typing import PipelineRunResult # 运行结果的类型定义

# 注册所有的操作（verbs）
from .verbs import *  # noqa
from .workflows import ( # 工作流定义
    VerbDefinitions, # 操作定义
    WorkflowDefinitions, # 工作流定义
    create_workflow, # 创建工作流
    load_workflows, # 加载工作流
)

# 设置日志记录器
log = logging.getLogger(__name__) # 获取当前模块的日志记录器

# 定义一个异步函数run_pipeline_with_config，它接受很多参数，用于运行数据管道
async def run_pipeline_with_config(
    # 参数1：可以是配置对象或配置文件路径
    config_or_path: PipelineConfig | str,
    # 参数2：可选的工作流程列表，可以覆盖配置中的工作流程
    workflows: list[PipelineWorkflowReference] | None = None,
    # 参数3：可选的数据集，如果提供则覆盖配置中的数据集
    dataset: pd.DataFrame | None = None,
    # 参数4：可选的存储方式，可以覆盖配置中的存储设置
    storage: PipelineStorage | None = None,
    # 参数5：可选的缓存，可以覆盖配置中的缓存设置
    cache: PipelineCache | None = None,
    # 参数6：可选的回调函数，用于报告进度，覆盖配置中的报告器
    callbacks: WorkflowCallbacks | None = None,
    # 参数7：可选的进度报告器，如果没有提供，则使用默认的无操作报告器
    progress_reporter: ProgressReporter | None = None,
    # 参数8：输入数据后处理步骤，可选，覆盖配置中的步骤
    input_post_process_steps: list[PipelineWorkflowStep] | None = None,
    # 参数9：额外的动词定义，用于自定义管道
    additional_verbs: VerbDefinitions | None = None,
    # 参数10：额外的工作流程定义，用于扩展管道
    additional_workflows: WorkflowDefinitions | None = None,
    # 参数11：表格发射器列表，用于输出结果
    emit: list[TableEmitterType] | None = None,
    # 参数12：是否开启内存分析，默认为False
    memory_profile: bool = False,
    # 参数13：运行ID，用于开始或恢复运行，如果没有提供，将使用当前时间生成
    run_id: str | None = None,
    # 参数14：是否恢复已中断的运行，默认为False
    is_resume_run: bool = False,
    **_kwargs: dict,  # 其他未命名的参数，这里不用
) -> AsyncIterable[PipelineRunResult]:
    """使用给定的配置运行管道。

    参数：
        - config_or_path - 运行管道的配置或配置文件路径
        - workflows - 要运行的工作流程（覆盖配置）
        - dataset - 运行管道的数据集（覆盖配置）
        - storage - 管道使用的存储（覆盖配置）
        - cache - 管道使用的缓存（覆盖配置）
        - reporter - 管道的进度报告器（覆盖配置）
        - input_post_process_steps - 输入数据的后处理步骤（覆盖配置）
        - additional_verbs - 管道的自定义动词
        - additional_workflows - 管道的自定义工作流程
        - emit - 管道的表格发射器
        - memory_profile - 是否进行内存分析
        - run_id - 开始或恢复运行的ID
    """

    # 如果config_or_path是字符串，表示是配置文件路径
    if isinstance(config_or_path, str):
        # 打印信息，表明将使用配置文件运行管道
        log.info("Running pipeline with config %s", config_or_path)
    else:
        # 否则，直接使用配置对象运行
        log.info("Running pipeline")

    # 如果没有提供run_id，用当前时间生成一个
    run_id = run_id or time.strftime("%Y%m%d-%H%M%S")
    # 加载配置
    config = load_pipeline_config(config_or_path)
    # 应用替换到配置中，可能与run_id有关
    config = _apply_substitutions(config, run_id)
    # 获取配置的根目录
    root_dir = config.root_dir

    # 函数：根据配置创建存储
    def _create_storage(config: PipelineStorageConfigTypes | None) -> PipelineStorage:
        return load_storage(
            config
            or PipelineFileStorageConfig(base_dir=str(Path(root_dir or "") / "output"))
        )

    # 函数：根据配置创建缓存
    def _create_cache(config: PipelineCacheConfigTypes | None) -> PipelineCache:
        return load_cache(config or PipelineMemoryCacheConfig(), root_dir=root_dir)

    # 函数：根据配置创建报告器
    def _create_reporter(
        config: PipelineReportingConfigTypes | None,
    ) -> WorkflowCallbacks | None:
        return load_pipeline_reporter(config, root_dir) if config else None

    # 异步函数：根据配置创建输入数据
    async def _create_input(
        config: PipelineInputConfigTypes | None,
    ) -> pd.DataFrame | None:
        if config is None:
            return None

        return await load_input(config, progress_reporter, root_dir)

    # 函数：根据配置创建输入数据后处理步骤
    def _create_postprocess_steps(
        config: PipelineInputConfigTypes | None,
    ) -> list[PipelineWorkflowStep] | None:
        return config.post_process if config is not None else None

    # 如果没有提供进度报告器，使用默认的无操作报告器
    progress_reporter = progress_reporter or NullProgressReporter()
    # 如果没有提供存储，根据配置创建
    storage = storage or _create_storage(config.storage)
    # 如果没有提供缓存，根据配置创建
    cache = cache or _create_cache(config.cache)
    # 如果没有提供回调，根据配置创建报告器
    callbacks = callbacks or _create_reporter(config.reporting)
    # 如果没有提供数据集，根据配置创建
    dataset = dataset if dataset is not None else await _create_input(config.input)
    # 如果没有提供后处理步骤，根据配置创建
    post_process_steps = input_post_process_steps or _create_postprocess_steps(
        config.input
    )
    # 如果没有提供工作流程，使用配置中的工作流程
    workflows = workflows or config.workflows

    # 如果没有提供数据集，抛出错误
    if dataset is None:
        raise ValueError("No dataset provided!")

    # 运行管道，使用提供的参数，获取表格结果
    async for table in run_pipeline(
        workflows=workflows,
        dataset=dataset,
        storage=storage,
        cache=cache,
        callbacks=callbacks,
        input_post_process_steps=post_process_steps,
        memory_profile=memory_profile,
        additional_verbs=additional_verbs,
        additional_workflows=additional_workflows,
        progress_reporter=progress_reporter,
        emit=emit,
        is_resume_run=is_resume_run,
    ):
        # 产生每个表格结果
        yield table



# 定义一个异步函数，用于运行管道
async def run_pipeline(
    # 工作流程列表
    workflows: list[PipelineWorkflowReference],
    # 数据集，是一个包含特定列（如id，text，title）的数据框
    dataset: pd.DataFrame,
    # 管道使用的存储，如果未指定则使用内存存储
    storage: PipelineStorage | None = None,
    # 管道使用的缓存，如果未指定则使用内存缓存
    cache: PipelineCache | None = None,
    # 工作流回调，用于报告进度，如果没有则使用控制台回调
    callbacks: WorkflowCallbacks | None = None,
    # 进度报告器，如果没有则使用无操作报告器
    progress_reporter: ProgressReporter | None = None,
    # 输入数据后处理步骤
    input_post_process_steps: list[PipelineWorkflowStep] | None = None,
    # 自定义动词定义
    additional_verbs: VerbDefinitions | None = None,
    # 自定义工作流定义
    additional_workflows: WorkflowDefinitions | None = None,
    # 输出类型，如果没有则默认为Parquet
    emit: list[TableEmitterType] | None = None,
    # 是否进行内存分析
    memory_profile: bool = False,
    # 是否恢复运行
    is_resume_run: bool = False,
    **_kwargs: dict,
) -> AsyncIterable[PipelineRunResult]:
    """运行管道。

    参数：
        - workflows - 要运行的工作流程
        - dataset - 运行管道的数据集，至少包含id，text和title列
        - storage - 管道使用的存储
        - cache - 管道使用的缓存
        - callbacks - 管道的回调
        - progress_reporter - 进度报告器
        - input_post_process_steps - 输入数据的后处理步骤
        - additional_verbs - 自定义动词
        - additional_workflows - 自定义工作流
        - debug - 是否启用调试模式
    返回：
        - output - 完成运行的工作流结果的可迭代对象，包括任何错误
    """

    # 记录开始时间
    start_time = time.time()
    # 初始化统计信息
    stats = PipelineRunStats()

    # 如果未指定，使用内存存储和缓存
    storage = storage or MemoryPipelineStorage()
    cache = cache or InMemoryCache()

    # 如果未指定，使用无操作报告器
    progress_reporter = progress_reporter or NullProgressReporter()
    # 如果未指定，使用控制台回调
    callbacks = callbacks or ConsoleWorkflowCallbacks()
    # 创建回调链
    callbacks = _create_callback_chain(callbacks, progress_reporter)

    # 如果未指定，输出类型为Parquet
    emit = emit or [TableEmitterType.Parquet]

    # 创建表格发射器
    emitters = create_table_emitters(
        emit,
        storage,
        # 错误处理回调
        lambda e, s, d: callbacks.on_error("Error emitting table", e, s, d),
    )

    # 加载工作流程
    loaded_workflows = load_workflows(
        workflows,
        additional_verbs=additional_verbs,
        additional_workflows=additional_workflows,
        memory_profile=memory_profile,
    )

    # 获取要运行的工作流程和依赖关系
    workflows_to_run = loaded_workflows.workflows
    workflow_dependencies = loaded_workflows.dependencies

    # 创建运行上下文
    context = _create_run_context(storage, cache, stats)

    # 检查是否有发射器，如果没有，警告用户
    if not emitters:
        log.info("没有提供发射器。不会生成表格输出。这可能是不正确的。")

    # 异步函数，保存统计信息到存储
    async def dump_stats() -> None:
        await storage.set("stats.json", json.dumps(asdict(stats), indent=4))

    # 异步函数，从存储中加载表格
    async def load_table_from_storage(name: str) -> pd.DataFrame:
        # 检查存储中是否存在该表格
        if not await storage.has(name):
            raise ValueError(f"找不到{name}在存储中!")
        try:
            log.info("从存储读取表格：%s", name)
            # 将表格从Parquet格式读入数据框
            return pd.read_parquet(BytesIO(await storage.get(name, as_bytes=True)))
        except Exception:
            log.error("从存储加载表格出错：%s", name, exc_info=True)
            raise

    # 异步函数，注入工作流的数据依赖
    async def inject_workflow_data_dependencies(workflow: Workflow) -> None:
        # 添加默认输入名称的表格
        workflow.add_table(DEFAULT_INPUT_NAME, dataset)
        # 处理工作流依赖
        deps = workflow_dependencies[workflow.name]
        log.info("工作流 %s 的依赖：%s", workflow.name, deps)
        for id in deps:
            workflow_id = f"workflow:{id}"
            # 加载依赖的表格数据
            table = await load_table_from_storage(f"{id}.parquet")
            workflow.add_table(workflow_id, table)

    # 异步函数，写入工作流统计信息
    async def write_workflow_stats(
        workflow: Workflow,
        workflow_result: WorkflowRunResult,
        workflow_start_time: float,
    ) -> None:
        # 更新统计信息
        for vt in workflow_result.verb_timings:
            stats.workflows[workflow.name][f"{vt.index}_{vt.verb}"] = vt.timing
        workflow_end_time = time.time()
        stats.workflows[workflow.name]["overall"] = workflow_end_time - workflow_start_time
        stats.total_runtime = time.time() - start_time
        await dump_stats()

        # 保存内存分析信息
        if workflow_result.memory_profile is not None:
            await _save_profiler_stats(
                storage, workflow.name, workflow_result.memory_profile
            )

        # 打印工作流输出的第一行
        log.debug(
            "工作流 %s 的第一行输出：%s",
            workflow.name,
            workflow.output().iloc[0].to_json(),
        )

    # 异步函数，发射工作流的输出
    async def emit_workflow_output(workflow: Workflow) -> pd.DataFrame:
        output = workflow.output()
        # 使用所有发射器发送工作流输出
        for emitter in emitters:
            await emitter.emit(workflow.name, output)
        return output

    # 运行输入数据的后处理步骤
    dataset = await _run_post_process_steps(
        input_post_process_steps, dataset, context, callbacks
    )

    # 验证数据集的正确性
    _validate_dataset(dataset)

    log.info("最终加载的行数：%s", len(dataset))
    stats.num_documents = len(dataset)
    last_workflow = "input"

    try:
        # 保存统计信息
        await dump_stats()

        # 遍历要运行的工作流程
        for workflow_to_run in workflows_to_run:
            # 试图清理中间数据框
            gc.collect()

            workflow = workflow_to_run.workflow
            workflow_name: str = workflow.name
            last_workflow = workflow_name

            log.info("运行工作流：%s...", workflow_name)

            # 如果恢复运行且工作流已经存在，跳过
            if is_resume_run and await storage.has(
                f"{workflow_to_run.workflow.name}.parquet"
            ):
                log.info("跳过 %s，因为它已存在", workflow_name)
                continue

            # 初始化工作流统计
            stats.workflows[workflow_name] = {"overall": 0.0}
            # 注入工作流数据依赖
            await inject_workflow_data_dependencies(workflow)

            workflow_start_time = time.time()
            # 运行工作流
            result = await workflow.run(context, callbacks)
            # 写入工作流统计信息
            await write_workflow_stats(workflow, result, workflow_start_time)

            # 发射工作流的输出
            output = await emit_workflow_output(workflow)
            # 生成工作流运行结果
            yield PipelineRunResult(workflow_name, output, None)
            output = None
            workflow.dispose()
            workflow = None

        # 更新总运行时间
        stats.total_runtime = time.time() - start_time
        await dump_stats()
    except Exception as e:
        # 记录并报告错误
        log.error("运行工作流 %s 出错", last_workflow, exc_info=True)
        callbacks.on_error("运行管道出错！", e, traceback.format_exc())
        # 生成带有错误的工作流运行结果
        yield PipelineRunResult(last_workflow, None, [e])

# 定义一个函数，用来创建回调管理器
def _create_callback_chain(
    callbacks: WorkflowCallbacks | None,  # 参数1：可能是WorkflowCallbacks类型的回调，也可能为空
    progress: ProgressReporter | None  # 参数2：可能是ProgressReporter类型的进度报告，也可能为空
) -> WorkflowCallbacks:  # 函数返回值：WorkflowCallbacks管理器

    # 创建一个WorkflowCallbacksManager实例
    manager = WorkflowCallbacksManager()

    # 如果传入的callbacks不为空，就用它注册到管理器里
    if callbacks is not None:
        manager.register(callbacks)

    # 如果传入的progress不为空，就创建一个ProgressWorkflowCallbacks并注册到管理器里
    if progress is not None:
        manager.register(ProgressWorkflowCallbacks(progress))

    # 返回管理器
    return manager

# 异步函数，用于将分析器的统计信息保存到存储中
async def _save_profiler_stats(
    storage: PipelineStorage,  # 参数1：PipelineStorage对象，用于存储数据
    workflow_name: str,  # 参数2：工作流的名字
    profile: MemoryProfile  # 参数3：内存分析的详细信息
):
    """将分析器的统计信息保存到存储中"""

    # 将峰值统计信息保存为csv文件
    await storage.set(
        f"{workflow_name}_profiling.peak_stats.csv",  # 文件名
        profile.peak_stats.to_csv(index=True),  # 内容：转换为csv格式的峰值统计
    )

    # 将快照统计信息保存为csv文件
    await storage.set(
        f"{workflow_name}_profiling.snapshot_stats.csv",  # 文件名
        profile.snapshot_stats.to_csv(index=True),  # 内容：转换为csv格式的快照统计
    )

    # 将时间统计信息保存为csv文件
    await storage.set(
        f"{workflow_name}_profiling.time_stats.csv",  # 文件名
        profile.time_stats.to_csv(index=True),  # 内容：转换为csv格式的时间统计
    )

    # 将详细视图信息保存为csv文件
    await storage.set(
        f"{workflow_name}_profiling.detailed_view.csv",  # 文件名
        profile.detailed_view.to_csv(index=True),  # 内容：转换为csv格式的详细视图
    )

# 异步函数，用于运行后处理步骤
async def _run_post_process_steps(
    post_process: list[PipelineWorkflowStep] | None,  # 参数1：后处理步骤列表，可能为空
    dataset: pd.DataFrame,  # 参数2：要处理的数据集
    context: PipelineRunContext,  # 参数3：管道运行上下文
    callbacks: WorkflowCallbacks,  # 参数4：回调函数
) -> pd.DataFrame:  # 返回值：处理后的数据集

    # 如果有后处理步骤并且不为空
    if post_process is not None and len(post_process) > 0:
        # 创建一个名为"Input Post Process"的工作流
        input_workflow = create_workflow(
            "Input Post Process",  # 工作流名字
            post_process,  # 后处理步骤列表
        )

        # 在工作流中添加一个表格，命名为DEFAULT_INPUT_NAME，内容为数据集
        input_workflow.add_table(DEFAULT_INPUT_NAME, dataset)

        # 运行工作流，使用上下文和回调函数
        await input_workflow.run(
            context=context,
            callbacks=callbacks,
        )

        # 获取工作流的输出结果，转换为pd.DataFrame类型
        dataset = cast(pd.DataFrame, input_workflow.output())

    # 返回处理后的数据集
    return dataset

# 定义一个函数，检查数据集是否有效
def _validate_dataset(dataset: pd.DataFrame):
    """检查数据集是否适合流水线使用。

    参数：
        - dataset - 要检查的数据集
    """
    # 如果数据集不是 pandas 的 DataFrame 类型
    if 不是 数据集 类型 是 pandas 的 DataFrame 类型:
        # 准备一个错误信息
        msg = "数据集必须是一个 pandas 的 DataFrame 哦！"
        # 抛出一个错误，告诉别人数据集格式不对
        raise TypeError(msg)

# 定义一个函数，根据配置和运行 ID 替换字符串
def _apply_substitutions(config: PipelineConfig, run_id: str) -> PipelineConfig:
    # 创建一个字典，把运行 ID 存进去
    substitutions = {"timestamp": run_id}

    # 检查存储配置
    if (
        # 如果存储配置是文件或 blob 类型，并且有 base_dir
        (isinstance(config.storage, PipelineFileStorageConfig) 或者 isinstance(config.storage, PipelineBlobStorageConfig))
        和 config.storage.base_dir 存在
    ):
        # 使用字典替换模板中的占位符
        config.storage.base_dir = Template(config.storage.base_dir).substitute(substitutions)

    # 检查缓存配置
    if (
        (isinstance(config.cache, PipelineFileCacheConfig) 或者 isinstance(config.cache, PipelineBlobCacheConfig))
        和 config.cache.base_dir 存在
    ):
        # 同样替换缓存配置中的占位符
        config.cache.base_dir = Template(config.cache.base_dir).substitute(substitutions)

    # 检查报告配置
    if (
        (isinstance(config.reporting, PipelineFileReportingConfig) 或者 isinstance(config.reporting, PipelineBlobReportingConfig))
        和 config.reporting.base_dir 存在
    ):
        # 替换报告配置中的占位符
        config.reporting.base_dir = Template(config.reporting.base_dir).substitute(substitutions)

    # 返回修改后的配置
    return config

# 定义一个函数，创建流水线运行上下文
def _create_run_context(
    storage: PipelineStorage,
    cache: PipelineCache,
    stats: PipelineRunStats,
) -> PipelineRunContext:
    """创建流水线运行时需要的上下文环境。"""
    # 创建一个 PipelineRunContext 对象，包含统计信息、缓存和存储
    return PipelineRunContext(
        stats=stats,  # 使用给定的统计信息
        cache=cache,  # 使用给定的缓存
        storage=storage,  # 使用给定的存储
    )

