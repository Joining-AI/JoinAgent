# 导入asyncio库，它用于处理异步操作，比如在程序执行其他任务时等待某个任务完成
import asyncio

# 导入datashaper的Progress模块，它可能用于数据处理时的进度跟踪
from datashaper import Progress as DSProgress

# 导入rich库的Console和Group类，它们帮助我们在控制台中以更美观的方式显示信息
from rich.console import Console, Group

# 导入rich.live的Live类，它允许实时更新控制台中的内容
from rich.live import Live

# 导入rich.progress的Progress、TaskID和TimeElapsedColumn类，它们用于创建和管理进度条，包括任务ID和已用时间列
from rich.progress import Progress, TaskID, TimeElapsedColumn

# 导入rich.spinner的Spinner类，它用于创建在任务进行时显示的旋转图标
from rich.spinner import Spinner

# 导入rich.tree的Tree类，它用于创建和显示树状结构的数据
from rich.tree import Tree

# 导入自定义的ProgressReporter类型，它可能是用来报告进度的类
from .types import ProgressReporter

# 这是代码的作者和许可信息，表示代码版权属于微软公司，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段代码的注释说明它是一个基于rich库的命令行界面（CLI）进度报告器
"""Rich-based progress reporter for CLI use."""

# 下面的代码没有显示，但根据引用的链接，可能是一个示例或函数，用于演示如何使用上面导入的类和模块来显示进度
# 参考：https://stackoverflow.com/a/34325723

# 定义一个名为RichProgressReporter的类，它继承自ProgressReporter
class RichProgressReporter(ProgressReporter):
    # 这个类是用于在命令行界面（CLI）中显示丰富的进度报告
    """A rich-based progress reporter for CLI use."""

    # 类中的成员变量，存储不同的对象
    _console: Console       # 控制台对象
    _group: Group           # 组对象
    _tree: Tree             # 树形结构对象
    _live: Live             # 实时更新对象
    _task: TaskID | None    # 任务ID，可能为None
    _prefix: str            # 前缀字符串
    _transient: bool        # 是否为临时显示
    _disposing: bool = False # 是否正在释放资源
    _progressbar: Progress  # 进度条对象
    _last_refresh: float = 0 # 上次刷新时间

    # 释放资源的方法
    def dispose(self) -> None:
        """清理进度报告器"""
        self._disposing = True
        self._live.stop()  # 停止实时更新

    # 获取控制台对象的属性
    @property
    def console(self) -> Console:
        """获取控制台对象"""
        return self._console

    # 获取组对象的属性
    @property
    def group(self) -> Group:
        """获取组对象"""
        return self._group

    # 获取树形结构对象的属性
    @property
    def tree(self) -> Tree:
        """获取树形结构对象"""
        return self._tree

    # 获取实时更新对象的属性
    @property
    def live(self) -> Live:
        """获取实时更新对象"""
        return self._live

    # 初始化方法，创建新的基于rich的进度报告器
    def __init__(
        self,
        prefix: str,         # 进度条前缀
        parent: "RichProgressReporter | None" = None,  # 父级进度报告器，可能为None
        transient: bool = True,  # 是否临时显示
    ) -> None:
        """创建一个新的基于rich的进度报告器"""
        self._prefix = prefix

        # 如果没有父级报告器
        if parent is None:
            # 创建新的控制台、组、树和实时更新对象
            console = Console()
            group = Group(Spinner("dots", prefix), fit=True)
            tree = Tree(group)
            live = Live(
                tree, console=console, refresh_per_second=1, vertical_overflow="crop"
            )
            live.start()

            self._console = console
            self._group = group
            self._tree = tree
            self._live = live
            self._transient = False
        else:  # 如果有父级报告器
            self._console = parent.console
            self._group = parent.group
            # 创建进度条对象，包含默认列和时间已过去列
            progress_columns = [*Progress.get_default_columns(), TimeElapsedColumn()]
            self._progressbar = Progress(
                *progress_columns, console=self._console, transient=transient
            )

            tree = Tree(prefix)
            tree.add(self._progressbar)
            tree.hide_root = True

            # 将新创建的树添加到父级的树中
            if parent is not None:
                parent_tree = parent.tree
                parent_tree.hide_root = False
                parent_tree.add(tree)

            self._tree = tree
            self._live = parent.live
            self._transient = transient

        # 刷新显示
        self.refresh()

    # 带有延时的刷新方法
    def refresh(self) -> None:
        """延迟刷新"""
        now = asyncio.get_event_loop().time()
        duration = now - self._last_refresh
        # 如果超过0.1秒，进行刷新
        if duration > 0.1:
            self._last_refresh = now
            self.force_refresh()

    # 强制刷新
    def force_refresh(self) -> None:
        """强制刷新显示"""
        self.live.refresh()

    # 停止进度报告器
    def stop(self) -> None:
        """停止进度报告器"""
        self._live.stop()

    # 创建子进度条
    def child(self, prefix: str, transient: bool = True) -> ProgressReporter:
        """创建子进度条"""
        return RichProgressReporter(parent=self, prefix=prefix, transient=transient)

    # 报告错误
    def error(self, message: str) -> None:
        """报告错误信息"""
        self._console.print(f"❌ [red]{message}[/red]")

    # 报告警告
    def warning(self, message: str) -> None:
        """报告警告信息"""
        self._console.print(f"⚠️ [yellow]{message}[/yellow]")

    # 报告成功
    def success(self, message: str) -> None:
        """报告成功信息"""
        self._console.print(f"🚀 [green]{message}[/green]")

    # 报告一般信息
    def info(self, message: str) -> None:
        """报告一般信息"""
        self._console.print(message)

    # 更新进度
    def __call__(self, progress_update: DSProgress) -> None:
        """更新进度"""
        # 如果正在释放资源，不进行更新
        if self._disposing:
            return
        progressbar = self._progressbar

        # 如果没有任务ID，创建新的任务
        if self._task is None:
            self._task = progressbar.add_task(self._prefix)

        # 设置进度描述
        progress_description = ""
        if progress_update.description is not None:
            progress_description = f" - {progress_update.description}"

        # 设置已完成和总项数
        completed = progress_update.completed_items or progress_update.percent
        total = progress_update.total_items or 1
        # 更新进度条
        progressbar.update(
            self._task,
            completed=completed,
            total=total,
            description=f"{self._prefix}{progress_description}",
        )
        # 如果已完成，且是临时显示，隐藏进度条
        if completed == total and self._transient:
            progressbar.update(self._task, visible=False)

        # 刷新显示
        self.refresh()

