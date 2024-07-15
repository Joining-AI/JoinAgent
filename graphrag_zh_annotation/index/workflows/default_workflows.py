# 导入WorkflowDefinitions模块，这个模块可能定义了一些工作流程的规则
from .typing import WorkflowDefinitions

# 从.v1.create_base_documents模块导入build_steps函数，这个函数可能用于创建基础文档的步骤
from .v1.create_base_documents import (
    build_steps as build_create_base_documents_steps,
)

# 同样从.v1.create_base_documents模块导入workflow_name，这可能是基础文档创建的工作流程名称
from .v1.create_base_documents import (
    workflow_name as create_base_documents,
)

# 接下来几行代码与上面类似，都是导入不同模块中用于创建不同部分的函数和工作流程名称
# ...
# ...
# ...
# 这里省略了重复的解释，每个模块都涉及创建特定内容的步骤和相应的工作流程名称

# 从.v1.join_text_units_to_relationship_ids模块导入build_steps函数，用于将文本单位与关系ID连接的步骤
from .v1.join_text_units_to_relationship_ids import (
    build_steps as join_text_units_to_relationship_ids_steps,
)

# 同样从.v1.join_text_units_to_relationship_ids模块导入workflow_name，这是将文本单位与关系ID连接的工作流程名称
from .v1.join_text_units_to_relationship_ids import (
    workflow_name as join_text_units_to_relationship_ids,
)

# 这段代码是微软公司的一个Python程序，它使用了MIT许可证。
# 注释：这是定义一些默认工作流程的包。

# 引入WorkflowDefinitions类型，可能是一个字典来存储工作流
from .typing import WorkflowDefinitions

# 从.v1.create_base_documents模块导入创建基础文档的步骤构建函数
from .v1.create_base_documents import (
    build_steps as build_create_base_documents_steps,
    workflow_name as create_base_documents,
)

# 从.v1.create_base_entity_graph模块导入创建基础实体图的步骤构建函数
from .v1.create_base_entity_graph import (
    build_steps as build_create_base_entity_graph_steps,
    workflow_name as create_base_entity_graph,
)

# ...类似地，以下代码导入了多个不同工作流程的步骤构建函数和工作流名称
# （为了简洁起见，这里省略了每个导入的详细解释）

# 定义一个变量default_workflows，类型为WorkflowDefinitions
default_workflows: WorkflowDefinitions = {

    # 将每个工作流程的名称（如create_base_extracted_entities）映射到其对应的步骤构建函数
    create_base_extracted_entities: build_create_base_extracted_entities_steps,
    create_base_entity_graph: build_create_base_entity_graph_steps,
    create_base_text_units: build_create_base_text_units_steps,
    create_final_text_units: build_create_final_text_units,
    create_final_community_reports: build_create_final_community_reports_steps,
    create_final_nodes: build_create_final_nodes_steps,
    create_final_relationships: build_create_final_relationships_steps,
    create_final_documents: build_create_final_documents_steps,
    create_final_covariates: build_create_final_covariates_steps,
    create_base_documents: build_create_base_documents_steps,
    create_final_entities: build_create_final_entities_steps,
    create_final_communities: build_create_final_communities_steps,
    create_summarized_entities: build_create_summarized_entities_steps,
    join_text_units_to_entity_ids: join_text_units_to_entity_ids_steps,
    join_text_units_to_covariate_ids: join_text_units_to_covariate_ids_steps,
    join_text_units_to_relationship_ids: join_text_units_to_relationship_ids_steps,
}

