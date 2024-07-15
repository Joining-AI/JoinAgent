# 这个代码是一个Python文件，定义了一些提示信息。
# 它是微软公司2024年的版权，并遵循MIT许可证。

# 文件的注释描述了一个包含提示定义的文件。
"""这是一个包含提示定义的文件。"""

# 定义了一个变量COMMUNITY_REPORT_PROMPT，它是一个很长的字符串，包含了生成社区报告的说明。
COMMUNITY_REPORT_PROMPT = """
你是一个AI助手，帮助人类分析师进行一般信息发现。信息发现是识别和评估与网络中的某些实体（如组织和个人）相关的信息的过程。

# 目标
根据社区内的实体列表以及它们的关系和可选的关联声明，编写一份全面的报告。该报告将用于向决策者提供有关社区及其潜在影响的相关信息。报告内容包括社区关键实体的概述、它们的法律合规性、技术能力、声誉以及值得注意的声明。

# 报告结构

报告应包括以下部分：

- 标题：代表其关键实体的社区名称 - 标题应简洁但具体。如果可能，将代表性命名实体包含在标题中。
- 摘要：社区总体结构的执行摘要，其实体之间的关系，以及与其实体相关的重大信息。
- 影响严重性评分：0到10之间的浮点数，表示社区内实体产生的影响严重程度。影响是社区得分的重要程度。
- 评分解释：用一句话解释影响严重性评分。
- 详细发现：关于社区的5到10个关键见解。每个见解都应有一个简短的总结，后面跟着多段根据以下规则解释的文本。要全面。

返回格式良好的JSON格式字符串，如下所示：
    {{
        "title": <报告标题>,
        "summary": <执行摘要>,
        "rating": <影响严重性评分>,
        "rating_explanation": <评分解释>,
        "findings": [
            {{
                "summary":<见解1总结>,
                "explanation": <见解1解释>
            }},
            {{
                "summary":<见解2总结>,
                "explanation": <见解2解释>
            }}
        ]
    }}

# 规则

由数据支持的观点应列出数据引用，如下所示：

"这是一个由多个数据参考支持的示例句子 [Data: <数据集名称>（记录ID）; <数据集名称>（记录ID）]。"

单个引用中不要列出超过5个记录ID。相反，列出最相关的前5个记录ID，并添加“+more”以表示还有更多。

例如：
"Person X是Company Y的所有者，并受到许多不当行为的指控 [Data: Reports (1), Entities (5, 7); Relationships (23); Claims (7, 2, 34, 64, 46, +more)]。"

其中1, 5, 7, 23, 2, 34, 46和64代表相关数据记录的ID（不是索引）。

不要包含没有支持证据的信息。

# 示例输入
-----------
文本：

实体

id,实体,描述
5,VERDANT OASIS PLAZA,Verdant Oasis Plaza是Unity March的地点
6,HARMONY ASSEMBLY,Harmony Assembly是在Verdant Oasis Plaza举行游行的组织

关系

id,源,目标,描述
37,VERDANT OASIS PLAZA,UNITY MARCH,Verdant Oasis Plaza是Unity March的地点
38,VERDANT OASIS PLAZA,HARMONY ASSEMBLY,Harmony Assembly在Verdant Oasis Plaza举行游行
39,VERDANT OASIS PLAZA,UNITY MARCH,Unity March在Verdant Oasis Plaza举行
40,VERDANT OASIS PLAZA,TRIBUNE SPOTLIGHT,Tribune Spotlight正在报道在Verdant Oasis Plaza举行的Unity游行
41,VERDANT OASIS PLAZA,BAILEY ASADI,Bailey Asadi在Verdant Oasis Plaza谈论游行
43,HARMONY ASSEMBLY,UNITY MARCH,Harmony Assembly正在组织Unity March

输出：
{{
    "title": "Verdant Oasis Plaza和Unity March",
    "summary": "社区围绕Verdant Oasis Plaza展开，它是Unity March的地点。该广场与Harmony Assembly、Unity March和Tribune Spotlight有关，所有这些都与游行事件相关联。",
    "rating": 5.0,
    "rating_explanation": "影响严重性评分为中等，因为Unity March期间可能存在动乱或冲突的风险。",
    "findings": [
        {{
            "summary": "Verdant Oasis Plaza作为中心位置",
            "explanation": "Verdant Oasis Plaza是这个社区的核心实体，作为Unity March的地点。这个广场是所有其他实体的共同联系，表明其在社区中的重要性。广场与游行的关联可能导致如公共秩序混乱或冲突等问题，取决于游行的性质和引发的反应。[Data: Entities (5), Relationships (37, 38, 39, 40, 41,+more)]"
        }},
        {{
            "summary": "Harmony Assembly在社区中的角色",
            "explanation": "Harmony Assembly是这个社区的另一个关键实体，是Verdant Oasis Plaza游行的组织者。Harmony Assembly及其游行的性质可能是潜在的威胁来源，取决于他们的目标和引发的反应。Harmony Assembly与广场的关系对于理解这个社区的动态至关重要。[Data: Entities(6), Relationships (38, 43)]"
        }},
        {{
            "summary": "Unity March作为重大事件",
            "explanation": "Unity March是在Verdant Oasis Plaza举行的重大事件。这个事件是社区动态的关键因素，可能是潜在的威胁来源，取决于游行的性质和引发的反应。游行与广场的关系对于理解社区动态至关重要。[Data: Relationships (39)]"
        }},
        {{
            "summary": "Tribune Spotlight的角色",
            "explanation": "Tribune Spotlight正在报道在Verdant Oasis Plaza举行的Unity March。这表明该事件吸引了媒体关注，可能会放大其对社区的影响。Tribune Spotlight的作用可能在塑造公众对事件和涉及实体的看法方面具有重要意义。[Data: Relationships (40)]"
        }}
    ]
}}


# 真实数据

在你的答案中使用以下文本。不要在你的答案中编造任何内容。

文本：
{input_text}

报告应包括以下部分：

- 标题：代表其关键实体的社区名称 - 标题应简洁但具体。如果可能，将代表性命名实体包含在标题中。
- 摘要：社区总体结构的执行摘要，其实体之间的关系，以及与其实体相关的重大信息。
- 影响严重性评分：0到10之间的浮点数，表示社区内实体产生的影响严重程度。影响是社区得分的重要程度。
- 评分解释：用一句话解释影响严重性评分。
- 详细发现：关于社区的5到10个关键见解。每个见解都应有一个简短的总结，后面跟着多段根据以下规则解释的文本。要全面。

返回格式良好的JSON格式字符串，如下所示：
    {{
        "title": <报告标题>,
        "summary": <执行摘要>,
        "rating": <影响严重性评分>,
        "rating_explanation": <评分解释>,
        "findings": [
            {{
                "summary":<见解1总结>,
                "explanation": <见解1解释>
            }},
            {{
                "summary":<见解2总结>,
                "explanation": <见解2解释>
            }}
        ]
    }}

# 规则

由数据支持的观点应列出数据引用，如下所示：

"这是一个由多个数据参考支持的示例句子 [Data: <数据集名称>（记录ID）; <数据集名称>（记录ID）]。"

单个引用中不要列出超过5个记录ID。相反，列出最相关的前5个记录ID，并添加“+more”以表示还有更多。

例如：
"Person X是Company Y的所有者，并受到许多不当行为的指控 [Data: Reports (1), Entities (5, 7); Relationships (23); Claims (7, 2, 34, 64, 46, +more)]。"

其中1, 5, 7, 23, 2, 34, 46和64代表相关数据记录的ID（不是索引）。

不要包含没有支持证据的信息。

输出:
"""

