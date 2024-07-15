# 导入一个叫做pandas的库，它用于处理表格数据
import pandas as pd

# 导入另一个库，这个库是graphrag的一部分，里面有关于社区报告的结构（schemas）
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 从graphrag的查询模块中导入一个叫做num_tokens的函数，它用来计算文本中的单词数量
from graphrag.query.llm.text_utils import num_tokens

# 这一行是版权声明，告诉我们这段代码的版权属于微软公司，使用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这段代码的作用：按度数降序排序上下文
"""这段代码是用来把东西按照它们连接的数量（度数）从多到少排列的。"""

# 定义一个名为sort_context的函数，它接收一些参数
def sort_context(
    # 一个包含字典的列表，代表本地上下文信息
    local_context: list[dict],
    # 可选的，包含字典的列表，代表子社区报告
    sub_community_reports: list[dict] | None = None,
    # 可选的，整数或None，用于限制返回的上下文字符串的字符数
    max_tokens: int | None = None,
    # 字符串，表示节点ID的列名
    node_id_column: str = schemas.NODE_ID,
    # 字符串，表示节点名称的列名
    node_name_column: str = schemas.NODE_NAME,
    # 字符串，表示节点详情的列名
    node_details_column: str = schemas.NODE_DETAILS,
    # 字符串，表示边ID的列名
    edge_id_column: str = schemas.EDGE_ID,
    # 字符串，表示边详情的列名
    edge_details_column: str = schemas.EDGE_DETAILS,
    # 字符串，表示边度数的列名
    edge_degree_column: str = schemas.EDGE_DEGREE,
    # 字符串，表示边源节点ID的列名
    edge_source_column: str = schemas.EDGE_SOURCE,
    # 字符串，表示边目标节点ID的列名
    edge_target_column: str = schemas.EDGE_TARGET,
    # 字符串，表示声明ID的列名
    claim_id_column: str = schemas.CLAIM_ID,
    # 字符串，表示声明详情的列名
    claim_details_column: str = schemas.CLAIM_DETAILS,
    # 字符串，表示社区ID的列名
    community_id_column: str = schemas.COMMUNITY_ID,
) -> str:
    """根据度数降序排列上下文。

    如果提供了最大字符数，我们将返回符合字符限制的上下文字符串。
    """

    # 内部辅助函数，将结构化数据合并成上下文字符串
    def _get_context_string(
        # 包含字典的列表，代表实体
        entities: list[dict],
        # 包含字典的列表，代表边
        edges: list[dict],
        # 包含字典的列表，代表声明
        claims: list[dict],
        # 可选的，包含子社区报告的列表
        sub_community_reports: list[dict] | None = None,
    ) -> str:
        """将结构化数据连接成一个上下文字符串"""
        # 初始化一个空列表来存储不同部分的字符串
        contexts = []

        # 处理子社区报告
        if sub_community_reports:
            # 筛选出包含社区ID并且非空的报告
            filtered_reports = [
                report
                for report in sub_community_reports
                if community_id_column in report
                and report[community_id_column]
                and str(report[community_id_column]).strip() != ""
            ]
            # 将报告转换为DataFrame并去重
            report_df = pd.DataFrame(filtered_reports).drop_duplicates()
            # 如果不为空，将社区ID转换为整数类型并生成字符串
            if not report_df.empty:
                if report_df[community_id_column].dtype == float:
                    report_df[community_id_column] = report_df[
                        community_id_column
                    ].astype(int)
                contexts.append(
                    f"----Reports-----\n{report_df.to_csv(index=False, sep=',')}"
                )

        # 处理实体
        if entities:
            # 筛选出包含节点ID并且非空的实体
            filtered_entities = [
                entity
                for entity in entities
                if node_id_column in entity
                and entity[node_id_column]
                and str(entity[node_id_column]).strip() != ""
            ]
            # 将实体转换为DataFrame并去重
            entity_df = pd.DataFrame(filtered_entities).drop_duplicates()
            # 如果不为空，将节点ID转换为整数类型并生成字符串
            if not entity_df.empty:
                if entity_df[node_id_column].dtype == float:
                    entity_df[node_id_column] = entity_df[node_id_column].astype(int)
                contexts.append(
                    f"-----Entities-----\n{entity_df.to_csv(index=False, sep=',')}"
                )

        # 处理声明
        if claims and len(claims) > 0:
            # 筛选出包含声明ID并且非空的声明
            filtered_claims = [
                claim
                for claim in claims
                if claim_id_column in claim
                and claim[claim_id_column]
                and str(claim[claim_id_column]).strip() != ""
            ]
            # 将声明转换为DataFrame并去重
            claim_df = pd.DataFrame(filtered_claims).drop_duplicates()
            # 如果不为空，将声明ID转换为整数类型并生成字符串
            if not claim_df.empty:
                if claim_df[claim_id_column].dtype == float:
                    claim_df[claim_id_column] = claim_df[claim_id_column].astype(int)
                contexts.append(
                    f"-----Claims-----\n{claim_df.to_csv(index=False, sep=',')}"
                )

        # 处理边
        if edges:
            # 筛选出包含边ID并且非空的边
            filtered_edges = [
                edge
                for edge in edges
                if edge_id_column in edge
                and edge[edge_id_column]
                and str(edge[edge_id_column]).strip() != ""
            ]
            # 将边转换为DataFrame并去重
            edge_df = pd.DataFrame(filtered_edges).drop_duplicates()
            # 如果不为空，将边ID转换为整数类型并生成字符串
            if not edge_df.empty:
                if edge_df[edge_id_column].dtype == float:
                    edge_df[edge_id_column] = edge_df[edge_id_column].astype(int)
                contexts.append(
                    f"-----Relationships-----\n{edge_df.to_csv(index=False, sep=',')}"
                )

        # 返回各个部分的字符串连接结果
        return "\n\n".join(contexts)

    # 初始化变量，用于存储处理后的数据
    edges = []
    node_details = {}
    claim_details = {}

    # 遍历本地上下文中的每个记录
    for record in local_context:
        # 获取节点名称和相关数据
        node_name = record[node_name_column]
        record_edges = record.get(edge_details_column, [])
        record_edges = [e for e in record_edges if not pd.isna(e)]
        record_node_details = record[node_details_column]
        record_claims = record.get(claim_details_column, [])
        record_claims = [c for c in record_claims if not pd.isna(c)]

        # 更新边缘、节点详情和声明信息
        edges.extend(record_edges)
        node_details[node_name] = record_node_details
        claim_details[node_name] = record_claims

    # 过滤并按边的度数降序排序
    edges = [edge for edge in edges if isinstance(edge, dict)]
    edges = sorted(edges, key=lambda x: x[edge_degree_column], reverse=True)

    # 初始化排序后的边、节点和声明列表
    sorted_edges = []
    sorted_nodes = []
    sorted_claims = []
    # 初始化上下文字符串
    context_string = ""

    # 遍历排序后的边，更新排序列表和上下文字符串
    for edge in edges:
        source_details = node_details.get(edge[edge_source_column], {})
        target_details = node_details.get(edge[edge_target_column], {})
        sorted_nodes.extend([source_details, target_details])
        sorted_edges.append(edge)
        source_claims = claim_details.get(edge[edge_source_column], [])
        target_claims = claim_details.get(edge[edge_target_column], [])
        sorted_claims.extend(source_claims if source_claims else [])
        sorted_claims.extend(target_claims if source_claims else [])

        # 如果设置了最大字符数，检查是否已超出限制
        if max_tokens:
            new_context_string = _get_context_string(
                sorted_nodes, sorted_edges, sorted_claims, sub_community_reports
            )
            if num_tokens(context_string) > max_tokens:
                break
            context_string = new_context_string

    # 如果上下文字符串为空，使用排序后的数据生成字符串
    if context_string == "":
        context_string = _get_context_string(
            sorted_nodes, sorted_edges, sorted_claims, sub_community_reports
        )

    # 返回最终的上下文字符串
    return context_string

