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

**简述:**
这是一个造数据的pipline, 所以输入和输出都应该是文件.
+ 输入: lines of prompt / text chunck
+ 输出: **仅输出vicuna格式的偏好数据**

**常见的造数据pipline**
这样可以反映需求. chain结尾都是数据集.
1. prompts --> evol-instruction --> more prompts --> ds
2. text chuncks --> QAs / dialogues
3. ds --> 改写ds(如语气改写)
4. texts --> text chuncks(for world book)
5. (for continueal pretraining task) ?

**可能的组件以及特点:**
+ LLM: 所有的post请求都会非阻塞地立刻发送.
+ PromptPool(自动化扩充): 使用Evol-instruction扩充prompt
+ Message: 