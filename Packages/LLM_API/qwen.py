import os
import random
from dotenv import load_dotenv
from http import HTTPStatus
from pathlib import Path
import dashscope
import requests
from openai import OpenAI

class QwenService:
    def __init__(self, version='long'):
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
            messages = [{'role': 'system', 'content': f'你是一个忠实细致的助手，你的输出应该使用{language}'},
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
        
    def chat_with_file(self, file_path: str, prompt: str, language='中文') -> str:
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        file_id = None
        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            file = client.files.create(file=Path(file_path), purpose="file-extract")
            file_id = file.id
            
            messages = [
                {'role': 'system', 'content': f'你是一个忠实细致的助手，你的输出应该使用{language}'},
                {'role': 'system', 'content': f'fileid://{file.id}'},
                {'role': 'user', 'content': prompt}
            ]
            
            completion = client.chat.completions.create(
                model=self.version,
                messages=messages,
                stream=False
            )
            
            # 确保正确解析返回内容
            if completion.choices and completion.choices[0].message and completion.choices[0].message.content:
                output_content = completion.choices[0].message.content
                self.output_word_count = len(output_content)
                
                # 删除云文件
                self.delete_file(file_id)
                
                return output_content
            else:
                print(completion)
                self.delete_file(file_id)
                return "未找到有效的响应内容"
                
        except Exception as e:
            if file_id:
                self.delete_file(file_id)
            return f"请求过程中发生错误: {e}"

    def list_files(self):
        """列出当前所有云文件的ID"""
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            files = client.files.list()
            file_ids = [file.id for file in files.data]
            return file_ids
            
        except Exception as e:
            return f"获取文件列表时发生错误: {e}"

    def delete_file(self, file_id: str):
        """删除指定的云文件ID"""
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            client.files.delete(file_id)
            return f"文件 {file_id} 已删除"
            
        except Exception as e:
            return f"删除文件时发生错误: {e}"

    def clear_all_files(self):
        """一键清空所有云文件"""
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            files = client.files.list()
            for file in files.data:
                client.files.delete(file.id)
                print("已删除文件: ", file.id)
            
            return "所有文件已删除"
            
        except Exception as e:
            return f"清空文件时发生错误: {e}"