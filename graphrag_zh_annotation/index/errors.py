# 这段代码的版权属于微软公司，2024年
# 并遵循MIT许可证，这是一个允许他人自由使用、修改和分享代码的许可协议。

# 这个文件定义了一些在处理GraphRAG（可能是一个图形数据结构）时可能出现的错误类型。

# 定义一个名为NoWorkflowsDefinedError的类，它是ValueError的子类
# 这个错误会在没有定义任何工作流时抛出

class NoWorkflowsDefinedError(ValueError):
    # 初始化这个错误类时
    def __init__(self):
        # 调用ValueError的初始化方法，并传入一条错误信息
        super().__init__("没有定义任何工作流。")


# 定义一个名为UndefinedWorkflowError的类，也是ValueError的子类
# 这个错误会在输入的工作流名称无效时抛出

class UndefinedWorkflowError(ValueError):
    # 初始化这个错误类时
    def __init__(self):
        # 调用ValueError的初始化方法，并传入一条错误信息
        super().__init__("工作流名称未定义。")


# 定义一个名为UnknownWorkflowError的类，同样是ValueError的子类
# 这个错误会在输入的工作流名称未知时抛出

class UnknownWorkflowError(ValueError):
    # 初始化这个错误类时，需要一个名为"name"的字符串参数
    def __init__(self, name: str):
        # 调用ValueError的初始化方法，并生成一条包含具体工作流名称的错误信息
        super().__init__(f"未知的工作流：{name}")

