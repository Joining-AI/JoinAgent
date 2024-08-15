class TextDivider:
    def __init__(self, threshold, overlap):
        self.threshold = threshold
        self.overlap = overlap

    @staticmethod
    def reverse(line_list):
        # 颠倒每个str_line中的str_character
        reversed_lines = [line[::-1] for line in line_list]
        # 颠倒每个line
        reversed_lines.reverse()
        return reversed_lines

    @staticmethod
    def headcutter(line_list, threshold, loose=True):
        
        current_chunk = []
        current_length = 0
        indices = []

        for i, line in enumerate(line_list):
            line_length = len(line)

            if loose:
                # 宽松分割逻辑
                if current_length + line_length > threshold:
                    indices.append(i)
                    current_chunk.append(line)
                    break
                else:
                    indices.append(i)
                    current_chunk.append(line)
                    current_length += line_length
            else:
                # 紧凑分割逻辑
                while line_length > 0:
                    if current_length + line_length > threshold:
                        remaining_length = threshold - current_length
                        if remaining_length > 0:
                            indices.append(i)
                            current_chunk.append(line[:remaining_length])
                            line = line[remaining_length:]
                            line_length -= remaining_length
                        return current_chunk, indices  # 达到阈值，返回当前块及其索引
                    else:
                        indices.append(i)
                        current_chunk.append(line)
                        current_length += line_length
                        break

        return current_chunk, indices

    def divide(self,txt_path):
        
        with open(txt_path, 'r', encoding='utf-8') as file:
            line_list = file.readlines()
        line_list=self.shredder(line_list, self.threshold//8)
        
        string_list = []
        loose_threshold = self.threshold
        tight_threshold = self.overlap
        # 使用 loose 模式获取第一个块及其索引
        current_chunk, current_chunk_indices = self.headcutter(line_list, loose_threshold, loose=True)
        line_list = [line for i, line in enumerate(line_list) if i not in current_chunk_indices]

        # 更新 loose_threshold 为 threshold - overlap
        loose_threshold = self.threshold - self.overlap
        string_list.append('\n'.join(current_chunk))
        while line_list:
            # 颠倒当前块
            reversed_chunk = self.reverse(current_chunk)

            # 使用 tight 模式获取重叠块及其索引
            overlap_chunk, overlap_chunk_indices = self.headcutter(reversed_chunk, tight_threshold, loose=False)

            # 颠倒重叠块以回正
            overlap_chunk = self.reverse(overlap_chunk)

            # 使用 loose 模式获取当前块并更新 line_list
            current_chunk, current_chunk_indices = self.headcutter(line_list, loose_threshold, loose=True)
            line_list = [line for i, line in enumerate(line_list) if i not in current_chunk_indices]

            # 把重叠块添加到当前块前面构成一个分割块
            current_chunk = overlap_chunk + current_chunk

            # 组合成字符串
            string_list.append('\n'.join(current_chunk))

        return string_list
    
    def shredder(self,line_list, threshold):
        """
        将line_list中长度超过4倍threshold的行进行切割，尽量在标点符号或空格处断开，必要时适当向后延长。
        
        参数:
        line_list (list): 包含字符串的列表。
        threshold (int): 切割长度的阈值。
        
        返回:
        list: 包含切割后字符串的新列表。
        """
        # 定义切割符列表，包含所有标点符号和空格
        split_chars = " !$%&'()*+,-./:;<=>?@[]^_`{|}~　，。、；：？！…—·ˉ¨‘’“”々～‖∶＂＇｀｜〃〔〕〈〉《》「」『』．［］（）｛｝" # 注意不能添加\，以防截断换行符；虽然不全面，但是实际上大部分的时候这个断词表已经够用了
        
        new_line_list = []
        
        for line in line_list:
            if len(line) > 4 * threshold:
                # 将行按threshold长度切割，尽量在标点符号或空格处断开
                start = 0
                while start < len(line):
                    end = start + threshold
                    if end < len(line):
                        # 在threshold之后找到下一个标点符号或空格
                        while end < len(line) and line[end] not in split_chars:
                            end += 1
                        if end < len(line):
                            # 找到标点符号或空格，将其作为结束点
                            new_line_list.append(line[start:end].rstrip())
                            start = end + 1  # 跳过标点符号或空格
                        else:
                            # 没有更多标点符号或空格，使用剩余部分
                            new_line_list.append(line[start:].rstrip())
                            start = len(line)
                    else:
                        # 没有更多标点符号或空格，使用剩余部分
                        new_line_list.append(line[start:].rstrip())
                        start = len(line)
            else:
                new_line_list.append(line)
        
        return new_line_list