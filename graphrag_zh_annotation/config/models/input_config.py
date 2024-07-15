# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们创建数据模型
from pydantic import BaseModel, Field

# 导入默认设置模块，它在graphrag.config包的defaults子模块里
import graphrag.config.defaults as defs

# 从graphrag.config包的enums子模块导入两个枚举类型：InputFileType和InputType
from graphrag.config.enums import InputFileType, InputType

# 这一行是版权声明，告诉我们这段代码的版权属于2024年的微软公司
# Licensed under the MIT License意味着代码遵循MIT许可证，允许他人自由使用、修改和分享

# 这是一个文档字符串，描述了这个代码块的作用，用于参数化默认配置
"""这是用来设置默认配置参数的代码。

我们将用到的工具包括定义数据模型的pydantic，以及我们项目的特定设置（默认值和输入类型）。
"""

# 定义一个名为InputConfig的类，它继承自BaseModel
class InputConfig(BaseModel):
    # 这个类是关于输入配置的默认部分
    """The default configuration section for Input."""

    # 定义一个变量type，类型是InputType，描述是“使用的输入类型”，默认值从defs模块的INPUT_TYPE获取
    type: InputType = Field(description="使用的输入类型。", default=defs.INPUT_TYPE)

    # 定义一个变量file_type，类型是InputFileType，描述是“使用的输入文件类型”，默认值从defs模块的INPUT_FILE_TYPE获取
    file_type: InputFileType = Field(description="使用的输入文件类型。", default=defs.INPUT_FILE_TYPE)

    # 定义一个变量base_dir，类型是字符串，描述是“使用的输入基础目录”，默认值从defs模块的INPUT_BASE_DIR获取
    base_dir: str = Field(description="使用的输入基础目录。", default=defs.INPUT_BASE_DIR)

    # 定义一个变量connection_string，类型是字符串或None，描述是“用于访问Azure Blob存储的连接字符串”，默认值为None
    connection_string: str | None = Field(description="用于访问Azure Blob存储的连接字符串。", default=None)

    # 定义一个变量storage_account_blob_url，类型是字符串或None，描述是“要使用的存储帐户blob URL”，默认值为None
    storage_account_blob_url: str | None = Field(description="要使用的存储帐户blob URL。", default=None)

    # 定义一个变量container_name，类型是字符串或None，描述是“要使用的Azure Blob存储容器名称”，默认值为None
    container_name: str | None = Field(description="要使用的Azure Blob存储容器名称。", default=None)

    # 定义一个变量encoding，类型是字符串或None，描述是“使用的输入文件编码”，默认值从defs模块的INPUT_FILE_ENCODING获取
    encoding: str | None = Field(description="使用的输入文件编码。", default=defs.INPUT_FILE_ENCODING)

    # 定义一个变量file_pattern，类型是字符串，描述是“使用的输入文件模式”，默认值从defs模块的INPUT_TEXT_PATTERN获取
    file_pattern: str = Field(description="使用的输入文件模式。", default=defs.INPUT_TEXT_PATTERN)

    # 定义一个变量file_filter，类型是字典或None，描述是“输入文件的可选过滤器”，默认值为None
    file_filter: dict[str, str] | None = Field(description="输入文件的可选过滤器。", default=None)

    # 定义一个变量source_column，类型是字符串或None，描述是“使用的输入源列”，默认值为None
    source_column: str | None = Field(description="使用的输入源列。", default=None)

    # 定义一个变量timestamp_column，类型是字符串或None，描述是“使用的输入时间戳列”，默认值为None
    timestamp_column: str | None = Field(description="使用的输入时间戳列。", default=None)

    # 定义一个变量timestamp_format，类型是字符串或None，描述是“使用的输入时间戳格式”，默认值为None
    timestamp_format: str | None = Field(description="使用的输入时间戳格式。", default=None)

    # 定义一个变量text_column，类型是字符串，描述是“使用的输入文本列”，默认值从defs模块的INPUT_TEXT_COLUMN获取
    text_column: str = Field(description="使用的输入文本列。", default=defs.INPUT_TEXT_COLUMN)

    # 定义一个变量title_column，类型是字符串或None，描述是“使用的输入标题列”，默认值为None
    title_column: str | None = Field(description="使用的输入标题列。", default=None)

    # 定义一个变量document_attribute_columns，类型是字符串列表，描述是“使用的文档属性列”，默认为空列表
    document_attribute_columns: list[str] = Field(description="使用的文档属性列。", default=[])

