# 导入一些必要的工具包，让程序能处理数据和类型
from collections.abc import Iterable  # 用于检查是否可以迭代（比如列表、元组）
from typing import Any  # 表示任何类型的变量
from datashaper import VerbCallbacks  # 用于处理操作反馈的类
import graphrag.config.defaults as defs  # 引入默认配置
from graphrag.config.enums import LLMType  # 定义语言模型类型的枚举
from graphrag.index.cache import PipelineCache  # 用于缓存的类
from graphrag.index.graph.extractors.claims import ClaimExtractor  # 提取声明的类
from graphrag.index.llm import load_llm  # 加载语言模型的函数
from graphrag.index.verbs.covariates.typing import (  # 定义数据类型的模块
    Covariate,
    CovariateExtractionResult,
)
from graphrag.llm import CompletionLLM  # 完成型语言模型类
from .defaults import MOCK_LLM_RESPONSES  # 引入模拟的LLM响应数据

# 这段文字是版权信息和许可说明

# 定义一个模块，包含run和_run_chain方法

# 从collections.abc导入Iterable，用于检查是否可迭代
# 从typing导入Any，表示任何类型的数据
# 从datashaper导入VerbCallbacks，处理反馈的类
# 从graphrag的配置部分导入默认设置
# 从枚举中导入LLMType，定义语言模型类型
# 从缓存部分导入PipelineCache类
# 从图提取部分导入ClaimExtractor类，用于提取声明
# 从LLM部分导入load_llm函数，加载语言模型
# 从数据类型定义部分导入Covariate和CovariateExtractionResult
# 从当前模块的默认设置导入MOCK_LLM_RESPONSES，模拟的LLM响应

# 定义一个异步函数run，用于运行声明提取链
async def run(
    input: str | Iterable[str],  # 输入可以是一个字符串或一组字符串
    entity_types: list[str],  # 实体类型列表
    resolved_entities_map: dict[str, str],  # 解析后的实体映射字典
    reporter: VerbCallbacks,  # 用于报告进度的对象
    pipeline_cache: PipelineCache,  # 缓存对象
    strategy_config: dict[str, Any],  # 策略配置字典
) -> CovariateExtractionResult:  # 返回的结果类型
    # 从策略配置中获取LLM配置，如果没有就用默认的静态响应
    llm_config = strategy_config.get(
        "llm", {"type": LLMType.StaticResponse, "responses": MOCK_LLM_RESPONSES}
    )
    # 获取LLM类型，如果没有就用默认的静态响应
    llm_type = llm_config.get("type", LLMType.StaticResponse)
    # 根据类型加载LLM
    llm = load_llm("claim_extraction", llm_type, reporter, pipeline_cache, llm_config)
    # 调用内部函数执行操作
    return await _execute(
        llm,  # 加载的语言模型
        input,  # 输入数据
        entity_types,  # 实体类型列表
        resolved_entities_map,  # 解析后的实体映射
        reporter,  # 进度报告对象
        strategy_config,  # 策略配置
    )

# 定义一个异步函数，用于执行一些操作
async def _execute(
    # 输入参数，它们代表不同的含义
    llm: CompletionLLM,  # 一个用于完成任务的模型
    texts: Iterable[str],  # 一组文本
    entity_types: list[str],  # 实体类型的列表
    resolved_entities_map: dict[str, str],  # 解析后的实体映射字典
    reporter: VerbCallbacks,  # 报告器，用于报告错误信息
    strategy_config: dict[str, Any],  # 策略配置，包含各种设置
) -> CovariateExtractionResult:  # 返回值类型，表示提取结果

    # 从策略配置中获取提取提示
    extraction_prompt = strategy_config.get("extraction_prompt")
    # 获取最大收获数量，默认值是 CLAIM_MAX_GLEANINGS
    max_gleanings = strategy_config.get("max_gleanings", defs.CLAIM_MAX_GLEANINGS)
    # 获取元组分隔符
    tuple_delimiter = strategy_config.get("tuple_delimiter")
    # 获取记录分隔符
    record_delimiter = strategy_config.get("record_delimiter")
    # 获取完成分隔符
    completion_delimiter = strategy_config.get("completion_delimiter")
    # 获取编码模型名称
    encoding_model = strategy_config.get("encoding_name")

    # 创建一个用于提取声明的类实例
    extractor = ClaimExtractor(
        llm_invoker=llm,  # 使用前面的模型
        extraction_prompt=extraction_prompt,  # 提取提示
        max_gleanings=max_gleanings,  # 最大收获数量
        encoding_model=encoding_model,  # 编码模型
        on_error=lambda e, s, d: (  # 错误处理函数
            reporter.error("Claim Extraction Error", e, s, d) if reporter else None
        ),
    )

    # 检查是否提供了声明描述，如果没有，则抛出错误
    claim_description = strategy_config.get("claim_description")
    if claim_description is None:
        msg = "claim_description is required for claim extraction"
        raise ValueError(msg)

    # 如果 texts 是字符串，将其转换为列表
    texts = [texts] if isinstance(texts, str) else texts

    # 调用提取器进行处理，并等待结果
    results = await extractor({
        # 提供给提取器所需的各种数据
        "input_text": texts,
        "entity_specs": entity_types,
        "resolved_entities": resolved_entities_map,
        "claim_description": claim_description,
        "tuple_delimiter": tuple_delimiter,
        "record_delimiter": record_delimiter,
        "completion_delimiter": completion_delimiter,
    })

    # 获取提取结果中的输出数据
    claim_data = results.output

    # 将每个数据项转换为协变量并返回
    return CovariateExtractionResult([create_covariate(item) for item in claim_data])

# 定义一个名为create_covariate的函数，它接受一个字典作为参数，字典里的键是字符串，值可以是任何类型
def create_covariate(item: dict[str, Any]) -> Covariate:
    # 这个函数的作用是从传入的字典中创建一个Covariate对象
    """Create a covariate from the item."""
    
    # 创建并返回一个新的Covariate对象，用括号里的内容初始化它
    # 下面每一行都是设置Covariate对象的一个属性，这些属性的名字来自字典中的键，值来自字典中的对应项
    return Covariate(
        # 主体ID，从字典的"subject_id"键获取
        subject_id=item.get("subject_id"),
        
        # 主体类型，从字典的"subject_type"键获取
        subject_type=item.get("subject_type"),
        
        # 对象ID，从字典的"object_id"键获取
        object_id=item.get("object_id"),
        
        # 对象类型，从字典的"object_type"键获取
        object_type=item.get("object_type"),
        
        # 类型，从字典的"type"键获取
        type=item.get("type"),
        
        # 状态，从字典的"status"键获取
        status=item.get("status"),
        
        # 开始日期，从字典的"start_date"键获取
        start_date=item.get("start_date"),
        
        # 结束日期，从字典的"end_date"键获取
        end_date=item.get("end_date"),
        
        # 描述，从字典的"description"键获取
        description=item.get("description"),
        
        # 来源文本，从字典的"source_text"键获取
        source_text=item.get("source_text"),
        
        # 文档ID，从字典的"doc_id"键获取
        doc_id=item.get("doc_id"),
        
        # 记录ID，从字典的"record_id"键获取
        record_id=item.get("record_id"),
        
        # ID，从字典的"id"键获取
        id=item.get("id"),
    )

