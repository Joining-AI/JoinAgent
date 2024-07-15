# 导入warnings模块，它帮助我们处理程序运行时的警告信息
import warnings

# 这是一个版权声明，表示这段代码归微软公司所有，2024年
# 并且遵循MIT许可证的规定
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，叫做"Bootstrap定义"
"""Bootstrap definition."""

# 使用warnings模块忽略numba库产生的特定警告
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")  # 忽略与'nopython'关键词相关的警告
warnings.filterwarnings("ignore", message=".*Use no seed for parallelism.*")  # 忽略关于并行计算种子使用的警告

# 定义一个全局变量，初始值为False，表示nltk库是否已经初始化
initialized_nltk = False


# 定义一个名为bootstrap的函数，它的作用是初始化一些东西
def bootstrap():
    """Bootstrap定义。"""
    # 使用全局变量initialized_nltk
    global initialized_nltk
    # 如果initialized_nltk为False，说明nltk库还没有初始化
    if not initialized_nltk:
        # 导入nltk库
        import nltk
        # 从nltk库中导入wordnet模块
        from nltk.corpus import wordnet as wn

        # 下面这几句代码是下载nltk库需要的一些数据包
        nltk.download("punkt")  # 下载分词工具
        nltk.download("averaged_perceptron_tagger")  # 下载词性标注器
        nltk.download("maxent_ne_chunker")  # 下载命名实体识别器
        nltk.download("words")  # 下载常见英文单词列表
        nltk.download("wordnet")  # 下载WordNet词汇数据库
        # 加载wordnet的数据，确保可以使用
        wn.ensure_loaded()
        # 设置initialized_nltk为True，表示nltk库已经初始化过了
        initialized_nltk = True

