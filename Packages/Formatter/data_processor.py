class DataProcessor:
    def __init__(self):
        pass

    def transform_tuple_list(self, data):
        """
        将嵌套的字符串列表转换为包含元组的列表，每个元组包含一个字符串及其索引。

        参数:
        data (list of tuple): 输入的嵌套字符串列表及索引的元组列表。

        返回:
        list of tuple: 包含元组的列表，每个元组是 (string, index)。
        """
        transformed_data = []
        for string_list, index in data:
            for string in string_list:
                transformed_data.append((string, index))
        return transformed_data

    def string2tuple_list(self, string_list):
        """
        将字符串列表转换为包含元组的列表，每个元组包含一个字符串及其索引。

        参数:
        string_list (list of str): 输入的字符串列表。

        返回:
        list of tuple: 包含元组的列表，每个元组是 (string, index)。
        """
        tuple_list = [(string, index) for index, string in enumerate(string_list)]
        return tuple_list

    def tuple2string_list(self, tuple_list):
        """
        将包含元组的列表转换为字符串列表，每个元组包含一个字符串及其索引。

        参数:
        tuple_list (list of tuple): 输入的包含元组的列表，每个元组是 (string, index)。

        返回:
        list of str: 字符串列表。
        """
        string_list = [item[0] for item in tuple_list]
        return string_list

    def update_tuple_list(self, tuple_list, synonyms):
        """
        更新包含元组的列表，将每个字符串替换为其主词并避免重复。

        参数:
        tuple_list (list of tuple): 输入的包含元组的列表，每个元组是 (string, index)。
        synonyms (dict): 包含主词和相似词的字典。

        返回:
        list of tuple: 更新后的包含元组的列表，每个元组是 (main_word, index)。
        """
        # 创建一个映射，将每个类似词指向它的main_word
        synonym_map = {}
        for main_word, similar_dict in synonyms.items():
            synonym_map[main_word] = main_word  # 主词也需要指向自己
            for similar_word in similar_dict['Similar_keys']:
                synonym_map[similar_word] = main_word

        # 更新tuple_list中的字符串，并避免重复
        updated_tuple_list = []
        seen = set()  # 用于跟踪已经添加的元素
        for string, index in tuple_list:
            main_word = synonym_map.get(string, string)
            element = (main_word, index)
            if element not in seen:
                updated_tuple_list.append(element)
                seen.add(element)
        
        return updated_tuple_list

    def convertor(self, embedder, tuple_list):
        temp_type_list=self.transform_tuple_list(tuple_list)

        type_list=self.tuple2string_list(temp_type_list)

        embedded_type_list=embedder.embed_list(type_list)

        synonyms=embedder.partition_by_similarity(embedded_type_list)

        updated_type_list=self.update_tuple_list(temp_type_list, synonyms)
        
        return updated_type_list
    
    def organize_data(self, type_data, entity_data):
        # 初始化一个字典，用于存储按 index 分组的数据
        organized_data = {}

        # 处理 type_data
        for type_string, index in type_data:
            if index not in organized_data:
                organized_data[index] = {'type_list': [], 'entity_list': []}
            organized_data[index]['type_list'].append(type_string)

        # 处理 entity_data
        for entity_string, index in entity_data:
            if index not in organized_data:
                organized_data[index] = {'type_list': [], 'entity_list': []}
            organized_data[index]['entity_list'].append(entity_string)

        # 将字典转换为列表形式，包含 (type_list, entity_list, index) 的元组
        result = [(data['type_list'], data['entity_list'], index) for index, data in organized_data.items()]

        return result
    
    def convert_structure(self, data):
        result = {}

        for item_list, index in data:
            for item in item_list:
                name = item['名称']
                explanation = item['解释']
                if name not in result:
                    result[name] = []
                result[name].append((explanation, index))

        return result