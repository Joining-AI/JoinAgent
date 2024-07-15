# 这段代码是微软公司写的，遵循了MIT许可证
# 它是一个包含MOCK_LLM_RESPONSES定义的文件

# MOCK_LLM_RESPONSES是一个列表，里面装着一些信息
MOCK_LLM_RESPONSES = [  # 开始定义列表
    """
[
    # 这里是一个JSON格式的数据，像一个包裹，装着关于公司和政府机构的信息
    {  # 开始一个包裹（字典）
        "subject": "COMPANY A",  # 主题是：公司A
        "object": "GOVERNMENT AGENCY B",  # 对象是：政府机构B
        "type": "ANTI-COMPETITIVE PRACTICES",  # 类型是：反竞争行为
        "status": "TRUE",  # 状态是：真实的
        "start_date": "2022-01-10T00:00:00",  # 开始日期：2022年1月10日
        "end_date": "2022-01-10T00:00:00",  # 结束日期：同上，事件只有一天
        "description": "Company A was found to engage in anti-competitive practices because it was fined for bid rigging in multiple public tenders published by Government Agency B according to an article published on 2022/01/10",
        # 描述：根据2022年1月10日发布的一篇文章，公司A因在政府机构B发布的多个公共招标中操纵投标而被罚款。
        "source_text": [  # 来源文本：文章里的内容
            "According to an article published on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B."
        ]
    }  # 结束这个包裹（字典）
]
    """.strip()  # 去掉字符串前面或后面的空白字符
]  # 列表定义结束

