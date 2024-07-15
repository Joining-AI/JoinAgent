# 导入logging模块，它帮助我们在程序中记录信息和错误
import logging

# 导入random模块，用于生成随机数，可以让我们的程序有随机行为
import random

# from typing import Any, cast 是Python的类型注解，用于告诉程序某些变量可能的数据类型，但这里不详细解释
from typing import Any, cast

# 导入pandas库，这是一个强大的数据处理库，可以用来组织和操作表格数据
import pandas as pd

# 导入tiktoken库，这个库可能用于处理某种特定的令牌或认证，具体功能未知，因为没有提供更多信息
import tiktoken

# 从graphrag.model导入CommunityReport和Entity类，它们可能是程序中用来表示社区报告和实体（比如人、地点）的结构
from graphrag.model import CommunityReport, Entity

# 从graphrag.query.llm.text_utils导入num_tokens函数，这个函数可能计算文本中的单词数量
from graphrag.query.llm.text_utils import num_tokens

# 这一行是版权声明，告诉我们这个代码的版权属于微软公司，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为"Community Context"的模块，这部分代码可能与社区相关的信息有关

# 创建一个日志器（logger），名字叫__name__，它会记录这个文件里的日志信息
log = logging.getLogger(__name__)

# 定义一个函数build_community_context，它有多个参数
def build_community_context(
    # 这是一个包含社区报告的列表
    community_reports: list[CommunityReport],
    # 这是一个实体列表，可能是None
    entities: list[Entity] | None = None,
    # 这是一个编码器，也可能是None
    token_encoder: tiktoken.Encoding | None = None,
    # 如果为True，则使用社区摘要
    use_community_summary: bool = True,
    # 列之间的分隔符，默认是"|"
    column_delimiter: str = "|",
    # 如果为True，会打乱数据
    shuffle_data: bool = True,
    # 如果为True，包含社区排名
    include_community_rank: bool = False,
    # 最小社区排名，默认是0
    min_community_rank: int = 0,
    # 排名的列名，默认是"rank"
    community_rank_name: str = "rank",
    # 如果为True，包含社区权重
    include_community_weight: bool = True,
    # 权重的列名，默认是"occurrence weight"
    community_weight_name: str = "occurrence weight",
    # 如果为True，权重会被归一化
    normalize_community_weight: bool = True,
    # 最大允许的令牌数，默认是8000
    max_tokens: int = 8000,
    # 如果为True，只创建一个批次
    single_batch: bool = True,
    # 上下文名称，默认是"Reports"
    context_name: str = "Reports",
    # 随机种子，默认是86
    random_state: int = 86,
) -> tuple[str | list[str], dict[str, pd.DataFrame]]:
    """
    准备社区报告数据表作为系统提示的上下文数据。

    如果提供了实体，社区权重将计算为与实体相关的文本单元的数量。

    计算出的权重将添加到社区报告的属性中，并添加到上下文数据表。
    """
    # 如果提供实体、社区报告不为空、需要包含社区权重并且报告的属性中没有权重属性
    if (
        entities
        and len(community_reports) > 0
        and include_community_weight
        and (
            community_reports[0].attributes is None
            or community_weight_name not in community_reports[0].attributes
        )
    ):
        # 打印信息，开始计算社区权重
        log.info("Computing community weights...")
        # 计算社区权重并更新社区报告
        community_reports = _compute_community_weights(
            community_reports=community_reports,
            entities=entities,
            weight_attribute=community_weight_name,
            normalize=normalize_community_weight,
        )

    # 选择排名大于等于最小社区排名的报告
    selected_reports = [
        report
        for report in community_reports
        if report.rank and report.rank >= min_community_rank
    ]

    # 如果没有选择到报告，返回空列表和字典
    if selected_reports is None or len(selected_reports) == 0:
        return ([], {})

    # 如果需要打乱数据，设置随机种子并打乱选择的报告
    if shuffle_data:
        random.seed(random_state)
        random.shuffle(selected_reports)

    # 创建上下文文本开头
    current_context_text = f"-----{context_name}-----" + "\n"

    # 创建表头
    header = ["id", "title"]  # 始终包含id和title
    # 获取报告的属性列名
    attribute_cols = (
        list(selected_reports[0].attributes.keys())
        if selected_reports[0].attributes
        else []
    )
    # 从属性列名中移除已有的表头
    attribute_cols = [col for col in attribute_cols if col not in header]
    # 如果不包含社区权重，移除权重列名
    if not include_community_weight:
        attribute_cols = [col for col in attribute_cols if col != community_weight_name]
    # 添加属性列名到表头
    header.extend(attribute_cols)
    # 添加"summary"或"content"列名
    header.append("summary" if use_community_summary else "content")
    # 如果包含社区排名，添加排名列名
    if include_community_rank:
        header.append(community_rank_name)

    # 将表头添加到上下文文本
    current_context_text += column_delimiter.join(header) + "\n"
    # 计算当前上下文文本的令牌数
    current_tokens = num_tokens(current_context_text, token_encoder)
    # 初始化当前上下文记录
    current_context_records = [header]
    # 初始化所有上下文文本和记录的列表
    all_context_text = []
    all_context_records = []

    # 遍历选择的报告
    for report in selected_reports:
        # 创建新上下文行
        new_context = [
            report.short_id,  # 报告的简短ID
            report.title,  # 报告的标题
            # 报告属性值，如果不存在则为空字符串
            *[
                str(report.attributes.get(field, "")) if report.attributes else ""
                for field in attribute_cols
            ],
        ]
        # 添加摘要或完整内容
        new_context.append(
            report.summary if use_community_summary else report.full_content
        )
        # 如果包含社区排名，添加排名
        if include_community_rank:
            new_context.append(str(report.rank))

        # 创建新上下文行文本
        new_context_text = column_delimiter.join(new_context) + "\n"

        # 计算新上下文行的令牌数
        new_tokens = num_tokens(new_context_text, token_encoder)

        # 如果当前上下文文本加上新行超过最大令牌数
        if current_tokens + new_tokens > max_tokens:
            # 将当前上下文记录转换为DataFrame并按权重和排名排序（如果存在）
            if len(current_context_records) > 1:
                record_df = _convert_report_context_to_df(
                    context_records=current_context_records[1:],
                    header=current_context_records[0],
                    weight_column=community_weight_name
                    if entities and include_community_weight
                    else None,
                    rank_column=community_rank_name if include_community_rank else None,
                )
            else:
                record_df = pd.DataFrame()

            # 将DataFrame转换回CSV文本
            current_context_text = record_df.to_csv(index=False, sep=column_delimiter)

            # 如果只创建一个批次，返回当前上下文文本和DataFrame
            if single_batch:
                return current_context_text, {context_name.lower(): record_df}

            # 将当前上下文文本和DataFrame添加到所有上下文的列表中
            all_context_text.append(current_context_text)
            all_context_records.append(record_df)

            # 开始新的批次
            current_context_text = (
                f"-----{context_name}-----"
                + "\n"
                + column_delimiter.join(header)
                + "\n"
            )
            current_tokens = num_tokens(current_context_text, token_encoder)
            current_context_records = [header]
        else:
            # 如果没超过最大令牌数，将新行添加到当前上下文文本和记录
            current_context_text += new_context_text
            current_tokens += new_tokens
            current_context_records.append(new_context)

    # 如果最后一个批次还没有添加，添加它
    if current_context_text not in all_context_text:
        # 将当前上下文记录转换为DataFrame并按权重和排名排序（如果存在）
        if len(current_context_records) > 1:
            record_df = _convert_report_context_to_df(
                context_records=current_context_records[1:],
                header=current_context_records[0],
                weight_column=community_weight_name
                if entities and include_community_weight
                else None,
                rank_column=community_rank_name if include_community_rank else None,
            )
        else:
            record_df = pd.DataFrame()

        # 将DataFrame转换回CSV文本
        current_context_text = record_df.to_csv(index=False, sep=column_delimiter)
        all_context_records.append(record_df)
        all_context_text.append(current_context_text)

    # 返回所有上下文文本的列表和合并后的DataFrame
    return all_context_text, {
        context_name.lower(): pd.concat(all_context_records, ignore_index=True)
    }

