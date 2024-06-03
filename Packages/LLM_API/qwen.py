import os
import random
from dotenv import load_dotenv
from http import HTTPStatus
import dashscope

class QwenService:
    def __init__(self, version='large'):
        # 加载当前目录的.env文件
        load_dotenv()
        
        self.version = 'qwen-' + version
        self.client = None
        self.initialized = False
        self.input_word_count = 0  # 输入字数
        self.output_word_count = 0  # 输出字数
        
        # 从环境变量中导入API密钥
        api_key = os.getenv('QWEN_API', None)
        if api_key:
            self.init_service(api_key)
        else:
            raise ValueError("API密钥未在环境变量中设置")

    def init_service(self, api_key: str) -> bool:
        try:
            dashscope.api_key = api_key
            self.client = dashscope.Generation()
            self.initialized = True
            print("服务初始化成功")
            return True
        except Exception as e:
            print(f"初始化服务失败: {e}")
            self.initialized = False
            return False

    def ask_once(self, prompt: str, language='中文') -> str:
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            # 计算输入字数
            self.input_word_count = len(prompt)
            
            # 确保将请求格式化为正确的消息格式
            messages = [{'role': 'system', 'content': f'你是一个忠实的文本分析师，除指定的输出格式遵循其语言之外，其他输出都应该使用{language}'},
                        {'role': 'user', 'content': prompt}]
            
            resp = self.client.call(model=self.version, messages=messages, seed=random.randint(1, 10000), result_format='message')

            if resp.status_code == HTTPStatus.OK:
                output_content = ""
                if hasattr(resp, 'output') and 'choices' in resp.output:
                    choices = resp.output['choices']
                    if choices and 'message' in choices[0] and 'content' in choices[0]['message']:
                        output_content = choices[0]['message']['content']
                        self.output_word_count = len(output_content)
                    else:
                        output_content = "未找到有效的响应内容"
                        self.output_word_count = len(output_content)
                else:
                    output_content = "响应中不包含choices"
                    self.output_word_count = len(output_content)
                return output_content
            else:
                return f"请求失败: {resp.code} - {resp.message}"
        except Exception as e:
            return f"请求过程中发生错误: {e}"