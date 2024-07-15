# 导入模块中的两个东西，它们是用来总结描述信息的
from .description_summarize import SummarizeStrategyType, summarize_descriptions

# 这是一个版权声明，告诉我们这段代码是微软公司在2024年写的
# 并且它遵循MIT许可证的规定

# 这个是包的根目录，关于“解决实体”的一些内容
# "__"前导的名称在Python中通常是内部使用的，但这里是在说明这个包的主要内容

# 再次导入`description_summarize`模块中的`SummarizeStrategyType`和`summarize_descriptions`
# 这是为了让其他文件能更容易地使用这两个功能

# 这一行告诉Python，当我们从这个包里导入东西时，
# 可以直接用"SummarizeStrategyType"和"summarize_descriptions"，而不用写全路径
__all__ = ["SummarizeStrategyType", "summarize_descriptions"]