# 定义一个函数，计算社区权重
def _compute_community_weights(
    # 输入：社区报告列表，每个报告包含社区信息和实体信息
    community_reports: list[CommunityReport],
    # 输入：实体列表，每个实体可能属于一个或多个社区
    entities: list[Entity],
    # 输入：权重属性名称，默认是"occurrence"，表示出现次数
    weight_attribute: str = "occurrence",
    # 输入：是否需要归一化，默认为True
    normalize: bool = True,
) -> list[CommunityReport]:
    """这个函数用来计算社区的权重，权重是社区内与实体相关的文本单元的数量。"""

    # 创建一个字典，键是社区ID，值是该社区的文本单元ID列表
    community_text_units = {}
    # 遍历每个实体
    for entity in entities:
        # 如果实体关联了社区ID
        if entity.community_ids:
            # 遍历实体关联的所有社区ID
            for community_id in entity.community_ids:
                # 如果社区ID不在字典中，创建一个新的空列表
                if community_id not in community_text_units:
                    community_text_units[community_id] = []
                # 将实体的文本单元ID添加到对应的社区ID列表中
                community_text_units[community_id].extend(entity.text_unit_ids)

    # 遍历每个社区报告
    for report in community_reports:
        # 如果报告的属性为空，创建一个新的空字典
        if not report.attributes:
            report.attributes = {}
        # 计算社区报告的权重，即对应社区ID的文本单元数量
        report.attributes[weight_attribute] = len(
            set(community_text_units.get(report.community_id, []))
        )

    # 如果需要归一化
    if normalize:
        # 收集所有报告的权重
        all_weights = [
            report.attributes[weight_attribute]
            for report in community_reports
            if report.attributes
        ]
        # 找到最大权重
        max_weight = max(all_weights)
        # 归一化每个报告的权重
        for report in community_reports:
            # 如果报告有属性（即有权重）
            if report.attributes:
                # 更新报告的权重，使其在0到1之间
                report.attributes[weight_attribute] = (
                    report.attributes[weight_attribute] / max_weight
                )

    # 返回更新后的社区报告列表
    return community_reports

