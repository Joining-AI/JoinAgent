# 导入json库，用于处理JSON格式的数据
import json

# 导入logging库，用于记录程序运行日志
import logging

# 导入traceback库，用于捕获和打印异常堆栈信息
import traceback

# 导入VerbCallbacks类，它可能用于处理数据操作的回调函数
from datashaper import VerbCallbacks

# 从graphrag.config.enums模块导入LLMType枚举，定义了不同类型的LLM（Language-Learning Model）
from graphrag.config.enums import LLMType

# 从graphrag.index.cache模块导入PipelineCache类，用于缓存数据管道
from graphrag.index.cache import PipelineCache

# 从graphrag.index.graph.extractors.community_reports模块导入CommunityReportsExtractor类，用于提取社区报告
from graphrag.index.graph.extractors.community_reports import CommunityReportsExtractor

# 从graphrag.index.llm模块导入load_llm函数，用于加载语言学习模型
from graphrag.index.llm import load_llm

# 从graphrag.index.utils.rate_limiter模块导入RateLimiter类，用于限制请求速率
from graphrag.index.utils.rate_limiter import RateLimiter

# 从graphrag.index.verbs.graph.report.strategies.typing模块导入CommunityReport和StrategyConfig类，它们可能是策略配置和报告结构
from graphrag.index.verbs.graph.report.strategies.typing import CommunityReport, StrategyConfig

# 从graphrag.llm模块导入CompletionLLM类，表示完成型的语言学习模型
from graphrag.llm import CompletionLLM

# 从当前模块的子模块.defaults导入MOCK_RESPONSES，可能是一个模拟的响应数据
from .defaults import MOCK_RESPONSES

# 使用logging库设置名为__name__的日志器（通常是当前模块的名称）
log = logging.getLogger(__name__)

# 定义异步函数run，用于执行图智能实体提取策略
async def run(
    # 参数community：社区的标识，可以是字符串或整数
    community: str | int,
    # 参数input：输入的字符串
    input: str,
    # 参数level：提取的级别
    level: int,
    # 参数reporter：回调函数对象，用于报告操作状态
    reporter: VerbCallbacks,
    # 参数pipeline_cache：数据管道缓存对象
    pipeline_cache: PipelineCache,
    # 参数args：策略配置对象
    args: StrategyConfig,
) -> CommunityReport | None:
    """执行图情报实体提取策略的函数"""
    
    # 从配置args中获取llm配置，如果没有则使用默认值
    llm_config = args.get(
        "llm", {"type": LLMType.StaticResponse, "responses": MOCK_RESPONSES}
    )
    
    # 获取llm类型，如果没有则使用默认值
    llm_type = llm_config.get("type", LLMType.StaticResponse)
    
    # 根据llm_type加载相应的语言学习模型
    llm = load_llm(
        "community_reporting", llm_type, reporter, pipeline_cache, llm_config
    )
    
    # 调用内部函数运行提取器并返回结果
    return await _run_extractor(llm, community, input, level, args, reporter)

# 定义一个异步函数（等待执行的任务）
async def _run_extractor(
    llm: CompletionLLM,  # 接受一个名为llm的特殊语言模型对象
    community: str | int,  # 接受社区的名称或编号
    input: str,  # 接受一段输入的文字
    level: int,  # 接受一个整数级别的信息
    args: StrategyConfig,  # 接受一个包含策略配置的参数对象
    reporter: VerbCallbacks,  # 接受一个用于报告错误和状态的对象
) -> CommunityReport | None:  # 函数返回一个社区报告或者None
    # 创建一个限速器，每60秒只能执行一次
    rate_limiter = RateLimiter(rate=1, per=60)

    # 创建一个用于提取社区报告的工具
    extractor = CommunityReportsExtractor(
        llm,  # 使用之前传入的语言模型对象
        extraction_prompt=args.get("extraction_prompt", None),  # 提取提示，如果配置中没有就设为None
        max_report_length=args.get("max_report_length", None),  # 最大报告长度，如果没有就设为None
        on_error=lambda e, stack, _data: reporter.error(  # 当出错时，报告错误
            "Community Report Extraction Error", e, stack
        ),
    )

    # 尝试获取限速器的许可并执行提取操作
    try:
        await rate_limiter.acquire()  # 等待限速器允许执行
        results = await extractor({"input_text": input})  # 使用提取工具处理输入文字
        report = results.structured_output  # 获取结构化的报告数据

        # 如果报告为空或没有内容，则记录警告并返回None
        if report is None or len(report.keys()) == 0:
            log.warning("No report found for community: %s", community)
            return None

        # 创建并返回一个社区报告对象
        return CommunityReport(
            community=community,
            full_content=results.output,  # 报告的完整内容
            level=level,  # 信息级别
            rank=_parse_rank(report),  # 解析并返回报告的评分
            title=report.get("title", f"Community Report: {community}"),  # 报告标题，如果没有就用社区名
            rank_explanation=report.get("rating_explanation", ""),  # 评分解释，如果没有就为空字符串
            summary=report.get("summary", ""),  # 报告摘要，如果没有就为空字符串
            findings=report.get("findings", []),  # 报告发现，如果没有就为空列表
            full_content_json=json.dumps(report, indent=4),  # 报告的JSON格式，便于阅读
        )
    # 捕获并处理异常
    except Exception as e:
        log.exception("Error processing community: %s", community)  # 记录处理社区时的错误
        reporter.error("Community Report Extraction Error", e, traceback.format_exc())  # 报告错误
        return None  # 返回None表示处理失败

# 定义一个辅助函数，从报告字典中解析并返回评分，如果解析失败则返回-1
def _parse_rank(report: dict) -> float:
    rank = report.get("rating", -1)  # 获取评分，如果没有就设为-1
    try:
        return float(rank)  # 尝试将评分转换为浮点数并返回
    except ValueError:  # 如果转换失败
        log.exception("Error parsing rank: %s defaulting to -1", rank)  # 记录错误
        return -1  # 返回-1作为默认评分

