import regex as re

class LineDivider:
    def __init__(self, pattern):
        """
        初始化LineDivider类，设置截断模式。
        :param pattern: 用于分割的正则表达式模式
        """
        self.pattern = pattern
    
    def split_text(self, text):
        """
        根据初始化时提供的正则表达式模式，分割输入文本并返回一个字典。
        :param text: 待处理的字符串
        :return: 包含分割结果的字典
        """
        lines = text.split('\n')
        temp_para_list = []
        temp_para = []
        split_lines = []
        
        for line in lines:
            if re.search(self.pattern, line.strip()):
                if temp_para:
                    temp_para_list.append('\n'.join(temp_para))
                    temp_para = []
                split_lines.append(line)
            else:
                if split_lines and not re.search(self.pattern, split_lines[-1].strip()):
                    temp_para.append(line)
                elif split_lines:
                    temp_para.append(line)
        
        if temp_para:
            temp_para_list.append('\n'.join(temp_para))

        result = {}
        for i, split_line in enumerate(split_lines):
            if i < len(temp_para_list):
                result[split_line] = temp_para_list[i]
            else:
                result[split_line] = ''

        return result