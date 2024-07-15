

# 这个代码定义了一个名为ClaimExtractor的类，它用于从文本中提取声明（claim）信息。

class ClaimExtractor:
    # 这是类的文档字符串，描述了这个类的作用。
    """Claim extractor class definition."""

    # 下面是一些类变量，它们是类的属性，每个都有一个描述性的名字。
    _llm: CompletionLLM       # 用于完成任务的语言模型
    _extraction_prompt: str   # 提取声明时使用的提示
    _summary_prompt: str      # （未使用）
    _output_formatter_prompt: str   # （未使用）
    _input_text_key: str      # 输入文本的键名
    _input_entity_spec_key: str   # 输入实体规格的键名
    _input_claim_description_key: str  # 输入声明描述的键名
    _tuple_delimiter_key: str     # 元组分隔符的键名
    _record_delimiter_key: str   # 记录分隔符的键名
    _completion_delimiter_key: str  # 完成分隔符的键名
    _max_gleanings: int        # 最大提取次数
    _on_error: ErrorHandlerFn  # 错误处理函数

    # 这是类的初始化方法，用于创建 ClaimExtractor 对象时设置属性。
    def __init__(self,
                 llm_invoker: CompletionLLM,         # 传入的语言模型
                 extraction_prompt: str | None = None,  # 提示，如果没有则使用默认值
                 input_text_key: str | None = None,   # 输入文本键名，如果没有则使用默认值
                 input_entity_spec_key: str | None = None,  # 实体规格键名，如果没有则使用默认值
                 input_claim_description_key: str | None = None,  # 声明描述键名，如果没有则使用默认值
                 input_resolved_entities_key: str | None = None,  # 解析后的实体键名，如果没有则使用默认值
                 tuple_delimiter_key: str | None = None,   # 元组分隔符键名，如果没有则使用默认值
                 record_delimiter_key: str | None = None,  # 记录分隔符键名，如果没有则使用默认值
                 completion_delimiter_key: str | None = None,  # 完成分隔符键名，如果没有则使用默认值
                 encoding_model: str | None = None,   # 编码模型，如果没有则使用默认值
                 max_gleanings: int | None = None,     # 最大提取次数，如果没有则使用默认值
                 on_error: ErrorHandlerFn | None = None,  # 错误处理函数，如果没有则使用默认值
    ):
        # 设置类的属性
        self._llm = llm_invoker
        self._extraction_prompt = extraction_prompt or CLAIM_EXTRACTION_PROMPT
        self._input_text_key = input_text_key or "input_text"
        self._input_entity_spec_key = input_entity_spec_key or "entity_specs"
        self._tuple_delimiter_key = tuple_delimiter_key or "tuple_delimiter"
        self._record_delimiter_key = record_delimiter_key or "record_delimiter"
        self._completion_delimiter_key = (
            completion_delimiter_key or "completion_delimiter"
        )
        self._input_claim_description_key = (
            input_claim_description_key or "claim_description"
        )
        self._input_resolved_entities_key = (
            input_resolved_entities_key or "resolved_entities"
        )
        self._max_gleanings = (
            max_gleanings if max_gleanings is not None else defs.CLAIM_MAX_GLEANINGS
        )
        self._on_error = on_error or (lambda _e, _s, _d: None)

        # 构建循环参数
        encoding = tiktoken.get_encoding(encoding_model or "cl100k_base")  # 获取编码模型
        yes = encoding.encode("YES")  # "YES"的编码
        no = encoding.encode("NO")   # "NO"的编码
        self._loop_args = {"logit_bias": {yes[0]: 100, no[0]: 100}, "max_tokens": 1}  # 用于语言模型的参数

    # 当对象被调用时执行的方法
    async def __call__(self, inputs: dict[str, Any], prompt_variables: dict | None = None) -> ClaimExtractorResult:
        # 如果没有提供提示变量，则使用空字典
        if prompt_variables is None:
            prompt_variables = {}
        
        # 获取输入文本、实体规格和声明描述
        texts = inputs[self._input_text_key]
        entity_spec = str(inputs[self._input_entity_spec_key])
        claim_description = inputs[self._input_claim_description_key]
        resolved_entities = inputs.get(self._input_resolved_entities_key, {})

        # 初始化结果和源文档映射
        all_claims: list[dict] = []
        source_doc_map = {}

        # 创建提示参数
        prompt_args = {...}

        # 遍历每份文本，提取声明并清洗
        for 文本编号, text in enumerate(texts):
            文档ID = f"d{文本编号}"
            try:
                # 提取文档中的声明
                claims = await self._process_document(prompt_args, text, 文本编号)
                # 清洗并添加到结果列表
                all_claims += [self._clean_claim(c, 文档ID, resolved_entities) for c in claims]
                # 将源文本添加到源文档映射
                source_doc_map[文档ID] = text
            except Exception as e:
                # 记录错误并调用错误处理函数
                log.exception("error extracting claim")
                self._on_error(e, traceback.format_exc(), {"doc_index": 文本编号, "text": text})
                continue

        # 返回结果
        return ClaimExtractorResult(output=all_claims, source_docs=source_doc_map)

    # 清洗提取的声明
    def _clean_claim(self, claim: dict, document_id: str, resolved_entities: dict) -> dict:
        # 更新声明中的subject_id和object_id
        ...（略）

    # 处理单个文档以提取声明
    async def _process_document(self, prompt_args: dict, doc, doc_index: int) -> list[dict]:
        # 获取记录和完成分隔符
        record_delimiter = ...
        completion_delimiter = ...

        # 使用语言模型进行第一次提取
        response = await self._llm(...
        # 处理结果
        claims = ...

        # 循环提取更多声明
        for i in range(self._max_gleanings):
            # 提取扩展信息
            ...
            # 检查是否继续循环
            ...

        # 解析提取的声明
        result = self._parse_claim_tuples(results, prompt_args)
        for r in result:
            r["doc_id"] = f"{doc_index}"
        return result

    # 解析声明元组
    def _parse_claim_tuples(self, claims: str, prompt_variables: dict) -> list[dict[str, Any]]:
        # 定义分隔符
        record_delimiter = ...
        completion_delimiter = ...
        tuple_delimiter = ...

        # 解析并返回结果
        result = []
        for 声明 in claims.split(record_delimiter):
            # 提取字段
            ...
            result.append(声明信息)
        return result

