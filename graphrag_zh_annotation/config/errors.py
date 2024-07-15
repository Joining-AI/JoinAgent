# 版权声明：这段代码由微软公司拥有，遵循MIT许可证
# 这段代码是关于默认配置时可能出现的错误的

# 定义一个类，表示缺少LLM（可能是Large Language Model）密钥的错误
class ApiKeyMissingError(ValueError):
    # 初始化方法，用于创建对象
    def __init__(self, 是否嵌入: bool = False) -> None:
        # 如果"是否嵌入"为真，API类型是"Embedding"，否则是"Completion"
        api_type = "Embedding" if 是否嵌入 else "Completion"
        # 根据API类型，设置对应的密钥环境变量名
        api_key = "GRAPHRAG_EMBEDDING_API_KEY" if 是否嵌入 else "GRAPHRAG_LLM_API_KEY"
        # 错误信息：需要API密钥才能使用指定类型的API
        msg = f"API Key是{api_type} API所需的。请设置OPENAI_API_KEY, GRAPHRAG_API_KEY或{api_key}环境变量。"
        # 调用父类（ValueError）的初始化方法，传入错误信息
        super().__init__(msg)

# 定义一个类，表示缺少Azure API基础地址的错误
class AzureApiBaseMissingError(ValueError):
    # 初始化方法
    def __init__(self, 是否嵌入: bool = False) -> None:
        # 类似于上一个类，确定API类型和对应的API基础地址环境变量名
        api_type = "Embedding" if 是否嵌入 else "Completion"
        api_base = "GRAPHRAG_EMBEDDING_API_BASE" if 是否嵌入 else "GRAPHRAG_API_BASE"
        # 错误信息：需要API基础地址才能使用指定类型的API
        msg = f"API Base是{api_type} API所需的。请设置OPENAI_API_BASE, GRAPHRAG_API_BASE或{api_base}环境变量。"
        # 调用父类的初始化方法
        super().__init__(msg)

# 定义一个类，表示缺少Azure部署名称的错误
class AzureDeploymentNameMissingError(ValueError):
    # 初始化方法
    def __init__(self, 是否嵌入: bool = False) -> None:
        # 确定API类型和对应的部署名称环境变量名
        api_type = "Embedding" if 是否嵌入 else "Completion"
        api_base = (
            "GRAPHRAG_EMBEDDING_DEPLOYMENT_NAME"
            if 是否嵌入
            else "GRAPHRAG_LLM_DEPLOYMENT_NAME"
        )
        # 错误信息：需要部署名称才能使用指定类型的API
        msg = f"Deployment Name是{api_type} API所需的。请设置OPENAI_DEPLOYMENT_NAME, GRAPHRAG_LLM_DEPLOYMENT_NAME或{api_base}环境变量。"
        # 调用父类的初始化方法
        super().__init__(msg)

