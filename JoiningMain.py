import openai
import os
import json
import PyPDF2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt
import sys
import shutil
import subprocess

class Joining:
    def __init__(self, api_url: str, openai_api_key: str):
        self.api_url = api_url
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        openai.api_base = api_url
        self.dialogues = []  # 用于存储对话信息的列表
    
    def _init_service(self, user_key: str, base_url: str) -> bool:
        # 在这里执行基于 user_key 和 base_url 的初始化操作
        # 示例代码，具体逻辑根据需要进行调整
        self.user_key = user_key
        self.base_url = base_url
        # 假设这里执行了一些操作并成功完成
        # 返回 True 表示初始化服务成功
        return True
    
    def process(self, question: str) -> str:
        try:
            messages = [{"role": "user", "content": question}]
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages
            )
            answer = response['choices'][0]['message']['content']
            # 构建对话元组并添加到列表中
            dialogue = (question, answer)
            self.dialogues.append(dialogue)
            return answer
        except openai.error.APIError as e:
            # 处理 OpenAI API 错误
            return f"OpenAI API错误: {str(e)}"
        except Exception as e:
            # 处理其他错误
            return f"处理错误: {str(e)}"
        
    def read_uploaded_file(self, file_path: str) -> str:
        """
        读取上传的文件内容
        :param file_path: 上传文件的路径
        :return: 文件内容的字符串表示
        """
        def process_pdf(file) -> str:
            """
            使用 PyPDF2 库处理 PDF 文件并读取内容
            :param file: PDF 文件对象
            :return: PDF 文件内容的字符串表示
            """
            try:
                # 创建 PyPDF2 的 PdfFileReader 对象
                pdf_reader = PyPDF2.PdfFileReader(file)
                
                # 初始化 PDF 内容字符串
                pdf_content = ""
                
                # 逐页读取 PDF 内容
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    pdf_content += page.extractText()
                
                return pdf_content
            except Exception as e:
                return f"处理 PDF 错误: {str(e)}"
        try:
            # 判断文件类型
            _, file_extension = os.path.splitext(file_path)
            if file_extension.lower() == '.pdf':
                # 处理 PDF 文件
                with open(file_path, 'rb') as file:
                    # 读取 PDF 内容
                    # 这里使用第三方库来处理 PDF，比如 PyPDF2 或 pdfplumber
                    pdf_content = process_pdf(file)
                return pdf_content
            elif file_extension.lower() in ('.txt', '.md'):
                # 处理 TXT 或 MD 文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 读取文本文件内容
                    text_content = file.read()
                return text_content
            else:
                return "不支持的文件格式"
        except Exception as e:
            return f"读取文件错误: {str(e)}"
        
    def query_json_file(self, file_name: str, key: str) -> str:
        """
        查询同一目录下的 JSON 文件中的内容
        :param file_name: JSON 文件名
        :param key: 要查询的键值
        :return: 查询到的值，如果未找到则返回空字符串
        """
        try:
            # 获取当前工作目录的路径
            current_dir = os.getcwd()
            # 构建 JSON 文件的完整路径
            json_file_path = os.path.join(current_dir, "Prompts", file_name)
            
            # 检查文件是否存在
            if not os.path.exists(json_file_path):
                return "JSON 文件不存在"
            
            # 读取 JSON 文件内容
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                
                # 查询指定键值
                value = data.get(key, "")
                
                return value
        except Exception as e:
            return f"查询 JSON 文件错误: {str(e)}"
        
    def create_json_file(self, file_name: str, data: dict) -> bool:
        """
        创建 JSON 文件并写入数据
        :param file_name: 要创建的 JSON 文件名
        :param data: 要写入的数据，字典形式
        :return: 如果成功创建文件则返回True，否则返回False
        """
        try:
            # 获取当前工作目录的路径
            current_dir = os.getcwd()
            # 构建 JSON 文件的完整路径
            json_file_path = os.path.join(current_dir, "Prompts", file_name)
            
            # 写入数据到 JSON 文件
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            return False

    def delete_json_file(self, file_name: str) -> bool:
        """
        删除指定的 JSON 文件
        :param file_name: 要删除的 JSON 文件名
        :return: 如果成功删除文件则返回True，否则返回False
        """
        try:
            # 获取当前工作目录的路径
            current_dir = os.getcwd()
            # 构建 JSON 文件的完整路径
            json_file_path = os.path.join(current_dir, "Prompts", file_name)
            
            # 检查文件是否存在，存在则删除
            if os.path.exists(json_file_path):
                os.remove(json_file_path)
                return True
            else:
                return False
        except Exception as e:
            return False

class JoiningPresenter(QWidget):
    def __init__(self, processor: Joining):
        super().__init__()
        self.processor = processor
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('问答系统')
        self.setGeometry(100, 100, 400, 300)
        self.setAcceptDrops(True)  # 允许窗口接受拖拽事件
        
        layout = QVBoxLayout()
        
        # 现有的UI组件
        self.question_label = QLabel('请输入你的问题：')
        layout.addWidget(self.question_label)
        
        self.question_entry = QLineEdit()
        layout.addWidget(self.question_entry)
        
        self.answer_button = QPushButton('获取回答')
        self.answer_button.clicked.connect(self.display_response)
        layout.addWidget(self.answer_button)
        
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        layout.addWidget(self.response_text)
        
        # 添加文件上传按钮
        self.upload_button = QPushButton('上传文件')
        self.upload_button.clicked.connect(self.uploadFile)
        layout.addWidget(self.upload_button)
        
        self.setLayout(layout)
    
    def uploadFile(self):
        # 打开文件选择对话框
        fname, _ = QFileDialog.getOpenFileName(self, '选择文件', '', '所有文件 (*)')
        if fname:
            self.saveFile(fname)
    
    def saveFile(self, filePath):
        # 检查并创建TempFile文件夹
        tempFolderPath = os.path.join(os.getcwd(), 'TempFile')
        if not os.path.exists(tempFolderPath):
            os.makedirs(tempFolderPath)
        # 复制文件到TempFile文件夹
        shutil.copy(filePath, tempFolderPath)
        self.response_text.setText(f"文件已上传至: {tempFolderPath}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            self.saveFile(file)
        self.response_text.setText(f"文件已上传至: {os.path.join(os.getcwd(), 'TempFile')}")

        
    def display_response(self):
        question = self.question_entry.text()
        response = self.processor.process(question)
        self.response_text.setText(f"问题: {question}\n回答: {response}")

class JoiningCodeRunner:
    def __init__(self, code_directory=os.path.join(os.getcwd(), 'TempCode')):
        self.code_directory = code_directory

    def run_code(self):
        # 确保代码目录存在
        if not os.path.exists(self.code_directory):
            print(f"目录{self.code_directory}不存在")
            return

        # 遍历目录下的所有.py文件并执行它们
        for filename in os.listdir(self.code_directory):
            if filename.endswith(".py"):
                filepath = os.path.join(self.code_directory, filename)
                print(f"正在运行: {filepath}")
                try:
                    # 使用subprocess.run来运行Python脚本
                    result = subprocess.run(["python", filepath], capture_output=True, text=True)
                    print(f"输出:\n{result.stdout}")
                    if result.stderr:
                        print(f"错误:\n{result.stderr}")
                except Exception as e:
                    print(f"运行{filename}时出错: {e}")
