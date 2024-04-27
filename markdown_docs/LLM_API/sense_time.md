# ClassDef SenseService
**SenseService**: 这个类的功能是提供与SenseTime API进行交互的服务。

该类的构造函数`__init__`接受两个参数：`version`和`refresh_interval`。`version`表示使用的SenseChat版本，默认为'SenseChat'。`refresh_interval`表示刷新token的时间间隔，默认为1700秒。在构造函数中，会初始化一些属性，包括`version`、`base_url`、`ak`、`sk`、`authorization`、`refresh_interval`、`timer`、`lock`和`total_tokens_used`。

**generate_jwt_token**: 这个方法用于生成JWT token。它首先定义了headers和payload，然后使用`jwt.encode`方法生成token并返回。

**refresh_token**: 这个方法用于刷新token。它使用`self.lock`来确保线程安全，生成新的authorization并更新`self.authorization`。如果已经存在定时器`self.timer`，则取消之前的定时器。然后创建一个新的定时器，定时调用`self.refresh_token`方法。

**send_get_request**: 这个方法用于发送GET请求。它首先定义了url和headers，然后使用`requests.get`方法发送请求并返回响应的json数据。

**ask_once**: 这个方法用于向SenseTime API发送一次对话请求。它首先定义了url、headers和payload。然后使用`requests.post`方法发送请求并返回响应的json数据。如果响应状态码为200，表示请求成功，会返回响应中的message字段的值。如果响应状态码为401，表示认证失败，会尝试重新刷新token并重新发送请求。如果重试次数超过3次，则返回认证失败的错误信息。如果响应状态码不是200或401，则返回响应的状态码。

**embed**: 这个方法用于获取文本的embedding。它首先定义了url、headers和payload。然后使用`requests.post`方法发送请求并返回响应的json数据。如果响应状态码为200，表示请求成功，会返回响应中的embedding字段的值。如果响应状态码为401，表示认证失败，会尝试重新刷新token并重新发送请求。如果重试次数超过3次，则返回认证失败的错误信息。如果响应状态码不是200或401，则返回包含错误信息的字典。

**__del__**: 这个方法在对象被销毁时调用。它使用`self.lock`来确保线程安全，如果存在定时器`self.timer`，则取消定时器。

**注意**: 在使用该类之前，需要先设置环境变量`SENSETIME_AK`和`SENSETIME_SK`，分别用于获取AK和SK。

**输出示例**:
```
{
    "message": "你好，有什么可以帮助你的吗？"
}
```
## FunctionDef __init__
**__init__**: 这个函数的功能是初始化一个对象。

在这个函数中，有以下几个关键的变量和操作：
- version: 表示版本号，默认为'SenseChat'。
- base_url: 表示API的基本URL地址。
- ak: 表示从环境变量中获取的AK值。
- sk: 表示从环境变量中获取的SK值。
- authorization: 表示授权信息，默认为None。
- refresh_interval: 表示刷新令牌的时间间隔，默认为1700。
- timer: 表示定时器对象。
- lock: 表示线程锁对象。
- refresh_token(): 表示刷新令牌的函数。
- total_tokens_used: 表示已使用的令牌数量。

在初始化对象时，会根据传入的参数进行相应的赋值操作。其中，version、refresh_interval、base_url等变量会被赋予传入的值，ak和sk会从环境变量中获取相应的值。同时，authorization、timer、lock等变量会被初始化为默认值。

在初始化完成后，会调用refresh_token()函数来刷新令牌，并将total_tokens_used初始化为0。

**注意**：在使用这段代码时，需要注意以下几点：
- 需要确保环境变量中存在SENSETIME_AK和SENSETIME_SK的值，否则ak和sk的值将为None。
- 可以根据实际需求修改version和refresh_interval的值。
- 需要确保base_url的值正确，以保证API的正常调用。
- 可以根据实际需求修改refresh_token()函数的实现，以满足自定义的刷新逻辑。
## FunctionDef generate_jwt_token
**generate_jwt_token**: 这个函数的功能是生成一个JWT令牌。

该函数首先创建了一个字典类型的headers变量，用于指定JWT的算法和类型。然后创建了一个payload变量，用于指定JWT的签发者、过期时间和生效时间。接下来使用jwt库的encode函数，将payload和headers作为参数，使用HS256算法和self.sk作为密钥，生成JWT令牌。最后将生成的令牌返回。

**注意**: 使用该代码时需要注意以下几点：
- 需要确保在调用该函数之前已经设置了self.ak和self.sk的值，分别作为JWT的签发者和密钥。
- 生成的JWT令牌的有效期为30分钟。

**输出示例**:
"eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiYWRtaW4iLCAiZXhwIjogMTYyMzQ1MzEwMCwgIm5iZiI6ICIxNjIzNDUyOTk5In0.8Qy5n3cX5r3Yy7s7O7XU6vU3g9kQX7l3m3W6c3a3x3c"
## FunctionDef refresh_token
**refresh_token**: 这个函数的功能是刷新令牌。在调用该函数时，它会使用一个锁来确保线程安全。首先，它会调用generate_jwt_token()函数生成一个JWT令牌，并将其赋值给authorization变量。然后，它会检查timer变量是否存在，如果存在，则取消之前的定时器。接下来，它会创建一个新的定时器，使用refresh_interval参数作为定时器的时间间隔，并将refresh_token函数作为回调函数。最后，它会启动定时器，使refresh_token函数在指定的时间间隔后再次被调用。

