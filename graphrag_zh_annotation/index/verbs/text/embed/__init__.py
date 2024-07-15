# 导入.text_embed模块中的TextEmbedStrategyType和text_embed函数
from .text_embed import TextEmbedStrategyType, text_embed

# 这是一个版权声明，表示代码由2024年的微软公司所有
# 并且代码遵循MIT许可证的规定，允许他人在一定条件下使用

# 这个文件是Indexing Engine文本嵌入包的根目录

# 再次从.text_embed导入TextEmbedStrategyType和text_embed
from .text_embed import TextEmbedStrategyType, text_embed

# 这一行告诉Python，当其他地方导入这个包时，
# 可以直接使用"TextEmbedStrategyType"和"text_embed"这两个名字
__all__ = ["TextEmbedStrategyType", "text_embed"]

