# 这段代码是微软公司写的，用于OpenAI DataShaper包中的错误定义
# 注释里的 "Copyright (c) 2024 Microsoft Corporation." 表示版权信息
# "Licensed under the MIT License" 表示这个代码使用MIT许可证授权

# 这是一个文档字符串，描述了这个代码段的功能，它是关于数据塑形包中错误的定义

# 定义了一个名为RetriesExhaustedError的类，它继承自RuntimeError
class RetriesExhaustedError(RuntimeError):
    # RetriesExhaustedError类的说明：当尝试次数用完时会抛出此错误

    # 这是初始化方法，当创建一个新的RetriesExhaustedError对象时会调用
    def __init__(self, name: str, num_retries: int) -> None:
        # 调用父类（即RuntimeError）的初始化方法
        super().__init__(
            # 使用f-string创建错误消息，其中'{name}'是操作名称，'{num_retries}'是尝试次数
            f"Operation '{name}' failed - {num_retries} retries exhausted"
        )