# 定义一个名为_rank_report_context的函数，它接收两个参数：一个叫report_df的数据框（DataFrame类型）和两个可选参数，weight_column和rank_column（默认为None）
def _rank_report_context(
    report_df: pd.DataFrame,  # 输入的数据框
    weight_column: str | None = "occurrence weight",  # 权重列的名称，默认是"occurrence weight"
    rank_column: str | None = "rank",  # 排名列的名称，默认是"rank"
) -> pd.DataFrame:  # 返回的数据框

    # 创建一个空列表，用于存放需要排序的列名
    rank_attributes = []

    # 如果weight_column有值，将该列添加到列表中，并将该列转换为浮点数类型
    if weight_column:
        rank_attributes.append(weight_column)
        report_df[weight_column] = report_df[weight_column].astype(float)

    # 如果rank_column有值，将该列添加到列表中，并将该列转换为浮点数类型
    if rank_column:
        rank_attributes.append(rank_column)
        report_df[rank_column] = report_df[rank_column].astype(float)

    # 如果列表中有列名，就按照这些列对数据框进行降序排序
    if len(rank_attributes) > 0:
        report_df.sort_values(by=rank_attributes, ascending=False, inplace=True)

    # 返回排序后的新数据框
    return report_df

# 定义一个名为_convert_report_context_to_df的函数，它接收三个参数：context_records（列表中的列表），header（列标题列表），以及两个可选参数weight_column和rank_column
def _convert_report_context_to_df(
    context_records: list[list[str]],  # 输入的记录列表，每个记录都是一个字符串列表
    header: list[str],  # 列标题列表
    weight_column: str | None = None,  # 权重列的名称，默认为None
    rank_column: str | None = None,  # 排名列的名称，默认为None
) -> pd.DataFrame:  # 返回的数据框

    # 将context_records转换为一个数据框，并指定列名
    record_df = pd.DataFrame(
        context_records,  # 记录列表
        columns=cast(Any, header),  # 列标题列表
    )

    # 调用_rank_report_context函数对新数据框进行排序，并返回排序后的结果
    return _rank_report_context(
        report_df=record_df,  # 输入的数据框
        weight_column=weight_column,  # 权重列的名称
        rank_column=rank_column,  # 排名列的名称
    )

