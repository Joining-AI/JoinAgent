# 版权声明：这段代码归2024年微软公司所有。
# 许可证：遵循MIT许可证的规定

# 这是一段用于处理低级LLM（大语言模型）调用的实用程序提示。

JSON_CHECK_PROMPT = """
# 说明：
# 你将看到一个格式错误的JSON字符串，它在尝试用json.loads解析时出错了。
# 可能是它有不必要的转义字符，或者在某个地方缺少逗号或冒号。
# 你的任务是修复这个字符串，返回一个格式正确的JSON字符串，里面只有一个对象。
# 去掉任何不必要的转义字符。
# 只返回可以被json.loads解析的有效JSON，不要包含额外的说明文字。

# 示例：
# -------------
# 输入：{{ \\"title\\": \\"abc\\", \\"summary\\": \\"def\\" }}
# 输出：{{"title": "abc", "summary": "def"}}
# -------------
# 输入：{{"title": "abc", "summary": "def"
# 输出：{{"title": "abc", "summary": "def"}}
# -------------
# 输入：{{"title': "abc", 'summary": "def"}
# 输出：{{"title": "abc", "summary": "def"}}
# -------------
# 输入：{{"title": "abc", "summary": "def"}}"
# 输出：{{"title": "abc", "summary": "def"}}
# -------------
# 输入：[{{"title": "abc", "summary": "def"}}]
# 输出：[{{"title": "abc", "summary": "def"}}]
# -------------
# 输入：[{{"title": "abc", "summary": "def"}}, {{ \\"title\\": \\"abc\\", \\"summary\\": \\"def\\" }}]
# 输出：[{{"title": "abc", "summary": "def"}}, {{"title": "abc", "summary": "def"}}]
# -------------
# 输入：

