# 这段代码是用来从一组社区报告中获取与选定实体相关的社区的工具函数。

from typing import Any, cast  # 引入两个类型定义的辅助工具
import pandas as pd  # 引入pandas库，用于数据处理
from graphrag.model import CommunityReport, Entity  # 引入自定义的模型类：CommunityReport和Entity

# 下面这段文字是版权声明和许可证信息，表示代码的归属和使用许可

# 定义一个函数，用于获取与选定实体关联的候选社区
def get_candidate_communities(
    selected_entities: list[Entity],  # 输入参数1：一个包含Entity对象的列表，表示已选择的实体
    community_reports: list[CommunityReport],  # 输入参数2：一个包含CommunityReport对象的列表，表示所有的社区报告
    include_community_rank: bool = False,  # 可选参数，默认为False，是否包含社区排名
    use_community_summary: bool = False,  # 可选参数，默认为False，是否使用社区摘要
) -> pd.DataFrame:  # 函数返回值：一个pandas DataFrame，展示社区信息

    # 遍历每个选定的实体，收集它们所属的社区ID
    selected_community_ids = [
        entity.community_ids for entity in selected_entities if entity.community_ids
    ]

    # 将嵌套的社区ID列表展平为单个列表
    selected_community_ids = [
        item for sublist in selected_community_ids for item in sublist
    ]

    # 从所有社区报告中筛选出与选定实体相关的社区报告
    selected_reports = [
        community
        for community in community_reports
        if community.id in selected_community_ids
    ]

    # 调用另一个函数（未显示在此处），将筛选后的社区报告转换为DataFrame并返回
    return to_community_report_dataframe(
        reports=selected_reports,
        include_community_rank=include_community_rank,
        use_community_summary=use_community_summary,
    )

# 定义一个函数，叫 to_community_report_dataframe
# 函数接受三个参数：reports（社区报告列表）、include_community_rank（是否包含排名，默认为False）和use_community_summary（是否使用社区摘要，默认为False）
def to_community_report_dataframe(
    reports: list[CommunityReport],
    include_community_rank: bool = False,
    use_community_summary: bool = False,
) -> pd.DataFrame:
    """这个函数会把社区报告列表变成一个数据框（pandas DataFrame）"""
    
    # 如果报告列表为空，就返回一个空的数据框
    if len(reports) == 0:
        return pd.DataFrame()

    # 创建表头，开始有 "id" 和 "title"
    header = ["id", "title"]
    
    # 检查第一个报告的属性，获取所有属性名，如果有的话
    attribute_cols = list(reports[0].attributes.keys()) if reports[0].attributes else []

    # 从属性列中移除已经在表头中的列
    attribute_cols = [col for col in attribute_cols if col not in header]

    # 将属性列添加到表头
    header.extend(attribute_cols)

    # 添加 "summary" 或 "content" 列，取决于use_community_summary的值
    header.append("summary" if use_community_summary else "content")

    # 如果include_community_rank为真，添加 "rank" 到表头
    if include_community_rank:
        header.append("rank")

    # 创建一个空列表来存储每条报告的信息
    records = []

    # 遍历每个报告
    for report in reports:
        # 创建新记录，包括id、标题和属性值
        new_record = [
            report.short_id if report.short_id else "",  # 报告的简短ID，如果没有就用空字符串
            report.title,  # 报告的标题
            # 把报告的属性值（字符串形式）添加到新记录，如果没有值则用空字符串
            *[
                str(report.attributes.get(field, ""))
                if report.attributes and report.attributes.get(field)
                else ""
                for field in attribute_cols
            ],
        ]

        # 添加报告的摘要或完整内容，取决于use_community_summary的值
        new_record.append(
            report.summary if use_community_summary else report.full_content
        )

        # 如果include_community_rank为真，添加报告的排名
        if include_community_rank:
            new_record.append(str(report.rank))

        # 把新记录添加到记录列表
        records.append(new_record)

    # 最后，用记录列表创建并返回数据框，指定列名为header
    return pd.DataFrame(records, columns=cast(Any, header))

