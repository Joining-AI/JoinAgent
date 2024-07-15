# 这段代码是用来处理和整理数据的，让它们变得更方便查看。我们将一步步解释每一行。

from typing import cast
# 这一行引入了一个叫做"cast"的东西，它帮助我们确保数据类型是正确的。

import pandas as pd
# 这一行导入了一个叫pandas的库，它专门用来处理表格数据。

from datashaper import TableContainer, VerbInput, verb
# 这一行导入了datashaper库中的几个工具，TableContainer用来存储数据，VerbInput和verb则是处理数据的方法。

from graphrag.index.graph.extractors.community_reports.schemas import (
    CLAIM_DESCRIPTION,
    CLAIM_DETAILS,
    CLAIM_ID,
    CLAIM_STATUS,
    CLAIM_SUBJECT,
    CLAIM_TYPE,
)
# 这一行从另一个地方导入了一些变量，它们代表数据里的不同列名，比如描述、详情、ID、状态、主题和类型。

# 下面这部分是版权声明，告诉我们这段代码的版权信息。

# 然后是这个模块的注释，说明里面包含了哪些方法。

@verb(name="prepare_community_reports_claims")
# 这是一个装饰器，表示下面定义的函数是用来处理数据的。

def prepare_community_reports_claims(
    input: VerbInput,
    to: str = CLAIM_DETAILS,
    id_column: str = CLAIM_ID,
    description_column: str = CLAIM_DESCRIPTION,
    subject_column: str = CLAIM_SUBJECT,
    type_column: str = CLAIM_TYPE,
    status_column: str = CLAIM_STATUS,
    **_kwargs,
) -> TableContainer:
    # 这个函数叫做"prepare_community_reports_claims"，它接收一些参数，比如数据输入(input)和不同列的名称。
    # 函数返回一个TableContainer对象。

    # 获取输入的数据
    claim_df: pd.DataFrame = cast(pd.DataFrame, input.get_input())
    # 把所有缺失的描述值替换为"No Description"
    claim_df = claim_df.fillna(value={description_column: _MISSING_DESCRIPTION})

    # 创建一个新的列，把五个列的信息合并成一个字典
    claim_df[to] = claim_df.apply(
        # 对每行数据进行操作
        lambda x: {
            id_column: x[id_column],  # ID
            subject_column: x[subject_column],  # 主题
            type_column: x[type_column],  # 类型
            status_column: x[status_column],  # 状态
            description_column: x[description_column],  # 描述
        },
        axis=1,
    )

    # 返回处理后的数据
    return TableContainer(table=claim_df)

