# 这段代码的版权属于微软公司，2024年
# 使用的是MIT许可协议

# 这个文件是用来定义一些提示（prompt）的

# 定义了一个变量，叫做SUMMARIZE_PROMPT，它是一个很长的字符串
SUMMARIZE_PROMPT = """
# 你是一个帮手，你的工作是把下面的数据总结成一段全面的描述
# 当给出一个或两个实体（比如人、地方或事物），和关于这些实体的一系列描述时
# 你要把这些描述合并成一个单独的、全面的句子。确保包含所有描述中的信息。
# 如果描述中有矛盾的地方，你需要解决矛盾，给出一个连贯的总结。
# 记住要用第三人称来写，并且要包括实体的名字，这样我们才能了解全部上下文。

# ---------------
# - 数据 -
# 实体名：{entity_name}
# 描述列表：{description_list}
# ---------------
# 输出：
"""

