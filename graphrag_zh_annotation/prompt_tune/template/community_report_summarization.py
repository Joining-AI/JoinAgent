# 这段代码是微软公司2024年的版权
# 使用的是MIT许可证

# 这是一个用于社区报告总结的提示微调程序

COMMUNITY_REPORT_SUMMARIZATION_PROMPT = """
# 你将扮演的角色
{persona}

# 目标
像一个{role}那样，写一份全面的社区评估报告。报告内容包括社区重要实体和它们的关系概述。

# 报告结构
报告应包含以下部分：
- 标题：代表社区关键实体的名字 - 标题要简短但具体。如果可能，包含有代表性的命名实体。
- 摘要：社区整体结构的执行摘要，实体如何相互关联，以及与实体相关的要点。
- 报告评分：{report_rating_description}
- 评分解释：用一句话解释评分。
- 详细发现：关于社区的5到10个关键见解。每个见解都有一个简短的总结，后面跟着根据以下规则展开的多段解释性文本。

返回格式良好的JSON字符串作为输出。不要使用不必要的转义序列。输出应是一个可以被json.loads解析的单个JSON对象。
    {{
        "title": "<report_title>",
        "summary": "<executive_summary>",
        "rating": <threat_severity_rating>,
        "rating_explanation": "<rating_explanation>"
        "findings": "[{{"summary":"<insight_1_summary>", "explanation": "<insight_1_explanation"}}, {{"summary":"<insight_2_summary>", "explanation": "<insight_2_explanation"}}]"
    }}

# 基准规则
每段文字后，如果内容来源于一个或多个数据记录，添加数据记录引用。引用格式为 [records: <record_source> (<record_id_list>, ...<record_source> (<record_id_list>)]。如果有超过10个数据记录，显示最相关的前10个记录。
每段应包含多句解释和包含具体命名实体的具体例子。所有段落必须在开头和结尾都有这些引用。如果没有相关角色或记录，则使用"NONE"。所有内容都应该是{language}。

例如，带有引用的段落：
这是一个带有引用的输出文本段落 [records: Entities (1, 2, 3), Claims (2, 5), Relationships (10, 12)]

# 示例输入
-----------
文本：

实体

id,实体,描述
5,ABILA CITY PARK,Abila City Park是POK集会的地点

关系

id,源,目标,描述
37,ABILA CITY PARK,POK RALLY,Abila City Park是POK集会的地点
38,ABILA CITY PARK,POK,POK在Abila City Park举行集会
39,ABILA CITY PARK,POKRALLY,POK集会在Abila City Park举行
40,ABILA CITY PARK,CENTRAL BULLETIN,Central Bulletin正在报道在Abila City Park举行的POK集会

输出：
{{
    "title": "Abila City Park和POK集会",
    "summary": "社区围绕Abila City Park，它是POK集会的地点。公园与POK, POKRALLY和Central Bulletin有关，都与集会事件相关联。",
    "rating": 5.0,
    "rating_explanation": "影响评级为中等，因为POK集会可能引起不安或冲突。",
    "findings": [
        {{
            "summary": "Abila City Park作为中心位置",
            "explanation": "Abila City Park是这个社区的核心实体，作为POK集会的地点。这个公园是所有其他实体之间的共同联系，表明了它在这个社区中的重要性。公园与集会的关联可能会导致如公共秩序问题或冲突，这取决于集会的性质及其引发的反应。 [records: Entities (5), Relationships (37, 38, 39, 40)]"
        }},
        ...
    ]
}}
# 真实数据

使用以下文本作为答案。在答案中不要编造任何内容。

文本：
{{input_text}}
输出:
"""

