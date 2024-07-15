# 这一行告诉Python使用未来的注解方式，让代码在新版本中也能正常工作
from __future__ import annotations

# 导入泛型（Generic）、字面量（Literal）和类型变量（TypeVar），它们是处理数据类型的方式
from typing import Generic, Literal, TypeVar

# 导入一个叫做BaseModel的类，它是Pydantic库的一部分，用来创建数据模型
from pydantic import BaseModel

# 导入Field，这是Pydantic的一个函数，用于定义模型中的字段和属性
from pydantic import Field as pydantic_Field

# 从graphrag.config.enums模块导入两个枚举类：InputFileType和InputType，它们是预设的一些输入类型
from graphrag.config.enums import InputFileType, InputType

# 从当前目录下的workflow模块导入PipelineWorkflowStep类，可能与工作流程有关
from .workflow import PipelineWorkflowStep

# 这是一个类型变量，用"T"表示可以代表任何其他类型
T = TypeVar("T")

# 定义一个名为PipelineInputConfig的类，它继承自BaseModel并且是泛型类，参数T代表可以存储任何类型的数据
class PipelineInputConfig(BaseModel, Generic[T]):
    # 定义一个变量file_type，类型为T，表示输入文件的类型
    file_type: T
    """这个变量用来保存输入文件的类型。"""

    # 定义一个变量type，类型为InputType或None，初始值为None
    type: InputType | None = pydantic_Field(
        # 这个变量描述了要使用的输入类型
        description="要使用的输入类型。",
        # 默认值是None
        default=None,
    )
    """这个变量用来指定要使用的输入类型。"""

    # 定义一个变量connection_string，类型为字符串或None，初始值为None
    connection_string: str | None = pydantic_Field(
        # 这个变量用于保存输入文件的blob缓存连接字符串
        description="输入文件的blob缓存连接字符串。",
        # 默认值是None
        default=None,
    )
    """这个变量保存输入文件的blob缓存连接字符串。"""

    # 定义一个变量storage_account_blob_url，类型为字符串或None，初始值为None
    storage_account_blob_url: str | None = pydantic_Field(
        # 这个变量用于保存输入文件的存储账户blob网址
        description="输入文件的存储账户blob网址。",
        # 默认值是None
        default=None,
    )
    """这个变量保存输入文件的存储账户blob网址。"""

    # 定义一个变量container_name，类型为字符串或None，初始值为None
    container_name: str | None = pydantic_Field(
        # 这个变量用于保存输入文件的容器名称
        description="输入文件的容器名称。",
        # 默认值是None
        default=None,
    )
    """这个变量保存输入文件的容器名称。"""

    # 定义一个变量base_dir，类型为字符串或None，初始值为None
    base_dir: str | None = pydantic_Field(
        # 这个变量用于保存输入文件的基本目录
        description="输入文件的基础目录。",
        # 默认值是None
        default=None,
    )
    """这个变量保存输入文件的基础目录。"""

    # 定义一个变量file_pattern，类型为字符串，没有默认值
    file_pattern: str = pydantic_Field(
        # 这个变量用于保存输入文件的正则表达式匹配模式
        description="输入文件的正则表达式匹配模式。",
    )
    """这个变量保存输入文件的正则表达式匹配模式。"""

    # 定义一个变量file_filter，类型为字典（字符串到字符串）或None，初始值为None
    file_filter: dict[str, str] | None = pydantic_Field(
        # 这个变量用于保存输入文件的可选过滤条件
        description="输入文件的可选过滤条件。",
        # 默认值是None
        default=None,
    )
    """这个变量保存输入文件的可选过滤条件。"""

    # 定义一个变量post_process，类型为PipelineWorkflowStep列表或None，初始值为None
    post_process: list[PipelineWorkflowStep] | None = pydantic_Field(
        # 这个变量用于保存输入后的处理步骤
        description="输入后的处理步骤。",
        # 默认值是None
        default=None,
    )
    """这个变量保存对输入进行后处理的步骤。"""

    # 定义一个变量encoding，类型为字符串或None，初始值为None
    encoding: str | None = pydantic_Field(
        # 这个变量用于保存输入文件的编码方式
        description="输入文件的编码方式。",
        # 默认值是None
        default=None,
    )
    """这个变量保存输入文件的编码方式。"""

# 定义一个名为PipelineCSVInputConfig的类，它是PipelineInputConfig的子类，参数类型是Literal[InputFileType.csv]
class PipelineCSVInputConfig(PipelineInputConfig[Literal[InputFileType.csv]]):
    """这个类用来存储CSV文件输入的配置信息"""

    # 定义一个变量file_type，它的值总是InputFileType.csv
    file_type: Literal[InputFileType.csv] = InputFileType.csv

    # 定义一个变量source_column，表示文档来源的列，初始值为None
    source_column: str | None = pydantic_Field(description="文档来源的列", default=None)
    """文档来源的列"""

    # 定义一个变量timestamp_column，表示文档时间戳的列，初始值为None
    timestamp_column: str | None = pydantic_Field(description="文档时间戳的列", default=None)
    """文档时间戳的列"""

    # 定义一个变量timestamp_format，表示时间戳列的格式，用于正确解析，初始值为None
    timestamp_format: str | None = pydantic_Field(description="时间戳列的格式", default=None)
    """时间戳列的格式，用于正确解析"""

    # 定义一个变量text_column，表示文档文本的列，初始值为None
    text_column: str | None = pydantic_Field(description="文档文本的列", default=None)
    """文档文本的列"""

    # 定义一个变量title_column，表示文档标题的列，初始值为None
    title_column: str | None = pydantic_Field(description="文档标题的列", default=None)
    """文档标题的列"""


# 定义一个名为PipelineTextInputConfig的类，同样是PipelineInputConfig的子类，参数类型是Literal[InputFileType.text]
class PipelineTextInputConfig(PipelineInputConfig[Literal[InputFileType.text]]):
    """这个类用来存储纯文本输入的配置信息"""

    # 定义一个变量file_type，它的值总是InputFileType.text
    file_type: Literal[InputFileType.text] = InputFileType.text

    # 文本输入特有的设置
    # 定义一个变量title_text_length，表示从文本中取多少个字符作为标题，默认值为None
    title_text_length: int | None = pydantic_Field(description="从文本中取多少个字符作为标题", default=None)
    """从文本中取多少个字符作为标题"""


# 定义一个名为PipelineInputConfigTypes的变量，它代表Pipeline可以接受的输入类型
PipelineInputConfigTypes = PipelineCSVInputConfig | PipelineTextInputConfig
"""代表管道中可以使用的输入类型"""

