import json
import ast
import re

class LLMParser:
    def __init__(self):
        pass

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
                return knowledge_points
            else:
                raise ValueError("解析出的对象不是列表。")
        except Exception as e:
            raise RuntimeError(f"解析失败，错误信息：{e}。原文字串为{str_with_list}")
        
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
            raise RuntimeError(f"解析失败，错误信息：{e}。原文字串为{str_with_dict}")

    def parse_pads(self, str_with_pads):
        try:
            # 替换中文标点为英文标点
            str_with_pads = str_with_pads.replace("，", ",").replace("‘", "'").replace("’", "'").replace("“", "'").replace("”", "'").replace("。", ".").replace("：", ":").replace("；", ";").replace("？", "?").replace("【", "[").replace("】", "]").replace("（", "(").replace("）", ")").replace("！", "!").replace("—", "-").replace("…", "...")
            str_with_pads = re.sub(r'(".*?")', lambda m: m.group(1).replace('\n', '\\n'), str_with_pads, flags=re.DOTALL)

            # 将数据转换为小写以确保兼容大小写
            str_with_pads_lower = str_with_pads.lower()

            # 找到第一个 '=start_pad=' 和最后一个 '=end_pad=' 的位置
            start_pad = '=start_pad='
            end_pad = '=end_pad='
            start_index = str_with_pads_lower.find(start_pad) + len(start_pad)
            end_index = str_with_pads_lower.rfind(end_pad)

            if start_index == -1 or end_index == -1:
                raise ValueError(f"开始或结束标志未找到。原文字串为{str_with_pads}")

            # 提取 pad 中的内容
            content_str = str_with_pads[start_index:end_index].strip()

            # 返回提取的内容
            return content_str
        except Exception as e:
            raise RuntimeError(f"解析失败，错误信息：{e}。原文字串为{str_with_pads}")


    def parse_code(self,markdown_text):
        """
        提取被 ```code ``` 包裹的单个代码以及代码语言。
        
        :param markdown_text: 包含代码的 Markdown 文本
        :return: 单个代码块的语言名称和代码内容
        """
        pattern = r'```([\w\s]+?)\n(.*?)```'
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if matches:
            language = matches[0][0].strip()
            code = matches[0][1].strip()
            return code
        return None
        
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