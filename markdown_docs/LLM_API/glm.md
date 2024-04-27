# ClassDef GLMService
**GLMService**: 这个类的功能是与GLM模型进行交互的服务类。

在构造函数`__init__`中，我们首先加载当前目录的.env文件，并初始化一些属性。`version`参数用于指定GLM模型的版本，默认为"glm-3-turbo"。`total_tokens_used`属性用于保存总共使用的token数量。`api_key`属性从环境变量中导入GLM_API的值，用作API密钥。`client`属性是一个ZhipuAI的实例，用于创建与GLM模型的连接。

`ask_once`方法用于向GLM模型发送请求并获取回答。该方法接受两个参数：`query`表示用户的查询字符串，`url`表示图像的URL（可选）。根据`version`的值，分别调用不同版本的GLM模型进行请求。

如果`version`为"glm-3-turbo"或"glm-4"，则使用`client.chat.completions.create`方法发送请求。请求的内容是一个包含用户角色和查询内容的字典。如果响应中存在回答，则返回回答字符串；否则返回"无法获取回答。"。同时，如果响应中存在`usage`属性，则更新`total_tokens_used`属性的值。

如果`version`不是"glm-3-turbo"或"glm-4"，则需要提供图像的URL。请求的内容是一个包含用户角色、查询内容和图像URL的字典。其他操作与上述相同。

**注意**：使用该代码时需要注意以下几点：
- 需要提前在.env文件中设置GLM_API的值作为API密钥。
- 需要确保已安装`zhipuai`库，并导入`ZhipuAI`类。

**输出示例**：
- 示例1：
  ```
  query = "你好"
  glm_service = GLMService()
  answer = glm_service.ask_once(query)
  print(answer)
  输出： "你好，我能帮助你吗？"
  ```
- 示例2：
  ```
  query = "这是什么东西？"
  url = "https://example.com/image.jpg"
  glm_service = GLMService()
  answer, error = glm_service.ask_once(query, url)
  if error:
      print(error)
  else:
      print(answer)
  输出： "这是一只猫。"
## FunctionDef __init__
**__init__**: 这个函数的功能是初始化一个对象。

这个函数接受一个可选参数version，默认值为"glm-3-turbo"。在函数体内，首先加载当前目录的.env文件。然后，将传入的version赋值给对象的version属性。接下来，将total_tokens_used属性初始化为0，用于保存总共使用的token数量。然后，从环境变量中导入名为'GLM_API'的API密钥，并将其赋值给对象的api_key属性。最后，创建一个ZhipuAI的实例，并将api_key作为参数传入，将该实例赋值给对象的client属性。

**注意**: 使用这段代码时需要注意以下几点：
- 需要确保当前目录下存在.env文件，否则会导致加载失败。
- 如果不传入version参数，则默认使用"glm-3-turbo"作为version。
- 需要在环境变量中设置名为'GLM_API'的API密钥，否则会导致api_key属性为None。
- 需要确保ZhipuAI类已经导入，否则会导致创建客户端实例失败。
## FunctionDef ask_once
**ask_once**: 这个函数的功能是使用zhipuai库向GLM-3-Turbo模型发送请求并获取回答。

该函数接受两个参数：query和url。query是用户的查询字符串，url是图像的URL。如果GLM的版本是'glm-3-turbo'或'glm-4'，则只需要提供query参数。如果GLM的版本不是这两个，还需要提供url参数。

函数首先检查GLM的版本是否是'glm-3-turbo'或'glm-4'，如果是，则使用zhipuai库的chat.completions.create方法发送请求，并将query作为用户的消息发送给模型。然后，检查响应对象的choices属性，如果存在回答，则提取第一个回答的内容，并更新token使用量。最后，返回模型的回答字符串。

如果GLM的版本不是'glm-3-turbo'或'glm-4'，则需要检查是否提供了url参数。如果没有提供url参数，则返回None和"请提供图像URL"。如果提供了url参数，则使用zhipuai库的chat.completions.create方法发送请求，并将query和url作为用户的消息发送给模型。然后，检查响应对象的choices属性，如果存在回答，则提取第一个回答的内容，并更新token使用量。最后，返回模型的回答字符串和None。

**注意**: 
- 请确保已经安装了zhipuai库，并且已经正确配置了相关的API密钥和模型版本。
- 如果GLM的版本不是'glm-3-turbo'或'glm-4'，请确保提供了正确的图像URL。

**输出示例**:
- 示例1:
  输入: query="你好"
  输出: "你好，我可以帮助你吗？"
- 示例2:
  输入: query="这是什么东西"，url="https://example.com/image.jpg"
  输出: "这是一张图片，它是一个红色的苹果。"
***
