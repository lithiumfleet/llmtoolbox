## dataset generator

使用异步并发, 充分利用vllm的大吞吐量优势快速造数据.

架构上类似langchain.

> 话说langchain好像支持异步...https://python.langchain.com/docs/modules/callbacks/async_callbacks/


## RP自留地

毕竟做这个的初衷就是RP...现在大半是为了Mira做准备.
https://www.reddit.com/r/LocalLLaMA/comments/191bufg/currently_working_on_building_a_worldbuildrp/ --> https://huggingface.co/VatsaDev
https://www.reddit.com/r/PygmalionAI/comments/17fr9w3/i_made_a_new_rp_dataset_78k_replies_humanwritten/ --> https://github.com/e-p-armstrong/amadeus
看起来还是怎么输入怎么输出... --> https://www.reddit.com/r/LocalLLaMA/comments/1bho5x8/is_it_better_to_train_with_a_text_corpus_and_then/


## miniLC

**简述**

这是一个造数据的pipline, 所以输入和输出都应该是文件.
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

+ Task: 就是上述的几个场景的实现, 把需要调用的函数以串行的形式写入函数数组.
+ Chain: 和Aioinvoke交互, 将函数数组封装到队列中, 发送到线程池.
+ Aioinvoke: 思路和正常异步并发一致: 创建一个异步线程池(set), 限制最大并发量(检查线程池大小, 大了就用await等待), 最后等待线程池清空.

**测试**

1. qwen14b-vllm(no flash-attn)
    1 -> 0:15.96
    50 -> 0:35.46
    100 -> 1:04.79
    200 -> 2:07.16