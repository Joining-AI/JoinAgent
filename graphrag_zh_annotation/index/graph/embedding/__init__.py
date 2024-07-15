# 导入模块，这部分是让Python程序能用到其他文件里的工具
from .embedding import NodeEmbeddings, embed_nod2vec
# 这是一个版权声明，说明代码由微软公司创作，2024年时有效
# 并且这个代码遵循MIT许可证的规定

# 这个是文档字符串，用来描述这个包是做什么的
"""这是一个关于图嵌入的索引引擎包的根目录。"""

# 再次导入`embedding`模块中的`NodeEmbeddings`和`embed_nod2vec`
from .embedding import NodeEmbeddings, embed_nod2vec

# 这一行告诉其他程序，这个文件里可以公开使用的工具有哪些
# 这里是可以被外部访问的两个工具：NodeEmbeddings和embed_nod2vec
__all__ = ["NodeEmbeddings", "embed_nod2vec"]

