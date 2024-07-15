# 这是代码的版权信息，表示2024年微软公司拥有此代码的版权。
# 它遵循MIT许可证，这是一种允许他人自由使用、修改和分享代码的许可协议。

# 这段文字是对这个代码文件的描述，它包含了一些清理和格式化JSON数据的工具函数。

def clean_up_json(json_str: str) -> str:
    """这个函数用来清理和格式化JSON字符串."""
    
    # 删除换行符和回车符，使JSON字符串整洁
    json_str = json_str.replace("\\n", "")   # 去掉反斜杠和'n'组成的转义字符
    json_str = json_str.replace("\n", "")   # 去掉普通换行符
    json_str = json_str.replace("\r", "")   # 去掉回车符
    
    # 修复可能影响JSON解析的引号和方括号
    json_str = json_str.replace('"[{', "[{")   # 如果左方括号前有双引号，去掉引号
    json_str = json_str.replace('}]"', "}]")   # 如果右方括号后有双引号，去掉引号
    json_str = json_str.replace("\\", "")   # 去掉所有的反斜杠
    
    # 去除多余的空格
    json_str = json_str.strip()   # 去掉字符串首尾的空白字符

    # 移除JSON Markdown格式的包围
    # 如果字符串以"

