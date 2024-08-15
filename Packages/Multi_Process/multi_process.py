import threading
import time
import random
from queue import Queue
from tqdm import tqdm
import json
import os

class MultiProcessor:

    def __init__(self, llm, parse_method, data_template, prompt_template, correction_template, validator, empty_template, time_limit=60, back_up_llm=None):
        self.llm = llm  # 主要的大型语言模型 (LLM)
        self.back_up_llm = back_up_llm  # 备用的 LLM，初始为 None
        self.parse_method = parse_method
        self.data_template = data_template
        self.prompt_template = prompt_template
        self.correction_template = correction_template
        self.validator = validator
        self.empty_template = empty_template
        self.time_limit = time_limit

    def generate_prompt(self, **kwargs):
        kwargs['data_template'] = self.data_template
        return self.prompt_template.format(**kwargs)

    def generate_correction_prompt(self, answer):
        return self.correction_template.format(answer=answer, data_template=self.data_template)

    def generate_empty_response(self, input_tuple):
        input_data = input_tuple[:-1]
        input_dict = {f'input_{i+1}': input_data[i] for i in range(len(input_data))} 
        return self.parse_method(self.empty_template.format(**input_dict))

    def task_perform(self, llm, **kwargs):
        try:
            prompt = self.generate_prompt(**kwargs)
            answer = llm.ask(prompt)
            structured_data = self.parse_method(answer)
            return structured_data
        except Exception as e:
            print(f"Error in task_perform: {str(e)}")
            raise e

    def correct_data(self, llm, answer):
        correction_prompt = self.generate_correction_prompt(answer)
        correction = llm.ask(correction_prompt)
        return self.parse_method(correction)

    def process_tuple(self, input_tuple):
        try:
            input_data = input_tuple[:-1]
            index = input_tuple[-1]
            attempts = 0
            base_wait_time = 1
            use_backup = False

            while attempts < 2:
                try:
                    input_dict = {f'input_{i+1}': input_data[i] for i in range(len(input_data))}
                    current_llm = self.back_up_llm if (use_backup and self.back_up_llm is not None) else self.llm
                    structured_data = self.task_perform(current_llm, **input_dict)
                    if self.validator(structured_data):
                        return (structured_data, index)
                    corrected_answer = self.correct_data(current_llm, structured_data)
                    if corrected_answer and self.validator(corrected_answer):
                        return (corrected_answer, index)
                    break
                except Exception as e:
                    if 'Throttling.RateQuota' in str(e):
                        wait_time = base_wait_time * (2 ** attempts) + random.uniform(0, 1)
                        print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds. Attempt {attempts + 1}/2")
                        time.sleep(wait_time)
                    else:
                        print(f"An error occurred: {str(e)}. Attempt {attempts + 1}/2")
                    
                    attempts += 1
                    if not use_backup and self.back_up_llm is not None:
                        use_backup = True
                        print("Switching to backup LLM to process:", input_data)

            return None  # 如果所有尝试都失败，返回 None

        except Exception as final_error:
            print(f"Error occurred during process_tuple: {str(final_error)}")
            return None  # 返回 None 表示跳过这个任务

    def multitask_perform(self, tuple_list, num_threads, checkpoint=10):
        results = [None] * len(tuple_list)
        queue = Queue()
        checkpoint_counter = 0

        checkpoint_dir = "checkpoint"
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)

        for idx, input_tuple in enumerate(tuple_list):
            queue.put((input_tuple, idx))

        def worker(pbar):
            nonlocal checkpoint_counter
            while not queue.empty():
                input_tuple, idx = queue.get()
                result = None
                thread_result_queue = Queue()

                thread = threading.Thread(target=lambda q, arg1: q.put(self.process_tuple(arg1)), args=(thread_result_queue, input_tuple))
                thread.start()
                thread.join(timeout=self.time_limit)

                if thread.is_alive():
                    print(f"Thread processing {input_tuple} timed out.")
                    thread.join()
                else:
                    if not thread_result_queue.empty():
                        result = thread_result_queue.get()
                    else:
                        print(f"No result obtained for {input_tuple}")

                if result is None:
                    print(f"Skipping task for {input_tuple}")
                    empty_response = self.generate_empty_response(input_tuple)
                    results[idx] = (empty_response, idx)
                else:
                    results[idx] = result

                queue.task_done()
                pbar.update(1)

                checkpoint_counter += 1
                if checkpoint_counter % checkpoint == 0:
                    save_checkpoint(results)

        def save_checkpoint(results):
            checkpoint_path = os.path.join(checkpoint_dir, 'checkpoint.json')
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print(f"Checkpoint saved at {checkpoint_path}")

        with tqdm(total=len(tuple_list)) as pbar:
            threads = []
            for _ in range(min(num_threads, len(tuple_list))):
                thread = threading.Thread(target=worker, args=(pbar,))
                threads.append(thread)
                thread.start()

            queue.join()

            for thread in threads:
                thread.join()

        save_checkpoint(results)

        return results
