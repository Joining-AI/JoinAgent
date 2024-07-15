# 导入未来的注解功能，这允许我们在Python 3.7及以下版本使用Python 3.7以上版本的特性
from __future__ import annotations

# 导入日志模块，用于记录程序运行中的信息
import logging

# 导入Callable类，表示可以调用的对象
from collections.abc import Callable

# 导入TYPE_CHECKING常量和一些类型定义，用于类型检查
from typing import TYPE_CHECKING, Any, NamedTuple, cast

# 导入datashaper库中的Workflow类
from datashaper import Workflow

# 从graphrag.index.errors导入错误类，用于处理错误
from graphrag.index.errors import (
    NoWorkflowsDefinedError,
    UndefinedWorkflowError,
    UnknownWorkflowError,
)

# 导入topological_sort函数，用于对工作流进行拓扑排序
from graphrag.index.utils import topological_sort

# 导入默认工作流的模块，但只引用名为_default_workflows的变量
from .default_workflows import default_workflows as _default_workflows

# 导入自定义类型定义
from .typing import VerbDefinitions, WorkflowDefinitions, WorkflowToRun

# 如果正在进行类型检查，导入额外的类型
if TYPE_CHECKING:
    from graphrag.index.config import (
        PipelineWorkflowConfig,
        PipelineWorkflowReference,
        PipelineWorkflowStep,
    )

# 定义一个全局变量，用于计数未命名的工作流
anonymous_workflow_count = 0

# 定义VerbFn类型，表示接受任意参数并返回任意类型的可调用对象
VerbFn = Callable[..., Any]

# 获取名为__name__（本模块名称）的日志记录器
log = logging.getLogger(__name__)

# 定义一个命名元组类LoadWorkflowResult，表示工作流加载的结果
class LoadWorkflowResult(NamedTuple):
    # 工作流列表，按照应运行的顺序排列
    workflows: list[WorkflowToRun]

    # 一个字典，键是工作流名称，值是该工作流依赖的其他工作流列表
    dependencies: dict[str, list[str]]

# 定义一个名为load_workflows的函数，它接受四个参数
def load_workflows(
    workflows_to_load: list[PipelineWorkflowReference],  # 要加载的工作流程列表
    additional_verbs: VerbDefinitions | None = None,  # 可选的自定义动词列表
    additional_workflows: WorkflowDefinitions | None = None,  # 可选的自定义工作流程列表
    memory_profile: bool = False,  # 是否开启内存分析，默认关闭
) -> LoadWorkflowResult:  # 返回的结果是一个包含加载工作流程和依赖关系的对象

    # 这个函数用于加载给定的工作流程
    """
    输入：
        - workflows_to_load：要加载的工作流程
        - additional_verbs：工作流程可用的自定义动词列表
        - additional_workflows：自定义工作流程列表
    输出：
        - 结果[0]：按运行顺序排列的已加载工作流程名称
        - 结果[1]：工作流程名称到其依赖项的字典
    """

    # 创建一个空字典，用于存储待运行的工作流程
    workflow_graph: dict[str, WorkflowToRun] = {}

    # 全局变量，用于匿名工作流程计数
    global anonymous_workflow_count

    # 遍历要加载的工作流程列表
    for reference in workflows_to_load:
        # 获取工作流程的名称
        name = reference.name
        # 检查名称是否为空或仅包含空格，如果是，则视为匿名工作流程
        is_anonymous = name is None or name.strip() == ""
        if is_anonymous:
            # 为匿名工作流程生成一个唯一的名称
            name = f"Anonymous Workflow {anonymous_workflow_count}"
            # 计数器加一
            anonymous_workflow_count += 1
        # 将名称转换为字符串类型
        name = cast(str, name)

        # 获取工作流程的配置
        config = reference.config
        # 使用给定信息创建工作流程
        workflow = create_workflow(
            name or "MISSING NAME!",  # 如果没有名字，就用"MISSING NAME!"
            reference.steps,  # 工作流程步骤
            config,  # 配置信息
            additional_verbs,  # 自定义动词
            additional_workflows,  # 自定义工作流程
        )
        # 将工作流程添加到工作流程图中
        workflow_graph[name] = WorkflowToRun(workflow, config=config or {})

    # 填充任何缺失的工作流程
    for name in list(workflow_graph.keys()):
        # 获取工作流程及其依赖
        workflow = workflow_graph[name]
        deps = [
            d.replace("workflow:", "")  # 移除依赖名称前的"workflow:"
            for d in workflow.workflow.dependencies
            if d.startswith("workflow:")  # 只保留以"workflow:"开头的依赖
        ]
        # 遍历依赖并添加到工作流程图中（如果尚未添加）
        for dependency in deps:
            if dependency not in workflow_graph:
                # 创建一个新的工作流程引用
                reference = {"name": dependency, **workflow.config}
                # 创建并添加工作流程
                workflow_graph[dependency] = WorkflowToRun(
                    workflow=create_workflow(
                        dependency,  # 依赖的名称
                        config=reference,  # 引用的配置
                        additional_verbs=additional_verbs,  # 自定义动词
                        additional_workflows=additional_workflows,  # 自定义工作流程
                        memory_profile=memory_profile,  # 内存分析设置
                    ),
                    config=reference,  # 保存配置
                )

    # 定义一个函数，用于过滤工作流程的外部依赖
    def filter_wf_dependencies(name: str) -> list[str]:
        externals = [
            e.replace("workflow:", "")
            for e in workflow_graph[name].workflow.dependencies
        ]
        # 返回只存在于工作流程图中的外部依赖
        return [e for e in externals if e in workflow_graph]

    # 为每个工作流程创建一个任务图，包含其依赖项
    task_graph = {name: filter_wf_dependencies(name) for name in workflow_graph}
    # 使用拓扑排序算法，按依赖关系确定工作流程的运行顺序
    workflow_run_order = topological_sort(task_graph)
    # 根据运行顺序创建工作流程列表
    workflows = [workflow_graph[name] for name in workflow_run_order]
    # 打印工作流程的运行顺序
    log.info("Workflow Run Order: %s", workflow_run_order)
    # 返回结果对象，包含工作流程列表和依赖关系
    return LoadWorkflowResult(workflows=workflows, dependencies=task_graph)

