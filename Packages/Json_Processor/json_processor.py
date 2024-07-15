import json
import ast
import re

class JSProcessor:
    def __init__(self):
        self.analysed_data={}
        self.analysed_list=[]
        self.json=None
        self.prompt=''

    def generate_structure(self,level, words='词', current_level=1, is_first_call=True):
        # 定义层级对应的名称
        def level_name(lv, words=words):
            prefix = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
            level_words = "级"+ words
            return prefix[lv - 1] + level_words if lv - 1 < len(prefix) else str(lv) + level_words
        
        indent = "    " * (current_level - 1)  # 根据当前层级确定缩进
        newline = "\n"
        
        # 如果是最子级的知识点，直接返回空结构体
        if current_level > level:
            return "{}"
        
        # 生成当前层级的知识点结构
        current_level_str = level_name(current_level)
        structure = ''
        if current_level == level - 1:  # 如果是倒数第二层，直接生成两个最子级知识点
            structure = ',\n'.join([f'{indent}    "{current_level_str}{i + 1}": {{}}' for i in range(2)]) + ', ...'
        else:  # 对于非倒数第二层，递归生成下一层
            next_level_str = self.generate_structure(level, words=words, current_level=current_level + 1, is_first_call=False)
            # 根据是否是首次调用，决定生成一个还是两个知识点
            points_to_generate = 1 if not is_first_call and current_level != 1 else 2
            structure = ',\n'.join([f'{indent}    "{current_level_str}{i + 1}": {next_level_str}' for i in range(points_to_generate)])
            if current_level == 1 or not is_first_call or current_level != level - 1:
                structure += ', ...'
        
        # 对于第一层知识点，模拟省略号的效果
        if current_level == 1 and is_first_call:
            structure += '\n...'

        return f"{{\n{structure}\n{indent}}}"

    def generate_prompt(self, level, pre_prompt, pro_prompt, words):
        prompt = pre_prompt + self.generate_structure(level, words=words) + pro_prompt
        return prompt

    def parse_list(self, str_with_list):
        try:
            # 替换中文标点为英文标点
            str_with_list = str_with_list.replace("，", ",").replace("‘", "'").replace("’", "'").replace("“", "'").replace("”", "'").replace("。", ".").replace("：", ":").replace("；", ";").replace("？", "?").replace("【", "[").replace("】", "]").replace("（", "(").replace("）", ")").replace("！", "!").replace("—", "-").replace("…", "...")
            
            # 找到第一个'['和最后一个']'的位置
            start_index = str_with_list.find('[')
            end_index = str_with_list.rfind(']') + 1  # 加1是因为切片操作不包含结束索引
            
            if start_index == -1 or end_index == 0:
                raise ValueError(f"列表的开始或结束标志未找到。原文字串为{str_with_list}")

            # 提取列表字符串
            list_str = str_with_list[start_index:end_index]

            # 尝试将提取的字符串解析为Python列表
            knowledge_points = ast.literal_eval(list_str)
            if isinstance(knowledge_points, list):
                self.analysed_list = knowledge_points
                return knowledge_points
            else:
                raise ValueError("解析出的对象不是列表。")
        except Exception as e:
            print(f"解析失败，错误信息：{e}。原文字串为{str_with_list}")
            return None

    def parse_dict(self,str_with_dict):
        try:
            # 替换中文标点为英文标点
            str_with_dict = str_with_dict.replace("，", ",").replace("‘", "'").replace("’", "'").replace("“", "'").replace("”", "'").replace("。", ".").replace("：", ":").replace("；", ";").replace("？", "?").replace("【", "[").replace("】", "]").replace("（", "(").replace("）", ")").replace("！", "!").replace("—", "-").replace("…", "...")
            str_with_dict = re.sub(r'(".*?")', lambda m: m.group(1).replace('\n', '\\n'), str_with_dict, flags=re.DOTALL)
            # 找到第一个'{'和最后一个'}'的位置
            start_index = str_with_dict.find('{')
            end_index = str_with_dict.rfind('}') + 1  # 加1是因为切片操作不包含结束索引
            
            if start_index == -1 or end_index == 0:
                raise ValueError(f"字典的开始或结束标志未找到。原文字串为{str_with_dict}")

            # 提取字典字符串
            dict_str = str_with_dict[start_index:end_index]

            # 尝试将提取的字符串解析为Python字典
            parsed_dict = ast.literal_eval(dict_str)
            
            if isinstance(parsed_dict, dict):
                return parsed_dict
            else:
                raise ValueError("解析出的对象不是字典。")
        except Exception as e:
            print(f"解析失败，错误信息：{e}。原文字串为{str_with_dict}")
            return None

    def parse_python(self,markdown_text):
        """
        提取被 ```python ``` 包裹的 Python 代码。
        
        :param markdown_text: 包含 Python 代码的 Markdown 文本
        :return: 提取的 Python 代码
        """
        pattern = r'```python(.*?)```'
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        return "\n".join(match.strip() for match in matches)
    
    def read_json(self, file_path):
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            self.json=json_data
        return json_data

    def write_json(self, content, file_path):
        # 将 content 写入 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)