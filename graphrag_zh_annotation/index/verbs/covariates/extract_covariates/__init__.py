# 导入模块中的两个元素：ExtractClaimsStrategyType 和 extract_covariates
from .extract_covariates import ExtractClaimsStrategyType, extract_covariates

# 这是一个版权声明，意味着这个代码由微软公司创作，2024年版权有效。
# 它是根据MIT许可证授权的，这意味着你可以自由使用，但需要遵守一些规定。

# 这个文件是Indexing Engine文本提取索赔包的根目录的文档字符串。
# 文档字符串是解释代码用途的一段文字，当别人查看这个模块时会看到。

from .extract_covariates import ExtractClaimsStrategyType, extract_covariates

# 这行代码再次导入了上面已经导入的两个元素，确保它们在本文件中可以被直接使用。

# 这是一个特殊列表，声明了这个模块对外提供的公共接口，也就是其他程序可以使用的功能。
# 这里列出的是"ExtractClaimsStrategyType"和"extract_covariates"。
__all__ = ["ExtractClaimsStrategyType", "extract_covariates"]

