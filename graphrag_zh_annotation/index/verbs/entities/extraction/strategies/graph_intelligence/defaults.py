# 导入了一个叫做 LLMType 的枚举类型，它来自 graphrag.config.enums 模块
from graphrag.config.enums import LLMType

# 这是一个由微软公司2024年创建的代码，遵循MIT许可证
# 注释：这是一个包含一些默认响应的文件

# 再次导入了 LLMType，确保我们可以使用这个枚举类型
from graphrag.config.enums import LLMType

# 定义了一个列表，里面有一个很长的字符串。这个字符串包含了关于一些实体和关系的信息
MOCK_LLM_RESPONSES = [
    """
    （"实体"<|>"COMPANY_A"<|>"公司"<|>"Company_A 是一个测试公司")
    ##
    （"实体"<|>"COMPANY_B"<|>"公司"<|>"Company_B 拥有 Company_A，并且与 Company_A 有相同的地址）
    ##
    （"实体"<|>"PERSON_C"<|>"人"<|>"Person_C 是 Company_A 的董事）
    ##
    （"关系"<|>"COMPANY_A"<|>"COMPANY_B"<|>"因为 Company_A 被 Company_B 100%拥有并且两家公司地址相同，所以它们有关联"<|>2）
    ##
    （"关系"<|>"COMPANY_A"<|>"PERSON_C"<|>"因为 Person_C 是 Company_A 的董事，所以 Company_A 和 Person_C 有关联"<|>1））
    """.strip()  # 去掉字符串前后的空白字符
]

# 定义了一个字典，表示默认的 LLM（可能是某种语言模型）配置
# "type" 设置为 LLMType.StaticResponse，意味着使用静态响应
# "responses" 设置为我们之前定义的 MOCK_LLM_RESPONSES 列表
DEFAULT_LLM_CONFIG = {
    "type": LLMType.StaticResponse,
    "responses": MOCK_LLM_RESPONSES,
}