**注意**: 在使用该代码时需要注意以下几点：
- 由于该函数使用了锁来确保线程安全，因此在调用该函数时需要注意避免死锁的情况。
- 在调用该函数之前，需要确保已经正确设置了ak和sk变量，否则将无法生成有效的JWT令牌。
- 在调用该函数之前，需要确保已经正确设置了refresh_interval参数，以确保定时器能够按照预期的时间间隔执行刷新操作。
- 在调用该函数之后，可以通过访问authorization变量来获取最新的令牌值，以便在后续的API请求中使用。
## FunctionDef send_get_request
**send_get_request**: 这个函数的功能是发送一个GET请求到指定的URL，并返回响应的JSON数据。

该函数首先定义了一个URL变量，指定了请求的目标地址。然后定义了一个headers变量，包含了请求的头部信息，其中包括了授权信息和内容类型。

接下来，使用requests库发送了一个GET请求，传入了URL和headers参数。发送请求后，将返回的响应保存在response变量中。

最后，使用print函数打印出响应的JSON数据。

**注意**: 使用该代码时需要注意以下几点：
- 需要安装requests库，可以使用pip install requests命令进行安装。
- 需要确保authorization属性已经正确设置，否则请求将无法通过授权验证。

**输出示例**:
{
    "status": "success",
    "data": {
        "models": [
            {
                "id": "1",
                "name": "model1"
            },
            {
                "id": "2",
                "name": "model2"
            },
            {
                "id": "3",
                "name": "model3"
            }
        ]
    }
}
## FunctionDef ask_once
**ask_once**: 这个函数的功能是向模型发送一条消息并获取模型的回复。

该函数接受以下参数：
- messages: 要发送给模型的消息内容。
- know_ids: 知识库的ID列表。
- max_new_tokens: 生成的回复的最大token数量。
- n: 生成回复的数量。
- repetition_penalty: 控制生成回复中重复内容的惩罚力度。
- stream: 是否以流式方式生成回复。
- temperature: 控制生成回复的随机性。
- top_p: 控制生成回复的概率分布。
- user: 用户信息。
- knowledge_config: 知识库配置。
- plugins: 插件配置。
- retry_count: 重试次数。

函数内部的实现逻辑如下：
1. 构建请求的URL和请求头。
2. 构建请求的payload，包括消息内容、模型版本、生成回复的数量等信息。
3. 发送POST请求，将payload转换为JSON格式，并附带请求头。
4. 解析响应数据，提取出回复的消息内容和使用的token数量。
5. 根据响应的状态码进行相应的处理：
   - 如果状态码为200，表示请求成功，打印使用的token数量，并返回回复的消息内容。
   - 如果状态码为401，表示身份验证失败，判断重试次数是否小于3，如果是，则刷新token并重新发送请求；如果不是，则返回身份验证失败的错误信息。
   - 其他状态码，直接返回状态码。

**注意**：在使用该函数时需要注意以下几点：
- 需要提供有效的模型授权信息。
- 可以通过设置参数来控制生成回复的质量和数量。
- 如果身份验证失败，会自动尝试重新发送请求，最多重试3次。

**输出示例**：
```
{
    "message": "这是模型的回复消息",
    "total_tokens_used": 100
}
```
## FunctionDef embed
**embed**: 这个函数的功能是将输入的文本嵌入到指定的模型中，并返回嵌入向量。

这个函数接受三个参数：
- input_text（可选）：要嵌入的文本。默认为None。
- model：要使用的模型的名称。默认为'nova-embedding-stable'。
- retry_count：重试次数。默认为0。

在函数内部，首先构建了请求的URL和请求头。然后，根据传入的参数构建了请求的payload。接下来，使用POST方法发送请求，并将返回的结果存储在response变量中。

如果返回的状态码为200，表示请求成功。则从返回的数据中提取出嵌入向量，并将其返回。

如果返回的状态码为401，表示身份验证失败。在这种情况下，函数会尝试重新获取令牌，并递归调用自身，直到重试次数达到3次为止。如果重试次数超过3次，则返回一个包含错误信息的字典。

如果返回的状态码不是200或401，则返回一个包含错误信息的字典，其中包含返回的状态码。

**注意**：在使用这段代码时需要注意以下几点：
- 需要确保已经正确设置了base_url和authorization属性。
- 如果输入的文本为空，则返回的嵌入向量也会为空。
- 如果模型名称不正确或不存在，则返回的嵌入向量也会为空。

**输出示例**：
```
{
    "embedding": {
        "vector": [0.1, 0.2, 0.3, ...]
    }
}
```
## FunctionDef __del__
**__del__**: 此函数的功能是在对象被销毁时执行一些操作。

在这段代码中，`__del__`函数被用于定义一个对象的析构函数。析构函数是在对象被销毁时自动调用的函数，用于执行一些清理操作或释放资源。在这个函数中，首先使用`with`语句获取了`self.lock`的锁，以确保在执行清理操作时不会被其他线程干扰。然后，通过判断`self.timer`是否存在，来决定是否执行取消定时器的操作。如果`self.timer`存在，则调用`cancel()`方法取消定时器。

需要注意的是，析构函数的调用是由Python的垃圾回收机制自动触发的，无法手动调用。当对象不再被引用时，垃圾回收机制会自动调用析构函数来销毁对象。在析构函数中，可以执行一些清理操作，如关闭文件、释放资源等。

**注意**：在编写析构函数时，需要注意以下几点：
- 析构函数的命名固定为`__del__`，不能更改。
- 析构函数没有参数，只有一个`self`参数，用于引用当前对象。
- 析构函数的执行时机是在对象被销毁时，无法手动调用。
- 析构函数中应该只执行一些清理操作或释放资源的操作，不应该进行复杂的计算或调用其他对象的方法。
***
