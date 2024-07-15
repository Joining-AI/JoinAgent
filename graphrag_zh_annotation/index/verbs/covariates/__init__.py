# 导入一个名为extract_covariates的函数，这个函数可能用来处理数据
from .extract_covariates import extract_covariates

# 这是版权声明，意思是2024年微软公司拥有这个代码的版权
# 并且这个代码遵循MIT许可证，允许他人在一定条件下使用和分享代码
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字是一个模块的描述，告诉我们这是关于"Indexing Engine"的
# "covariates"包的根目录，可能与数据分析有关
"""The Indexing Engine covariates package root."""

# 再次导入extract_covariates函数，这样其他文件可以通过这个包直接调用它
from .extract_covariates import extract_covariates

# 这个列表告诉别人这个包里可以公开使用的只有"extract_covariates"这个函数
__all__ = ["extract_covariates"]

