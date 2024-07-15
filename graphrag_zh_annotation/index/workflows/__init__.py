# 这段代码是从一个Python程序开始的，它导入了一些其他文件中的函数和类型定义。
# `from .load import create_workflow, load_workflows` 这行是说，从当前目录下的"load"模块中，
# 引入了两个函数：创建工作流的`create_workflow`和加载工作流的`load_workflows`。

# `from .typing import ( ... )` 这行则是在导入一些数据类型定义，这些定义可以帮助我们更清楚地了解代码中数据的结构。
# - `StepDefinition`: 定义了一个步骤（可能是一个任务或动作）。
# - `VerbDefinitions`: 可能是一系列动词（操作）的定义。
# - `VerbTiming`: 关于何时执行动词的时间信息。
# - `WorkflowConfig`: 工作流的配置信息，比如设置和参数。
# - `WorkflowDefinitions`: 一组工作流的定义。
# - `WorkflowToRun`: 表示要运行的工作流。

# 下面这一行是一个版权声明，告诉别人这个代码是由微软公司创作的，使用的是MIT许可证。
# `# Copyright (c) 2024 Microsoft Corporation.`
# `# Licensed under the MIT License`

# 这个注释说明了这个Python文件是工作流包的根目录。
# `"The Indexing Engine workflows package root."`

# 接下来，`__all__`是一个特殊列表，它告诉其他导入这个模块的代码，应该公开哪些名称。
# 这里列出的都是之前导入的类型和函数，这样在其他地方导入这个模块时，可以直接使用它们。
__all__ = [
    "StepDefinition",
    "VerbDefinitions",
    "VerbTiming",
    "WorkflowConfig",
    "WorkflowDefinitions",
    "WorkflowToRun",
    "create_workflow",
    "load_workflows",
]

