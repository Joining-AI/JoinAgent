import ast
import os
import concurrent.futures
import time
from collections import defaultdict

class PythonProjectProcessor:
    def __init__(self, processor, service):
        self.processor = processor
        self.service = service

    def get_source_segment(self, source, node):
        """Get the source code segment for the given AST node。"""
        lines = source.splitlines()
        start_line = node.lineno - 1
        end_line = node.end_lineno
        return "\n".join(lines[start_line:end_line])

    def get_python_units(self, file_path, threshold=4096):
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()

        tree = ast.parse(source_code)
        units = []

        import_unit = []
        last_end_line = 0

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_unit.append(self.get_source_segment(source_code, node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if import_unit:
                    units.append({
                        "index": len(units) + 1,
                        "source_code": "\n".join(import_unit),
                        "file_path": file_path,
                        "start_line": last_end_line + 1,
                        "end_line": node.lineno - 1
                    })
                    import_unit = []
                start_line = node.lineno - 1
                if last_end_line < start_line:
                    units.append({
                        "index": len(units) + 1,
                        "source_code": "\n".join(source_code.splitlines()[last_end_line:start_line]),
                        "file_path": file_path,
                        "start_line": last_end_line + 1,
                        "end_line": start_line
                    })
                units.append({
                    "index": len(units) + 1,
                    "source_code": self.get_source_segment(source_code, node),
                    "file_path": file_path,
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                })
                last_end_line = node.end_lineno

        # Append remaining import statements
        if import_unit:
            units.append({
                "index": len(units) + 1,
                "source_code": "\n".join(import_unit),
                "file_path": file_path,
                "start_line": last_end_line + 1,
                "end_line": last_end_line + len(import_unit)
            })

        # Append any trailing code
        if last_end_line < len(source_code.splitlines()):
            units.append({
                "index": len(units) + 1,
                "source_code": "\n".join(source_code.splitlines()[last_end_line:]),
                "file_path": file_path,
                "start_line": last_end_line + 1,
                "end_line": len(source_code.splitlines())
            })

        # Merge units to ensure each unit is at least threshold characters long
        merged_units = []
        current_unit = ""
        current_start_line = 0
        for unit in units:
            if len(current_unit) == 0:
                current_start_line = unit['start_line']

            if len(current_unit) + len(unit['source_code']) > threshold:
                if current_unit:
                    merged_units.append({
                        "index": len(merged_units) + 1,
                        "source_code": current_unit,
                        "file_path": file_path,
                        "start_line": current_start_line,
                        "end_line": unit['start_line'] - 1
                    })
                current_unit = unit['source_code']
                current_start_line = unit['start_line']
            else:
                current_unit += "\n" + unit['source_code']

        if current_unit:
            merged_units.append({
                "index": len(merged_units) + 1,
                "source_code": current_unit,
                "file_path": file_path,
                "start_line": current_start_line,
                "end_line": len(source_code.splitlines())
            })

        return merged_units

    def task_processor(self, code, retries=3, delay=2):
        """
        Process the code and add Chinese comments.
        Retries up to `retries` times in case of failure, with `delay` seconds between retries.
        """
        prompt = f'''
        请你为我解释下面的python代码，逐行中文注释，使得一个十岁小孩也能看懂，并且不许减少一行代码。

        {code}
        '''
        for attempt in range(retries):
            try:
                answer = self.service.ask_once(prompt)
                python_code = self.processor.parse_python(answer)
                return python_code
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        raise Exception("All retry attempts failed。")

    def process_unit(self, unit):
        try:
            new_code = self.task_processor(unit['source_code'])
            return (unit['file_path'], unit['index'], new_code)
        except Exception as e:
            print(f"Failed to process unit {unit['index']} in file {unit['file_path']}: {e}")
            return (unit['file_path'], unit['index'], None)

    def process_python_project(self, root_folder, new_root_folder, threshold=100, max_workers=50):
        python_files = []
        for subdir, _, files in os.walk(root_folder):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(subdir, file))

        all_units = []
        for file_path in python_files:
            relative_path = os.path.relpath(file_path, root_folder)
            units = self.get_python_units(file_path, threshold)
            for unit in units:
                unit['file_path'] = relative_path
                all_units.append(unit)

        # Sort all units by file path and start line to maintain order
        all_units.sort(key=lambda x: (x['file_path'], x['start_line']))

        if not os.path.exists(new_root_folder):
            os.makedirs(new_root_folder)

        results = []
        total_units = len(all_units)

        def print_progress(finished_units, total_units):
            print(f"Processed {finished_units}/{total_units} units ({(finished_units / total_units) * 100:.2f}%)")

        finished_units = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.process_unit, unit) for unit in all_units]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                finished_units += 1
                print_progress(finished_units, total_units)

        # Group results by file path
        grouped_results = defaultdict(list)
        for file_path, index, new_code in results:
            grouped_results[file_path].append((index, new_code))

        # Write results to new files in order
        for file_path, code_segments in grouped_results.items():
            # Sort code segments by index
            code_segments.sort(key=lambda x: x[0])
            new_file_path = os.path.join(new_root_folder, file_path)
            new_dir = os.path.dirname(new_file_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            last_index = 0
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                for index, new_code in code_segments:
                    if index != last_index + 1:
                        print(f"Warning: Missing code segment between indices {last_index} and {index} in file {file_path}")
                    if new_code is None:
                        print(f"Warning: Code segment at index {index} in file {file_path} is None")
                    else:
                        new_file.write(new_code)
                        new_file.write("\n\n")  # Add extra new lines between units
                    last_index = index