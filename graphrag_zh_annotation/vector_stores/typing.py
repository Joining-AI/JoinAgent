

# 这是一个叫做VectorStoreFactory的类，它的任务是帮助我们创建不同类型的向量存储。
class VectorStoreFactory:
    """这是一个创建向量存储的工厂类，向量存储是用来保存数据的。"""

    # 这个变量像一个字典，保存了所有我们知道的向量存储类型。
    vector_store_types: ClassVar[dict[str, type]] = {}

    # 这个函数是个特殊的方法，它可以让其他类用它来添加新的向量存储类型。
    @classmethod
    def register(cls, vector_store_type: str, vector_store: type):
        """这个方法用来登记新的向量存储类型。"""
        # 把新类型的存储加到我们的字典里。
        cls.vector_store_types[vector_store_type] = vector_store

    # 这个方法也是个特殊函数，它会根据给定的信息创建一个向量存储的实例。
    @classmethod
    def get_vector_store(
        cls, vector_store_type: VectorStoreType | str, kwargs: dict
    ) -> LanceDBVectorStore | AzureAISearch:
        """根据名字获取一个向量存储实例。"""
        # Python的match语句像个开关，检查我们要哪种类型的存储。
        match vector_store_type:
            case VectorStoreType.LanceDB:  # 如果要LanceDB类型的
                # 那就创建一个LanceDBVectorStore的实例。
                return LanceDBVectorStore(**kwargs)
            case VectorStoreType.AzureAISearch:  # 如果要Azure AI搜索类型的
                # 那就创建一个AzureAISearch的实例。
                return AzureAISearch(**kwargs)
            case _:  # 如果我们没见过的类型
                # 如果这个类型在我们的字典里，我们就用它创建一个实例。
                if vector_store_type in cls.vector_store_types:
                    return cls.vector_store_types[vector_store_type](**kwargs)
                # 如果我们既不认识，字典里也没有，就告诉用户我们不知道这个类型。
                msg = f"未知的向量存储类型：{vector_store_type}"
                raise ValueError(msg)  # 抛出错误信息

