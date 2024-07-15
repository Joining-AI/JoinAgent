# 导入argparse模块，它是一个用于命令行选项、参数和子命令解析的标准库
import argparse

# 从当前文件所在的目录（因为有'.'）导入名为index_cli的函数或类，这个是处理命令行接口的部分
from .cli import index_cli

# 这段代码是Python写的，用于一个叫做"索引引擎"的程序包。它有很多设置和选项，让使用者可以定制程序的行为。
# 下面我会用简单易懂的中文解释每一行的作用：

# 这两行是版权信息和许可证，意思是这个代码由微软公司创建，使用了MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个描述性字符串，告诉人们这个程序包是做什么的
"""The Indexing Engine package root."""

# 导入一个名为argparse的库，它帮助我们处理命令行参数
import argparse

# 从.indexing_engine.cli导入一个叫index_cli的函数，这个函数会执行实际的工作
from .cli import index_cli

# 如果这段代码被直接运行（而不是作为模块导入），那么执行以下代码
if __name__ == "__main__":
    # 创建一个解析器对象，用来理解我们在命令行中输入的参数
    parser = argparse.ArgumentParser()

    # 添加一个参数，--config，用于指定配置文件的路径，不是必须的
    parser.add_argument(
        "--config",
        help="运行管道时使用的配置yaml文件",
        required=False,
        type=str,
    )

    # 添加一个参数，-v 或 --verbose，开启详细日志模式
    parser.add_argument(
        "-v",
        "--verbose",
        help="以详细日志模式运行管道",
        action="store_true",
    )

    # 添加一个参数，--memprofile，开启内存分析
    parser.add_argument(
        "--memprofile",
        help="以内存分析模式运行管道",
        action="store_true",
    )

    # 添加一个参数，--root，用于指定输入数据和输出数据的根目录，默认是当前目录
    parser.add_argument(
        "--root",
        help="如果没有配置文件，输入输出数据的根目录，默认值：当前目录",
        required=False,
        default=".",
        type=str,
    )

    # 添加一个参数，--resume，用于恢复之前的数据运行
    parser.add_argument(
        "--resume",
        help="利用Parquet输出文件恢复给定的数据运行",
        required=False,
        default=None,
        type=str,
    )

    # 添加一个参数，--reporter，用于选择进度报告的方式
    parser.add_argument(
        "--reporter",
        help="使用的进度报告器，可选值：'rich', 'print', 'none'",
        type=str,
    )

    # 添加一个参数，--emit，用于指定输出数据的格式
    parser.add_argument(
        "--emit",
        help="以逗号分隔的数据格式，可选值：'parquet' 和 'csv'，默认='parquet,csv'",
        type=str,
    )

    # 添加一个参数，--dryrun，用于预览配置，但不执行任何操作
    parser.add_argument(
        "--dryrun",
        help="不执行任何步骤，只检查配置",
        action="store_true",
    )

    # 添加一个参数，--nocache，用于禁用缓存
    parser.add_argument("--nocache", help="禁用LLM缓存", action="store_true")

    # 添加一个参数，--init，用于在指定路径创建初始配置
    parser.add_argument(
        "--init",
        help="在给定路径创建初始配置",
        action="store_true",
    )

    # 添加一个参数，--overlay-defaults，用于在提供的配置文件上覆盖默认值
    parser.add_argument(
        "--overlay-defaults",
        help="在提供的配置文件上覆盖默认配置值",
        action="store_true",
    )

    # 解析命令行参数，得到一个args对象
    args = parser.parse_args()

    # 检查如果指定了--overlay-defaults，就必须提供--config
    if args.overlay_defaults and not args.config:
        parser.error("--overlay-defaults requires --config")

    # 调用index_cli函数，传入解析到的参数，开始执行程序
    index_cli(
        root=args.root,
        verbose=args.verbose or False,
        resume=args.resume,
        memprofile=args.memprofile or False,
        nocache=args.nocache or False,
        reporter=args.reporter,
        config=args.config,
        emit=args.emit,
        dryrun=args.dryrun or False,
        init=args.init or False,
        overlay_defaults=args.overlay_defaults or False,
        cli=True,
    )

