# 导入一个Python库，这个库帮助我们定义数据类型
from typing import Any

# 导入datashaper库中的几个类
# ExecutionNode: 代表数据处理过程中的一个步骤
# NoopWorkflowCallbacks: 是一种不做任何操作的工作流回调函数
# Progress: 表示进度信息
# TableContainer: 用来存储表格数据的容器
from datashaper import ExecutionNode, NoopWorkflowCallbacks, Progress, TableContainer

# 导入graphrag.index.progress模块中的ProgressReporter类
# ProgressReporter: 负责报告和更新进度信息
from graphrag.index.progress import ProgressReporter

# 这一行是版权声明，告诉我们这段代码的版权属于微软公司，使用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 下面这段文字是一个文档字符串，解释了这个代码的作用
# "一个工作流回调管理器，它会向ProgressReporter发送更新以显示进度。"
"""
A workflow callback manager that emits updates to a ProgressReporter.
"""

# 定义一个名为ProgressWorkflowCallbacks的类，它继承自NoopWorkflowCallbacks（这个类不做任何操作）
class ProgressWorkflowCallbacks(NoopWorkflowCallbacks):
    # 这个类是用来管理进度报告的
    """A callbackmanager that delegates to a ProgressReporter."""

    # 类中两个属性，一个记录根进度，一个记录进度栈
    _root_progress: ProgressReporter  # 根进度报告器
    _progress_stack: list[ProgressReporter]  # 进度报告器栈

    # 初始化方法，创建新的ProgressWorkflowCallbacks对象时调用，传入一个ProgressReporter
    def __init__(self, progress: ProgressReporter) -> None:
        """创建一个新的ProgressWorkflowCallbacks对象."""
        self._progress = progress  # 设置根进度
        self._progress_stack = [progress]  # 将根进度放入栈中

    # 弹出栈顶的进度报告器
    def _pop(self) -> None:
        self._progress_stack.pop()

    # 向栈中添加一个新进度报告器，作为当前进度报告器的子进度
    def _push(self, name: str) -> None:
        self._progress_stack.append(self._latest.child(name))

    # 获取栈顶的进度报告器（即最新的进度）
    @property
    def _latest(self) -> ProgressReporter:
        return self._progress_stack[-1]

    # 当工作流程开始时调用此回调
    def on_workflow_start(self, name: str, instance: object) -> None:
        """当工作流程开始时执行此回调."""
        self._push(name)  # 添加一个表示工作流程开始的新进度

    # 当工作流程结束时调用此回调
    def on_workflow_end(self, name: str, instance: object) -> None:
        """当工作流程结束时执行此回调."""
        self._pop()  # 移除表示工作流程开始的进度

    # 每当步骤开始时调用此回调
    def on_step_start(self, node: ExecutionNode, inputs: dict[str, Any]) -> None:
        """每当步骤开始时执行此回调."""
        # 根据节点是否有明确的ID添加标识
        verb_id_str = f" ({node.node_id})" if node.has_explicit_id else ""
        # 添加表示当前步骤开始的新进度
        self._push(f"Verb {node.verb.name}{verb_id_str}")
        # 设置初始进度为0%
        self._latest(Progress(percent=0))

    # 每当步骤结束时调用此回调
    def on_step_end(self, node: ExecutionNode, result: TableContainer | None) -> None:
        """每当步骤结束时执行此回调."""
        self._pop()  # 移除表示当前步骤开始的进度

    # 当步骤有进度更新时调用此回调
    def on_step_progress(self, node: ExecutionNode, progress: Progress) -> None:
        """处理进度更新时调用此回调."""
        self._latest(progress)  # 更新最新进度

