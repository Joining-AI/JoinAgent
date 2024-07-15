# 这段代码定义了一些常量，用于表示不同表格中的列名。想象一下，这些是数据表格的标题。

# 开始的两行是关于代码的版权信息和使用的许可证，这很重要，但不是实际的代码。

# 接下来的部分定义了社区报告中常用的字段名称。

# 针对处理后的节点（比如人或组织）表格的列名：
NODE_ID = "human_readable_id"       # 可读的节点标识
NODE_NAME = "title"                # 节点的名称
NODE_DESCRIPTION = "description"   # 节点的描述
NODE_DEGREE = "degree"             # 节点的连接度（与多少其他节点相连）
NODE_DETAILS = "node_details"      # 节点的详细信息
NODE_COMMUNITY = "community"       # 节点所属的社区
NODE_LEVEL = "level"               # 节点在社区中的层级

# 处理后的边（连接节点的关系）表格的列名：
EDGE_ID = "human_readable_id"     # 可读的边标识
EDGE_SOURCE = "source"            # 边的起点
EDGE_TARGET = "target"            # 边的终点
EDGE_DESCRIPTION = "description"  # 边的描述
EDGE_DEGREE = "rank"              # 边的排名
EDGE_DETAILS = "edge_details"     # 边的详细信息
EDGE_WEIGHT = "weight"            # 边的权重（表示关系的强度）

# 处理后的主张（可能的观点或声明）表格的列名：
CLAIM_ID = "human_readable_id"    # 可读的主张标识
CLAIM_SUBJECT = "subject_id"      # 主张涉及的主体的ID
CLAIM_TYPE = "type"               # 主张的类型
CLAIM_STATUS = "status"           # 主张的状态（如：真、假、未知）
CLAIM_DESCRIPTION = "description" # 主张的描述
CLAIM_DETAILS = "claim_details"   # 主张的详细信息

# 社区层级表格的列名：
SUB_COMMUNITY = "sub_communitty"    # 子社区的名称
SUB_COMMUNITY_SIZE = "sub_community_size"  # 子社区的大小（成员数量）
COMMUNITY_LEVEL = "level"           # 社区的层级

# 社区上下文表格的列名：
ALL_CONTEXT = "all_context"        # 所有上下文
CONTEXT_STRING = "context_string"  # 上下文的文本
CONTEXT_SIZE = "context_size"      # 上下文的大小
CONTEXT_EXCEED_FLAG = "context_exceed_limit"  # 是否超过上下文限制的标志

# 社区报告表格的列名：
REPORT_ID = "id"                   # 报告的唯一标识
COMMUNITY_ID = "id"                # 社区的唯一标识
COMMUNITY_LEVEL = "level"          # 社区的层级
TITLE = "title"                    # 报告的标题
SUMMARY = "summary"                # 报告的摘要
FINDINGS = "findings"              # 发现的结果
RATING = "rank"                    # 报告的评级
EXPLANATION = "rating_explanation" # 评级的解释
FULL_CONTENT = "full_content"      # 报告的完整内容
FULL_CONTENT_JSON = "full_content_json"  # 报告的完整内容（以JSON格式）

