# 这段代码的版权属于微软公司，2024年
# 并且遵循MIT许可证

# 这是一个关于清理和格式化JSON数据的工具模块

def clean_up_json(json_str: str):
    """这个函数用来清理JSON字符串，使其更整洁"""
    
    # 删除换行符和回车符
    json_str = json_str.replace("\\n", "")  # 去掉反斜杠和'n'
    json_str = json_str.replace("\n", "")   # 去掉普通换行符
    json_str = json_str.replace("\r", "")   # 去掉回车符

    # 修复可能的括号错误
    json_str = json_str.replace('"[{', "[{")  # 把'"['替换为'['
    json_str = json_str.replace('}"]', "}]")  # 把'}"'替换为']'

    # 删除多余的反斜杠
    json_str = json_str.replace("\\", "")   # 去掉所有的反斜杠

    # 去除两端的空白字符
    json_str = json_str.strip()             # 删除字符串前后的空白

    # 移除JSON的Markdown格式框架
    # 如果字符串以"

