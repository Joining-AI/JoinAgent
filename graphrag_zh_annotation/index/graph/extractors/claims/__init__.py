# 导入名为ClaimExtractor的工具，它能帮助我们找出重要的信息（声明）
from .claim_extractor import ClaimExtractor

# 导入CLAIM_EXTRACTION_PROMPT，这是一个提示，可能用于询问如何提取声明
from .prompts import CLAIM_EXTRACTION_PROMPT

# 这是微软公司在2024年的版权信息
# 许可证是MIT License，意味着你可以自由使用，但需要遵守一些规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件是关于索引引擎图形提取器中处理声明的包的根目录
# "The Indexing Engine graph extractors claims package root."

# 再次导入ClaimExtractor和CLAIM_EXTRACTION_PROMPT
# 这是为了确保其他部分的代码可以轻松地使用这两个工具
from .claim_extractor import ClaimExtractor
from .prompts import CLAIM_EXTRACTION_PROMPT

# 这行代码告诉其他程序，这个包里可以公开使用的有两个东西：CLAIM_EXTRACTION_PROMPT和ClaimExtractor
__all__ = ["CLAIM_EXTRACTION_PROMPT", "ClaimExtractor"]

