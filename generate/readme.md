## dataset generator

使用异步并发, 充分利用vllm的大吞吐量优势快速造数据.

架构上类似langchain.

> 话说langchain好像支持异步...https://python.langchain.com/docs/modules/callbacks/async_callbacks/


## RP自留地

毕竟做这个的初衷就是RP...现在大半是为了Mira做准备. 一般来说数据质量高于一切. 所以如果手里数据不够好用这个姓名还是无济于事...

https://www.reddit.com/r/LocalLLaMA/comments/191bufg/currently_working_on_building_a_worldbuildrp/ --> https://huggingface.co/VatsaDev

https://www.reddit.com/r/PygmalionAI/comments/17fr9w3/i_made_a_new_rp_dataset_78k_replies_humanwritten/ --> https://github.com/e-p-armstrong/amadeus

看起来还是怎么输入怎么输出... --> https://www.reddit.com/r/LocalLLaMA/comments/1bho5x8/is_it_better_to_train_with_a_text_corpus_and_then/


## miniLC

**简述**

这是一个造数据的pipline. 在llm造数据的pipline中网络延时和llm推理延时不可忽略.

现在我们无论是vllm还是外部api都是在大并发量时才能体现优势, 所以使用异步+并发是一个很自然的选择.

+ 输入: lines of prompt / text chunck

+ 输出: **仅输出vicuna格式的偏好数据**

**更详尽的需求/场景**

大部分应该都是(prompt, chucks) => chuncks...

1. 续写: 我有一些质量高但是数量少的弱智吧数据, 我想扩充它.
2. 改写: 模型输出风格很GPT, 想使用模型用另一种语气/风格改写某个数据集做微调.
3. 改写(抽取): 从书里抽问题, 这样模型每次碰到医学类问题都会显得很专业. (从以往经验来看很不靠谱)
4. 续写: 我想把prompt后的大模型能力蒸馏到小模型上, 找一批问题, 让模型回答.

现在看来只有两种需求: 扩写和改写, 其实也就是prompt不同罢了

**结构**

+ Task: 主函数s
+ LLM: 提供一个上下文管理器, 使用方法在下面.
+ Chain: langchain的乞丐版本
+ State: 辅助类

**细节**

Q1

chain.invoke目前是直接执行函数, 且参数只有state. 这样编写环节中的函数起来不舒服(限定一个参数且不适合检查).
如果改成前一个函数返回值直接给下一个函数则不适合跨环节传参

A1

~~在invoke间隐式地调用pipe, 下一个函数的输入由pipe函数给定.~~
~~pipe函数会从"上一个函数的输出"到chain.state的顺序搜索, 然后传递给下一个函数.~~
~~搜索方法是按位置搜索.~~
要是真这样写就完蛋了, 搜索绝对是个问题.
目前异步操作就一个llm的调用, 直接针对它设置规则就行了

**使用**

```python
async main():
    with LLM.connect(my_server_url, apikey, max_concurrency) as llm:
        chain1 = LLMChain(prepare, llm, after)
        chain2 = Chain(func1, func2, func3, llm, func4, chain2)
        await asyncio.gather(*[chain2.invoke(initstate(item)) for item in items])

asyncio.run(main())
```

要点:

1. chain.invoke只接收State.
2. 记得在gather前加上await.
3. 每个chain中的chain会继承当前state.
4. LLMChain只是为了方便三段式处理llm输入输出.
