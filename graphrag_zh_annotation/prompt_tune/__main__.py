# 导入一个叫做argparse的库，它帮助我们处理命令行参数
import argparse

# 导入asyncio库，这个库用于异步编程，让程序能同时做多件事
import asyncio

# 导入Python的枚举（Enum）类，这是一个特殊类型的类，用来创建固定的、不可变的值集合
from enum import Enum

# 从graphrag.prompt_tune.generator导入MAX_TOKEN_COUNT，这是一个常量，表示最大的令牌（token）数量
from graphrag.prompt_tune.generator import MAX_TOKEN_COUNT

# 从graphrag.prompt_tune.loader导入MIN_CHUNK_SIZE，这也是一个常量，表示最小的数据块大小
from graphrag.prompt_tune.loader import MIN_CHUNK_SIZE

# 从当前文件夹下的cli模块导入fine_tune函数，这个函数可能用来微调模型
from .cli import fine_tune

# 这是一个版权声明，告诉我们这个代码是微软公司2024年的作品，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是程序的主说明，告诉我们这个包是关于自动提示模板的
"""The Prompt auto templating package root."""

# 定义一个名为DocSelectionType的枚举类，它有三种类型：ALL（所有）、RANDOM（随机）和TOP（顶部）
class DocSelectionType(Enum):
    # 类中的三个成员变量，每个都代表一种文档选择方式
    ALL = "all"   # 选择所有文档
    RANDOM = "random"  # 随机选择文档
    TOP = "top"   # 选择最好的（顶部）文档

    # 这个方法返回枚举值的字符串形式
    def __str__(self):
        # 返回枚举成员的值（也就是"all"、"random"或"top"）
        return self.value

# 如果这个文件被直接运行（而不是作为模块导入），则执行以下代码
if __name__ == "__main__":
    # 创建一个解析命令行参数的工具
    parser = argparse.ArgumentParser()

    # 添加一个参数 "--root"，用于指定数据项目根目录，可以是.yml、.json或.env文件所在的地方
    # 参数不是必须的，默认值是当前目录 "."
    parser.add_argument(
        "--root",
        help="数据项目根目录，包含配置文件",
        required=False,
        type=str,
        default=".",
    )

    # 添加一个参数 "--domain"，用于指定输入数据相关的领域，如“空间科学”、“微生物学”或“环境新闻”
    # 如果不指定，将从输入数据中推断领域
    parser.add_argument(
        "--domain",
        help="输入数据相关的领域",
        required=False,
        default="",
        type=str,
    )

    # 添加一个参数 "--method"，用于选择文档的方式，可以是"all"、"random"或"top"
    # 参数类型是预先定义好的枚举类型DocSelectionType
    # 默认值是DocSelectionType.RANDOM
    parser.add_argument(
        "--method",
        help="选择文档的方法",
        required=False,
        type=DocSelectionType,
        choices=list(DocSelectionType),
        default=DocSelectionType.RANDOM,
    )

    # 添加一个参数 "--limit"，用于限制在随机或顶部选择时加载的文件数量
    parser.add_argument(
        "--limit",
        help="随机或顶部选择时加载的文件数量上限",
        type=int,
        required=False,
        default=15,
    )

    # 添加一个参数 "--max-tokens"，用于设定提示生成的最大令牌数
    parser.add_argument(
        "--max-tokens",
        help="生成提示时的最大令牌数",
        type=int,
        required=False,
        default=MAX_TOKEN_COUNT,
    )

    # 添加一个参数 "--chunk-size"，用于设定提示生成的最大令牌数
    # 注意：这里的描述似乎重复了，应该是不同的参数
    parser.add_argument(
        "--chunk-size",
        help="提示生成的最大令牌数",
        type=int,
        required=False,
        default=MIN_CHUNK_SIZE,
    )

    # 添加一个参数 "--language"，用于设定输入和输出在GraphRAG中的主要语言
    parser.add_argument(
        "--language",
        help="输入和输出的语言",
        type=str,
        required=False,
        default="",
    )

    # 添加一个参数 "--no-entity-types"，如果使用，将进行无类型实体提取生成
    parser.add_argument(
        "--no-entity-types",
        help="使用无类型的实体提取生成",
        action="store_true",
        required=False,
        default=False,
    )

    # 添加一个参数 "--output"，用于指定保存生成的提示的文件夹
    parser.add_argument(
        "--output",
        help="保存生成的提示的文件夹",
        type=str,
        required=False,
        default="prompts",
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 获取事件循环
    loop = asyncio.get_event_loop()

    # 使用事件循环运行直到完成fine_tune函数
    # 将命令行参数传递给该函数
    loop.run_until_complete(
        fine_tune(
            args.root,
            args.domain,
            str(args.method),
            args.limit,
            args.max_tokens,
            args.chunk_size,
            args.language,
            args.no_entity_types,
            args.output,
        )
    )

