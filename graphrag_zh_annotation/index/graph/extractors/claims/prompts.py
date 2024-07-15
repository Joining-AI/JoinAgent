# 这段代码是微软公司2024年的版权，遵循MIT许可证
# 它定义了一个文件，里面有关于如何提取特定信息的说明

# 这是一个字符串变量，用来描述一个任务
CLAIM_EXTRACTION_PROMPT = """
- 目标活动 -
你是一个智能助手，帮助人类分析员分析文本中关于某些实体的声明。

- 目标 -
给定一个可能相关的文本文档，一个实体规格和一个声明描述，提取所有匹配的实体和这些实体上的所有声明。

- 步骤 -
1. 提取所有符合预设实体规格的命名实体。实体规格可以是一些实体名称或实体类型。
2. 对于步骤1中找到的每个实体，提取与之相关的所有声明。声明需要匹配指定的声明描述，且实体应是声明的主体。
对于每个声明，提取以下信息：
- 主体：声明主体的名称，首字母大写。主体是执行声明中描述的行为的实体。主体必须是步骤1中识别出的命名实体之一。
- 客体：声明客体的名称，首字母大写。客体是报告/处理或受声明中行为影响的实体。如果客体未知，使用 **NONE**。
- 声明类型：声明的大类别，首字母大写。以可重复的方式命名，以便多个文本输入中的相似声明共享相同的声明类型。
- 声明状态：**TRUE**、**FALSE** 或 **SUSPECTED**。TRUE表示声明被确认，FALSE表示声明被发现是假的，SUSPECTED表示声明未经验证。
- 声明描述：详细解释声明理由的描述，包括所有相关证据和参考资料。
- 声明日期：声明发出的时间范围（开始日期，结束日期）。两个日期都应为ISO-8601格式。如果声明是在单一日期而不是日期范围内发出的，则两个日期相同。如果日期未知，返回 **NONE**。
- 声明来源文本：原始文本中与声明相关的所有引用列表。

每个声明的格式为 (<主体实体>{tuple_delimiter}<客体实体>{tuple_delimiter}<声明类型>{tuple_delimiter}<声明状态>{tuple_delimiter}<声明开始日期>{tuple_delimiter}<声明结束日期>{tuple_delimiter}<声明描述>{tuple_delimiter}<声明来源>)

3. 用英文将步骤1和2中识别的所有声明作为一个单独的列表返回。使用 **{record_delimiter}** 作为列表分隔符。

4. 结束时，输出 {completion_delimiter}

- 示例 -
示例1：
实体规格：组织
声明描述：与实体相关的红旗
文本：根据2022/01/10的一篇文章，公司A因在政府机构B发布的多个公共招标中串通投标而被罚款。该公司由C先生拥有，他在2015年涉嫌参与腐败活动。
输出：

(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}公司A因串通投标在多个公共招标中被罚款，因此被发现存在反竞争行为，根据2022/01/10发布的一篇文章{tuple_delimiter}根据2022/01/10发布的一篇文章，公司A因在多个公共招标中串通投标而被罚款，这些招标由政府机构B发布。)
{completion_delimiter}

示例2：
实体规格：公司A，C先生
声明描述：与实体相关的红旗
文本：根据2022/01/10的一篇文章，公司A因在政府机构B发布的多个公共招标中串通投标而被罚款。该公司由C先生拥有，他在2015年涉嫌参与腐败活动。
输出：

(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}公司A因串通投标在多个公共招标中被罚款，因此被发现存在反竞争行为，根据2022/01/10发布的一篇文章{tuple_delimiter}根据2022/01/10发布的一篇文章，公司A因在多个公共招标中串通投标而被罚款，这些招标由政府机构B发布。)
{record_delimiter}
(PERSON C{tuple_delimiter}NONE{tuple_delimiter}CORRUPTION{tuple_delimiter}SUSPECTED{tuple_delimiter}2015-01-01T00:00:00{tuple_delimiter}2015-12-30T00:00:00{tuple_delimiter}C先生在2015年涉嫌参与腐败活动{tuple_delimiter}该公司由C先生拥有，他涉嫌在2015年参与腐败活动)
{completion_delimiter}

- 实际数据 -
用以下输入为你提供答案。
实体规格：{entity_specs}
声明描述：{claim_description}
文本：{input_text}
输出:
"""

# 这是一个字符串变量，用于提示用户补充遗漏的实体
CONTINUE_PROMPT = "上一次提取中遗漏了很多实体。请使用相同格式添加它们：\n"

# 这是一个字符串变量，询问用户是否还有遗漏的实体需要添加
LOOP_PROMPT = "看起来可能还有一些实体被遗漏了。如果还有实体需要添加，请回答YES {tuple_delimiter} NO。\n"

