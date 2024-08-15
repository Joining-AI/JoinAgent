# 这段代码的版权属于微软公司，2024年
# 使用的是MIT许可证，这是一种允许他人自由使用、修改和分享代码的许可协议。

# 这个程序是用来生成领域分类提示的。

GENERATE_DOMAIN_PROMPT = """
# 你是一个聪明的助手，你的工作是帮助人们理解文本中的信息。
# 当给定一段文字时，你的任务是为这段文字分配一个描述性的领域标签，用来概括文本的主要内容。
# 例如，可能的领域有：“社会学”，“算法分析”，“医学科学”等。

# 这里是一个例子：
# 文本：{input_text}
# 领域：
"""
