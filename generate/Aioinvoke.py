from Chain import Chain
from State import State
from LLM import LLM
from Task import *
import asyncio

# current: 
# a specific task, rewrite ruozhiba ds with argumented tone.
# more general pipline is still in developing...

async def rewrite_ruozhiba():
    url = "http://localhost:9880"
    req1 = {
            "model": "Qwen/Qwen1.5-1.8B-Chat-GGUF",
            "messages": [
                {
                    "role": "user",
                    "content": "hello!"
                }
            ],
            "temperature": 0.8
        }
    req2 = {
            "model": "Qwen/Qwen1.5-1.8B-Chat-GGUF",
            "messages": [
                {
                    "role": "user",
                    "content": "Write a tiny story about a llama in my yard."
                }
            ],
            "temperature": 0.8
        }
    def init(state, init_data):
        state.req = init_data
    
    async with LLM.connect(url,"lm-studio") as llm:
        chain = Chain(init, llm, print_resp)
        await asyncio.gather(chain.invoke(req1), chain.invoke(req2), chain.invoke(req1), chain.invoke(req1), chain.invoke(req2))

        


asyncio.run(rewrite_ruozhiba())