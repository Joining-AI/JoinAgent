# 导入argparse模块，它帮助我们处理命令行参数
import argparse

# 导入Enum类，它是Python中用于创建枚举类型的数据结构
from enum import Enum

# 从当前目录下的cli模块导入两个函数：run_global_search和run_local_search
from .cli import run_global_search, run_local_search

# 这是微软公司的版权声明，表示代码由微软公司编写
# 并且遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个包是做什么的
"""The Query Engine package root."""

# 定义一个名为SearchType的枚举类，表示两种搜索类型
class SearchType(Enum):
    # 枚举值LOCAL代表本地搜索
    LOCAL = "local"
    # 枚举值GLOBAL代表全局搜索
    GLOBAL = "global"

    # 当我们将枚举对象转换为字符串时，这个方法返回对应的值
    def __str__(self):
        # 返回枚举成员的值（"local"或"global"）
        return self.value

# INVALID_METHOD_ERROR是一个错误信息，表示使用了无效的方法
INVALID_METHOD_ERROR = "Invalid method"

# 如果这个文件被直接运行（而不是作为模块导入），则执行以下代码
if __name__ == "__main__":
    # 创建一个解析命令行参数的工具
    parser = argparse.ArgumentParser()

    # 添加一个参数"data"，用于指定处理数据的路径，不是必须的，类型是字符串
    parser.add_argument(
        "--data",
        help="数据管道输出的数据路径",
        required=False,
        type=str,
    )

    # 添加一个参数"root"，用于指定数据项目根目录，默认值是当前目录，类型是字符串
    parser.add_argument(
        "--root",
        help="数据项目的根目录，默认值：当前目录",
        required=False,
        default=".",
        type=str,
    )

    # 添加一个必需的参数"method"，选择要运行的本地或全局方法，类型是SearchType
    parser.add_argument(
        "--method",
        help="要运行的方法，可选：local或global",
        required=True,
        type=SearchType,
        choices=list(SearchType),
    )

    # 添加一个参数"community_level"，用于设定Leiden社区层次结构中的级别，数值越大，使用的社区报告越小
    parser.add_argument(
        "--community_level",
        help="在Leiden社区层次结构中选择的级别，数值越大，社区越小",
        type=int,
        default=2,
    )

    # 添加一个参数"response_type"，用于描述响应的类型和格式，可以自定义，例如：多个段落、单个段落等，默认值是"多个段落"
    parser.add_argument(
        "--response_type",
        help="描述响应类型和格式的自由文本，如：多个段落，单个段落，单个句子，3-7点列表，单页，多页报告",
        type=str,
        default="Multiple Paragraphs",
    )

    # 添加一个必需的参数"query"，用于指定要运行的查询，类型是字符串，可以有多个，但这里只取第一个
    parser.add_argument(
        "query",
        nargs=1,
        help="要运行的查询",
        type=str,
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 根据"method"参数的值，执行相应的函数
    match args.method:
        # 如果是局部搜索
        case SearchType.LOCAL:
            run_local_search(
                args.data,
                args.root,
                args.community_level,
                args.response_type,
                args.query[0],
            )
        # 如果是全局搜索
        case SearchType.GLOBAL:
            run_global_search(
                args.data,
                args.root,
                args.community_level,
                args.response_type,
                args.query[0],
            )
        # 其他情况抛出错误，因为方法无效
        case _:
            raise ValueError(INVALID_METHOD_ERROR)

