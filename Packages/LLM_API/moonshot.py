import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

class KimiService:
    def __init__(self, version='8k'):
        # 加载当前目录的.env文件
        load_dotenv()

        self.version='moonshot-v1-'+version
        self.client = None
        self.initialized = False
        self.total_tokens_used = 0  # 添加一个成员变量用于保存总共使用的token数量
        # 从环境变量中导入API密钥和基础URL
        api_key = os.getenv('KIMI_API', None)
        base_url ='https://api.moonshot.cn/v1'
        self.init_service(api_key, base_url)

    def init_service(self, api_key: str, base_url: str) -> bool:
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.initialized = True
        return True

    def ask_once(self, prompt: str) -> str:
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")
        
        if not self.client:
            raise ValueError("OpenAI 客户端未正确初始化，请检查初始化过程。")
        
        response = self.client.chat.completions.create(
            max_tokens=8192,
            model=self.version,
            messages=[{"role": "user", "content": prompt}]
        )

        if response:
            total_tokens = response.usage.total_tokens
            self.total_tokens_used += total_tokens  # 更新总共使用的token数量
            #print("本次使用的token数量：", total_tokens)
            return response.choices[0].message.content
        else:
            return ""

    def upload_file(self, file_path: str, purpose: str = "file-extract"):
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")

        file_object = self.client.files.create(file=Path(file_path), purpose=purpose)
        return file_object

    def get_file_content(self, file_id: str) -> str:
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")

        file_content = self.client.files.content(file_id=file_id).text
        return file_content
    
    def list_files(self):
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")

        file_list = self.client.files.list()
        return file_list.data

    def delete_file(self, file_id: str):
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")

        self.client.files.delete(file_id=file_id)

    def clear_all_files(self):
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")

        files = self.list_files()
        for file in files:
            self.delete_file(file.id)  # 使用点操作符访问文件 ID 属性
            print('one file deleted')
        return "All files have been deleted."

    def chat_with_file(self, file_path: str, user_prompt: str):
        file_object = self.upload_file(file_path)
        file_id = file_object.id
        file_content = self.get_file_content(file_object.id)

        messages = [
            {
                "role": "system",
                "content": "你是 Kimi，是一个pdf理解助手，对于收到的pdf文件，你总是忠实地理解它，对于数学符号和公式总是输出latex格式",
            },
            {
                "role": "system",
                "content": file_content,
            },
            {"role": "user", "content": user_prompt},
        ]

        completion = self.client.chat.completions.create(
            model=self.version,
            messages=messages,
            temperature=0.3,
        )

        # 删除文件
        self.delete_file(file_id)

        return completion.choices[0].message.content