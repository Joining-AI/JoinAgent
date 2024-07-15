# 导入一些有用的工具，帮助我们创建和管理数据
from dataclasses import dataclass as dc_dataclass  # 用于创建数据类的工具
from dataclasses import field  # 用于定义数据类字段的工具
from .cache import PipelineCache  # 从缓存模块导入 PipelineCache 类
from .storage.typing import PipelineStorage  # 从存储模块导入 PipelineStorage 类

# 这是微软公司的版权信息，表示代码遵循 MIT 许可证
# isort: skip_file  # 这行告诉代码排序工具跳过此文件

# 这个模块包含 'PipelineRunStats' 和 'PipelineRunContext' 两个数据类

# 使用 dataclass 工具创建一个数据类，用来记录管道运行的统计信息
@dc_dataclass
class PipelineRunStats:
    # 总运行时间，用浮点数表示，默认是 0
    total_runtime: float = field(default=0)

    # 文档数量，默认是 0
    num_documents: int = field(default=0)

    # 输入加载时间，用浮点数表示，默认是 0
    input_load_time: float = field(default=0)

    # 一个字典，存储每个工作流的信息，默认为空字典
    workflows: dict[str, dict[str, float]] = field(default_factory=dict)


# 创建另一个数据类，提供当前管道运行的上下文信息
@dc_dataclass
class PipelineRunContext:
    # 包含管道运行统计信息的对象
    stats: PipelineRunStats

    # 存储对象，用于处理数据
    storage: PipelineStorage

    # 缓存对象，用于保存和加载数据
    cache: PipelineCache


# 暂时，这个 VerbRunContext 类与 PipelineRunContext 具有相同属性
VerbRunContext = PipelineRunContext
# 提供当前动词运行的上下文信息

