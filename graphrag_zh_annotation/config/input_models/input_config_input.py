# 导入一些特殊类型的定义，帮助我们编写更清晰的代码
from typing_extensions import NotRequired, TypedDict
# 导入自定义的枚举类型，用于表示输入数据的类型和文件类型
from graphrag.config.enums import InputFileType, InputType

# 这段代码的版权属于微软公司，遵循MIT许可证
# 注释：这是一个描述性文字，说明这段代码是关于默认配置的参数设置

# 使用typing_extensions库中的NotRequired和TypedDict来创建一个特定的字典类
from typing_extensions import NotRequired, TypedDict

# 继承自TypedDict的类，用来定义“Input”部分的默认配置
class InputConfigInput(TypedDict):
    # 'type'键可以是InputType枚举、字符串或None，但不是必需的
    type: NotRequired[InputType | str | None]

    # 'file_type'键可以是InputFileType枚举、字符串或None，但不是必需的
    file_type: NotRequired[InputFileType | str | None]

    # 'base_dir'键可以是字符串或None，但不是必需的
    base_dir: NotRequired[str | None]

    # 'connection_string'键可以是字符串或None，但不是必需的
    connection_string: NotRequired[str | None]

    # 'container_name'键可以是字符串或None，但不是必需的
    container_name: NotRequired[str | None]

    # 'file_encoding'键可以是字符串或None，但不是必需的
    file_encoding: NotRequired[str | None]

    # 'file_pattern'键可以是字符串或None，但不是必需的
    file_pattern: NotRequired[str | None]

    # 'source_column'键可以是字符串或None，但不是必需的
    source_column: NotRequired[str | None]

    # 'timestamp_column'键可以是字符串或None，但不是必需的
    timestamp_column: NotRequired[str | None]

    # 'timestamp_format'键可以是字符串或None，但不是必需的
    timestamp_format: NotRequired[str | None]

    # 'text_column'键可以是字符串或None，但不是必需的
    text_column: NotRequired[str | None]

    # 'title_column'键可以是字符串或None，但不是必需的
    title_column: NotRequired[str | None]

    # 'document_attribute_columns'键可以是字符串列表、字符串或None，但不是必需的
    document_attribute_columns: NotRequired[list[str] | str | None]

    # 'storage_account_blob_url'键可以是字符串或None，但不是必需的
    storage_account_blob_url: NotRequired[str | None]

