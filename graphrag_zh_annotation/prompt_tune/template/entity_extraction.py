# 这段代码是微软公司的一个程序，使用的是MIT许可证
# 它是用来训练一个提取文本中实体和关系的程序

# 这是一个定义，用于实体提取的提示
GRAPH_EXTRACTION_PROMPT = """
-目标-
给定一个可能与这个活动相关的文本和一个实体类型列表，找出文本中的所有这些类型的实体以及它们之间的所有关系。

-步骤-
1. 找出所有实体。对每个找到的实体，提取以下信息：
   - 实体名称：首字母大写的实体名字
   - 实体类型：以下类型之一：[{entity_types}]
   - 实体描述：关于实体属性和活动的详细描述
   格式化每个实体为 ("entity"{{tuple_delimiter}}<entity_name>{{tuple_delimiter}}<entity_type>{{tuple_delimiter}}<entity_description>

2. 从步骤1中找出的实体中，找出所有明显相互关联的（源实体，目标实体）对。
   对于每对相关实体，提取以下信息：
   - 源实体：步骤1中识别出的源实体的名字
   - 目标实体：步骤1中识别出的目标实体的名字
   - 关系描述：解释为什么你认为源实体和目标实体之间有关联
   - 关系强度：1到10之间的整数，表示源实体和目标实体之间关系的强度

   格式化每个关系为 ("relationship"{{tuple_delimiter}}<source_entity>{{tuple_delimiter}}<target_entity>{{tuple_delimiter}}<relationship_description>{{tuple_delimiter}}<relationship_strength>)

3. 将步骤1和2中识别的所有实体和关系以{language}语言作为单个列表返回。用**{{record_delimiter}}**作为列表分隔符。如果需要翻译，只翻译描述，其他不要变！

4. 完成后，输出 {{completion_delimiter}}

-例子-
######################
{examples}

-真实数据-
######################
entity_types: [{entity_types}]
text: {{input_text}}
######################
输出: ""
"""

# 这是一个JSON格式的实体提取提示
GRAPH_EXTRACTION_JSON_PROMPT = """
-目标-
给定一个可能与这个活动相关的文本和一个实体类型列表，找出文本中的所有这些类型的实体以及它们之间的所有关系。

-步骤-
1. 找出所有实体。对每个找到的实体，提取以下信息：
   - 实体名称：首字母大写的实体名字
   - 实体类型：以下类型之一：[{entity_types}]
   - 实体描述：关于实体属性和活动的详细描述
   格式化每个实体输出为一个JSON条目，如下所示：

   {"name": <实体名>, "type": <类型>, "description": <实体描述>}

2. 从步骤1中找出的实体中，找出所有明显相互关联的（源实体，目标实体）对。
   对于每对相关实体，提取以下信息：
   - 源实体：步骤1中识别出的源实体的名字
   - 目标实体：步骤1中识别出的目标实体的名字
   - 关系描述：解释为什么你认为源实体和目标实体之间有关联
   - 关系强度：1到10之间的整数，表示源实体和目标实体之间关系的强度
   格式化每个关系为一个JSON条目，如下所示：

   {"source": <源实体>, "target": <目标实体>, "relationship": <关系描述>, "relationship_strength": <关系强度>}

3. 将步骤1和2中识别的所有JSON实体和关系以{language}语言作为单个列表返回。如果需要翻译，只翻译描述，其他不要变！

-例子-
######################
{examples}

-真实数据-
######################
entity_types: {entity_types}
text: {{input_text}}
######################
输出: ""
"""

# 这是一个用于示例的模板
EXAMPLE_EXTRACTION_TEMPLATE = """
示例 {n}：

实体类型: [{entity_types}]
文本:
{input_text}
------------------------
输出:
{output}
#############################

"""

# 这是一个没有指定类型示例的模板
UNTYPED_EXAMPLE_EXTRACTION_TEMPLATE = """
示例 {n}：

文本:
{input_text}
------------------------
输出:
{output}
#############################

"""

# 这是一个未分类实体提取提示
UNTYPED_GRAPH_EXTRACTION_PROMPT = """
-目标-
给定一个可能与这个活动相关的文本，首先找出文本中所有需要的实体以便捕捉文本中的信息和想法。
然后报告所有识别出的实体之间的关系。

-步骤-
1. 找出所有实体。对每个找到的实体，提取以下信息：
   - 实体名称：首字母大写的实体名字
   - 实体类型：为实体建议几个标签或类别。类别不应具体，而应尽可能通用。
   - 实体描述：关于实体属性和活动的详细描述
   格式化每个实体为 ("entity"{{tuple_delimiter}}<entity_name>{{tuple_delimiter}}<entity_type>{{tuple_delimiter}}<entity_description>

2. 从步骤1中找出的实体中，找出所有明显相互关联的（源实体，目标实体）对。
   对于每对相关实体，提取以下信息：
   - 源实体：步骤1中识别出的源实体的名字
   - 目标实体：步骤1中识别出的目标实体的名字
   - 关系描述：解释为什么你认为源实体和目标实体之间有关联
   - 关系强度：表示源实体和目标实体之间关系强度的数字分数
   格式化每个关系为 ("relationship"{{tuple_delimiter}}<source_entity>{{tuple_delimiter}}<target_entity>{{tuple_delimiter}}<relationship_description>{{tuple_delimiter}}<relationship_strength>)

3. 将步骤1和2中识别的所有实体和关系以{language}语言作为单个列表返回。用**{{record_delimiter}}**作为列表分隔符。如果需要翻译，只翻译描述，其他不要变！

4. 完成后，输出 {{completion_delimiter}}

-例子-
######################
{examples}

-真实数据-
######################
文本: {{input_text}}
######################
输出:
"""

