# 导入json模块，它帮助我们处理数据，像把字典变成字符串或反过来
import json

# 这里是微软公司2024年的版权信息，它告诉别人这段代码不能随便用
# Licensed under the MIT License 表示代码遵循MIT许可证

# 这个文件包含两个重要的东西：DEFAULT_CHUNK_SIZE和MOCK_RESPONSES的定义
# 注释是用来解释代码的，这样别人更容易理解

# 定义一个变量 DEFAULT_CHUNK_SIZE，它的值是3000
DEFAULT_CHUNK_SIZE = 3000
# 定义一个列表 MOCK_RESPONSES，里面会有一些模拟的数据
MOCK_RESPONSES = [  # 开始定义列表
    # 列表的第一个元素是一个用json.dumps()处理过的字典，它会把字典变成字符串
    json.dumps({  # 开始字典
        "title": "<report_title>",  # 报告的标题，这里用< >表示是个占位符
        "summary": "<executive_summary>",  # 摘要，也是占位符
        "rating": 2,  # 评分，这里是2
        "rating_explanation": "<rating_explanation>",  # 评分解释，占位符
        "findings": [  # 发现的问题列表
            {  # 第一个问题
                "summary": "<insight_1_summary>",  # 问题总结，占位符
                "explanation": "<insight_1_explanation",  # 问题解释，占位符
            },
            {  # 第二个问题
                "summary": "<farts insight_2_summary>",  # 问题总结，这里有错别字，可能是"<farts insight_2_summary>"
                "explanation": "<insight_2_explanation",  # 问题解释，占位符
            },
        ],
    })  # 结束字典，列表结束
]  # 结束列表定义

