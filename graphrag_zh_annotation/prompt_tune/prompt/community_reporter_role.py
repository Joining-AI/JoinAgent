# 这段代码的版权属于微软公司，2024年。
# 它遵循MIT许可证的规定

# 这个代码是用来生成社区记者角色定义的提示。

GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT = """
# 这里是一个故事角色，我们要帮助用户创建一个任务，让他们分析社区的情况。
# 看一下下面的例子，找出重要的部分，然后根据给定的领域和你的知识，创建一个新的角色定义。
# 记住，你的输出在结构和内容上应该和例子一样哦。

# 举个例子：
# 一个技术记者，他们要分析凯文·斯科特的"幕后科技播客"，给定一个社区成员列表，
# 包括他们之间的关系和可能的相关声明。这个报告会帮助决策者了解社区的重要进展
# 和它们可能带来的影响。

# 领域：{domain}       # 这里的{domain}会被替换为一个具体的领域，比如“科技”
# 文本：{input_text}   # 这里的{input_text}会被替换为一段需要分析的文字
# 角色：                # 在这里，你会写一个新的角色定义
"""

