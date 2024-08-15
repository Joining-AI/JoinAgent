import time
import random
import dashscope
import threading
import collections
import os
from dotenv import load_dotenv, find_dotenv

# 定义一个线程类，用于发送请求
class RequestThread(threading.Thread):
    def __init__(self, client, lock, tester):
        threading.Thread.__init__(self)  # 调用父类初始化方法
        self.client = client  # 客户端实例
        self.lock = lock  # 线程锁
        self.tester = tester  # RPMTester实例
        self.response = None  # 存储响应
        
    def run(self):
        self.response = self.tester.send_request()  # 调用RPMTester的send_request方法发送请求

# 定义一个类，用于测试每分钟请求数（RPM）
class QwenRater:
    def __init__(self):
        load_dotenv()
        self.client = dashscope.Generation()  # 创建一个生成客户端实例
        self.project_root = os.getenv('PROJECT_ROOT')
        self.total_requests = 0  # 总请求数
        self.total_input_tokens = 0  # 总输入tokens数
        self.total_output_tokens = 0  # 总输出tokens数

        self.past_minute_requests = collections.deque()  # 存储过去一分钟内的请求信息
        self.past_minute_input_tokens = 0  # 过去一分钟内的输入tokens数
        self.past_minute_output_tokens = 0  # 过去一分钟内的输出tokens数

        self.lock = threading.Lock()  # 创建一个线程锁
        self.api_key = os.getenv('QWEN_API', None)

        if self.api_key:
            try:
                dashscope.api_key = self.api_key
                self.client = dashscope.Generation()
                self.initialized = True
                print("服务初始化成功")
            except Exception as e:
                print(f"初始化服务失败: {e}")
                self.initialized = False
        else:
            raise ValueError("API密钥未在环境变量中设置")
        
    def send_request(self):
        messages = [
            {"role": "system", "content": "你是一个助手，总是简短地回复"},
            {"role": "user", "content": "你好！"}
        ]
        
        start_time = time.time()  # 记录请求开始时间
        response = self.client.call(
            model="qwen-long",
            messages=messages,
            seed=random.randint(1, 10000),
            result_format="message"
        )
        end_time = time.time()  # 记录请求结束时间

        with self.lock:  # 使用锁确保线程安全
            self.total_requests += 1  # 增加总请求数

            if response['status_code'] == 200:  # 如果请求成功

                input_tokens = response['usage']['input_tokens']  # 获取输入tokens数
                output_tokens = response['usage']['output_tokens']  # 获取输出tokens数
                self.total_input_tokens += input_tokens  # 增加总输入tokens数
                self.total_output_tokens += output_tokens  # 增加总输出tokens数
                self.past_minute_requests.append((start_time, end_time, input_tokens, output_tokens))  # 记录请求信息

                self.past_minute_input_tokens += input_tokens  # 增加过去一分钟内的输入tokens数
                self.past_minute_output_tokens += output_tokens  # 增加过去一分钟内的输出tokens数

                self.cleanup_past_minute_requests()  # 清理过期的请求信息

                return response  # 返回响应
            elif response['status_code'] == 429:  # 如果请求受限
                self.cleanup_past_minute_requests()  # 清理过期的请求信息
                return response  # 返回响应

    def cleanup_past_minute_requests(self):
        current_time = time.time()  # 获取当前时间
        while self.past_minute_requests and current_time - self.past_minute_requests[0][0] > 60:  # 如果请求信息超过一分钟
            _, _, input_tokens, output_tokens = self.past_minute_requests.popleft()  # 移除过期的请求信息
            self.past_minute_input_tokens -= input_tokens  # 减少过去一分钟内的输入tokens数
            self.past_minute_output_tokens -= output_tokens  # 减少过去一分钟内的输出tokens数

    def rpm_test(self, batch_size=10, initial_interval=0.1, decre_ratio=0.9):
        interval = initial_interval
        batch_count = 0
        recent_rpms = collections.deque(maxlen=30)  # 保存最近10次的 RPM

        while True:
            threads = []  # 存储线程
            successful_requests = 0  # 成功请求数
            total_response_time = 0  # 总响应时间

            # 创建并启动线程
            for _ in range(batch_size):
                thread = RequestThread(self.client, self.lock, self)
                threads.append(thread)
                thread.start()

            # 等待间隔时间再发起下一批请求
            time.sleep(interval)

            # 检查前一个批次的线程响应
            for thread in threads:
                if thread.is_alive():
                    thread.join(0)  # 非阻塞等待线程结束
                if thread.response and thread.response['status_code'] == 200:  # 如果请求成功
                    successful_requests += 1
                    start_time, end_time, _, _ = self.past_minute_requests[-1]
                    total_response_time += (end_time - start_time)
                elif thread.response and thread.response['status_code'] == 429:  # 如果请求受限
                    stop_time = time.time()
                    self.cleanup_past_minute_requests()  # 清理过期的请求信息
                    rpm = len(self.past_minute_requests)  # 计算RPM
                    print(f"RPM: {rpm}")
                    return rpm  # 返回RPM
            print(total_response_time, successful_requests)
            avg_response_time = total_response_time / successful_requests if successful_requests > 0 else float('inf')
            self.cleanup_past_minute_requests()  # 清理过期的请求信息
            rpm = len(self.past_minute_requests)  # 计算RPM

            recent_rpms.append(rpm)
            batch_count += 1

            if batch_count % 10 == 0:  # 每10个批次打印一次统计信息
                print(f"Batch Size: {batch_size}, RPM: {rpm}, Average Response Time: {avg_response_time:.2f} seconds")
                interval = interval * decre_ratio  # 缩小间隔

            
            if len(recent_rpms) == 30 :  # 如果最近的 RPM 变化在三倍范围内
                avg_rpm = sum(recent_rpms) / len(recent_rpms)
                if recent_rpms[-1]<=avg_rpm:
                    print('rpm_is_stable')
                    print(f"Final RPM: {avg_rpm}")
                    return avg_rpm  # 返回最终RPM