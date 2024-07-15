# 导入一个叫做pandas的库，它用于处理表格数据
import pandas as pd

# 导入graphrag库中关于社区报告模式的部分
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 从graphrag库的查询模块导入一个用于计算文本中单词数量的工具函数
from graphrag.query.llm.text_utils import num_tokens

# 从当前文件夹中的sort_context模块导入排序上下文的函数
from .sort_context import sort_context

# 这是一个版权声明，告诉我们这段代码的版权属于微软公司，使用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个模块包含的功能
# """A module containing the build_mixed_context method definition."""

# 这些是代码的主体，但我们没有看到具体的方法或函数定义。这可能是一个模块设置和导入部分，
# 具体的函数或类定义可能在后面的代码中出现，但这里没有显示出来。

# 定义一个名为build_mixed_context的函数，它接收两个参数：context（一个包含字典的列表）和max_tokens（一个整数）
def build_mixed_context(context: list[dict], max_tokens: int) -> str:

    """
    这个函数的作用是将所有子社区的上下文合并成一个父级上下文。

    如果总的上下文超过限制，我们会用子社区的报告来代替。
    """

    # 首先，按照子社区的大小（上下文数量）降序排列context
    sorted_context = sorted(
        context, key=lambda x: x[schemas.CONTEXT_SIZE], reverse=True
    )

    # 初始化一些变量
    substitute_reports = []  # 存放用于替换的子社区报告
    final_local_contexts = []  # 最终保留的局部上下文
    exceeded_limit = True  # 标记是否超过最大令牌数
    context_string = ""  # 用于存储最终的上下文字符串

    # 遍历排序后的子社区上下文
    for idx, sub_community_context in enumerate(sorted_context):
        # 如果超过限制，处理子社区报告
        if exceeded_limit:
            # 如果子社区有完整报告，就添加到替代报告列表中
            if sub_community_context[schemas.FULL_CONTENT]:
                substitute_reports.append({
                    schemas.COMMUNITY_ID: sub_community_context[schemas.SUB_COMMUNITY],
                    schemas.FULL_CONTENT: sub_community_context[schemas.FULL_CONTENT],
                })
            else:
                # 若子社区没有报告，使用它的局部上下文
                final_local_contexts.extend(sub_community_context[schemas.ALL_CONTEXT])
                continue

            # 将剩余子社区的局部上下文添加到列表中
            remaining_local_context = []
            for rid in range(idx + 1, len(sorted_context)):
                remaining_local_context.extend(sorted_context[rid][schemas.ALL_CONTEXT])

            # 排序并合并剩余的局部上下文和替代报告，生成新的上下文字符串
            new_context_string = sort_context(
                local_context=remaining_local_context + final_local_contexts,
                sub_community_reports=substitute_reports,
            )

            # 检查新字符串的令牌数是否在限制内
            if num_tokens(new_context_string) <= max_tokens:
                exceeded_limit = False  # 未超过限制
                context_string = new_context_string  # 更新上下文字符串
                break

    # 如果所有子社区的报告都超过限制，就添加报告直到达到最大令牌数
    if exceeded_limit:
        substitute_reports = []  # 重新初始化替代报告列表
        for sub_community_context in sorted_context:
            substitute_reports.append({
                schemas.COMMUNITY_ID: sub_community_context[schemas.SUB_COMMUNITY],
                schemas.FULL_CONTENT: sub_community_context[schemas.FULL_CONTENT],
            })

            # 将所有报告转换为CSV格式的字符串
            new_context_string = pd.DataFrame(substitute_reports).to_csv(
                index=False, sep=","
            )

            # 检查新字符串的令牌数，如果超过限制，停止添加报告
            if num_tokens(new_context_string) > max_tokens:
                break

            context_string = new_context_string  # 更新上下文字符串

    # 返回最终的上下文字符串
    return context_string

