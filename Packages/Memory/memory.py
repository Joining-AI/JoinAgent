import threading
from queue import Queue

class Memory():
    def __init__(self, threshold, overlap, llm):
        self.threshold = threshold
        self.overlap = overlap
        self.llm=llm
    
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

    def summarize(self, input_text, concern_topic=None):
        summarize_prompt = f'''
        你是一个出色的文字压缩器，以下有一段长文本，我期待你对其进行压缩和摘要：

        {input_text}

        请你不要输出任何无关内容，仅输出压缩后的文本。
        '''
        if concern_topic:
            summarize_prompt += f'''
            我还期望你仅输出与{concern_topic}相关的内容。
            '''
        return self.llm.ask(summarize_prompt)
    
    def summarize_worker(self, queue, output, concern_topic):
        while not queue.empty():
            index, input_text = queue.get()
            summarized_text = self.summarize(input_text, concern_topic)
            output[index] = summarized_text
            queue.task_done()

    def summarize_list(self, string_list, thread_number, concern_topic=None):
        queue = Queue()
        output = [None] * len(string_list)
        
        # 将每个字符串及其索引放入队列
        for i, input_text in enumerate(string_list):
            queue.put((i, input_text))
        
        threads = []
        # 创建指定数量的线程来处理队列中的任务
        for _ in range(thread_number):
            thread = threading.Thread(target=self.summarize_worker, args=(queue, output, concern_topic))
            thread.start()
            threads.append(thread)
        
        # 等待所有任务完成
        queue.join()
        
        # 确保所有线程都已完成
        for thread in threads:
            thread.join()
        
        return output
    
    @classmethod
    def combine_lines(cls, string_list, threshold):
        combined_lines = []
        current_lines = []
        current_length = 0

        for string in string_list:
            string_length = len(string)
            if current_length + string_length > threshold:
                combined_lines.append(current_lines)
                current_lines = []
                current_length = 0
            
            current_lines.append(string)
            current_length += string_length

        if current_lines:
            combined_lines.append(current_lines)

        return combined_lines
