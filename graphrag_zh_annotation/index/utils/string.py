# 导入一些有用的库
import html  # 这个库能帮助我们处理HTML字符
import re    # 这个库用于正则表达式，可以用来查找和替换字符串中的模式
from typing import Any  # 这个是类型提示，表示函数可以接收任何类型的输入

# 这里是版权声明，告诉我们这段代码由微软公司编写，并遵循MIT许可证

# 这是一个关于字符串的工具模块的文档说明
"""字符串处理的工具函数。"""

# 继续导入库
import html
import re
from typing import Any

# 定义一个名为clean_str的函数，它接收一个参数input，并返回一个字符串
def clean_str(input: Any) -> str:
    # 如果输入的不是字符串，就直接返回它
    if not isinstance(input, str):
        return input

    # 先去除输入字符串两边的空白，并解开HTML转义字符
    result = html.unescape(input.strip())

    # 使用正则表达式移除所有控制字符（这些字符在屏幕上通常是不可见的）
    # 这个链接（https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python）提供了这个方法
    return re.sub(r"[\x00-\x1f\x7f-\x9f]", "", result)

