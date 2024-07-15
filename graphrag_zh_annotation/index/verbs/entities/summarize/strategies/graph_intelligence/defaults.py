# 导入一个叫做 LLMType 的枚举类型，它来自 graphrag.config.enums 模块
from graphrag.config.enums import LLMType

# 这是一个版权声明，告诉我们这段代码是微软公司在2024年写的
# 并且它遵循 MIT 许可证的规则
# 注：MIT 许可证是一种允许他人自由使用、复制和修改软件的许可协议

# 这个文件里有一些默认的回复信息
# 我们来定义一些假的 LLM（可能是“语言模型”）响应
# 这些响应是为了演示或者测试用的

# 创建一个列表，里面有一个字符串，这个字符串是一个模拟的 LLM 响应，它已经被总结过了
MOCK_LLM_RESPONSES = [
    """
    这是一个模拟的 LLM 响应。它已经被简化了！
    """.strip()  # strip() 函数用于去掉字符串开头和结尾的空白字符
]

# 定义一个字典，表示 LLM 的默认配置
# 字典里有两个键值对：
# - "type"：它的值是 LLMType.StaticResponse，可能表示 LLM 的响应方式是静态的
# - "responses"：它的值是上面创建的模拟响应列表
DEFAULT_LLM_CONFIG = {
    "type": LLMType.StaticResponse,
    "responses": MOCK_LLM_RESPONSES,
}