# 定义一个创建工作流程的函数
def create_workflow(
    # 工作流程的名字，是个字符串
    name: str,
    # 步骤列表，可以是PipelineWorkflowStep类型的一个列表，也可能为空
    steps: list[PipelineWorkflowStep] | None = None,
    # 配置信息，可以是PipelineWorkflowConfig类型的一个对象，也可能为空
    config: PipelineWorkflowConfig | None = None,
    # 可选的动词定义，可以是一个VerbDefinitions类型的对象，也可能为空
    additional_verbs: VerbDefinitions | None = None,
    # 可选的工作流程定义，可以是一个WorkflowDefinitions类型的对象，也可能为空
    additional_workflows: WorkflowDefinitions | None = None,
    # 是否分析内存使用情况，默认为False
    memory_profile: bool = False,
) -> Workflow:
    """根据给定的配置创建一个工作流程"""
    
    # 合并默认的工作流程和用户提供的工作流程（如果有的话）
    additional_workflows = {
        **_default_workflows,  # 先放默认的工作流程
        **(additional_workflows or {}),  # 再放用户提供的，如果为空则不添加
    }

    # 如果没有提供步骤，就根据工作流程名、配置和工作流程定义获取
    steps = steps or _get_steps_for_workflow(name, config, additional_workflows)

    # 移除所有禁用的步骤
    steps = _remove_disabled_steps(steps)

    # 创建并返回一个Workflow对象，包含动词、工作流程的结构信息，以及是否分析内存
    return Workflow(
        verbs=additional_verbs or {},  # 使用动词定义，如果为空则使用{}
        schema={  # 定义工作流程的结构
            "name": name,  # 工作流程的名字
            "steps": steps,  # 步骤列表
        },
        validate=False,  # 是否验证，默认不验证
        memory_profile=memory_profile,  # 是否开启内存分析
    )

# 一个内部函数，用于获取给定工作流程配置的步骤
def _get_steps_for_workflow(
    # 工作流程的名字，可能为空
    name: str | None,
    # 配置信息，可能为空
    config: PipelineWorkflowConfig | None,
    # 工作流程定义，可能为空
    workflows: dict[str, Callable] | None,
) -> list[PipelineWorkflowStep]:
    """根据给定的工作流程配置获取步骤"""
    
    # 如果有配置并且配置中包含步骤，直接返回配置中的步骤
    if config is not None and "steps" in config:
        return config["steps"]

    # 如果没有定义任何工作流程，抛出错误
    if workflows is None:
        raise NoWorkflowsDefinedError

    # 如果没有指定工作流程的名字，抛出错误
    if name is None:
        raise UndefinedWorkflowError

    # 如果指定的工作流程不存在，抛出错误
    if name not in workflows:
        raise UnknownWorkflowError(name)

    # 如果以上条件都满足，调用工作流程定义中的函数，传入配置信息（如果有的话），返回步骤列表
    return workflows[name](config or {})

# 一个内部函数，用于移除步骤列表中被禁用的步骤
def _remove_disabled_steps(
    # 步骤列表
    steps: list[PipelineWorkflowStep],
) -> list[PipelineWorkflowStep]:
    # 过滤出"enabled"属性为True的步骤，返回新的步骤列表
    return [step for step in steps if step.get("enabled", True)]

