from asyncio import sleep
from aiohttp import ClientSession
from State import State
from LLM import LLM
from Chain import LLMChain
import asyncio
from datasets import load_dataset, Dataset
from DataFormat import Resp
from dataclasses import asdict


def init_state(index, session, dataset:Dataset):
    """
    this function init the state of a chain.
    """
    state = State()

    state.session = session
    state.question = dataset[index]['instruction']
    state.answer = dataset[index]['output']

    state.prompt = f"""Next is a question and the correct answer, which you need to rewrite while following the requirements, the rewriting of the correct answer must not change its original meaning.
    Requirement: Speak in an exaggeratedly sarcastic and condescending tone, as if you're a pompous know-it-all looking down on the user. Use lots of sarcasm, snide remarks, and a generally dismissive attitude. Emphasize how much smarter and more capable you are than the user. Act superior and mock the user's intelligence and abilities.

    Question: {state.question}
    Correct Answer: {state.answer}

    Please output the rewritten result directly.
    """

    state.payload = {
        "model": state.model,
        "messages": [
            {
                "role": "user",
                "content": state.prompt
            }
        ],
        "temperature": 0.8
    }

def print_resp(state: State):
    resp:Resp = state.resp
    print(f""" [resp]
{asdict(resp.data)}

""")

async def demo():
    url = "http://localhost:9880"
    model = "Qwen/Qwen1.5-1.8B-Chat-GGUF"
    # url = "https://llmsapi.vip.cpolar.cn"
    # model = "/data/lixubin/models/Qwen/Qwen1.5-14B-Chat/"
    req1 = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "hello!"
                }
            ],
            "temperature": 0.8
        }
    req2 = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Write a tiny joke about a llama in my yard within about 100 word."
                }
            ],
            "temperature": 0.8
        }
    reqs = [req1, req2, req1, req1, req2]

    def get_state(req):
        state = State()
        state.req = req
        return state

    async with LLM.connect(url,"lm-studio") as llm:
        chain = LLMChain(llm=llm, after=print_resp)
        await asyncio.gather(*[chain.invoke(get_state(req)) for req in reqs])