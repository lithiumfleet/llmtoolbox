from asyncio import sleep
from aiohttp import ClientSession
from State import State
from datasets import load_dataset, Dataset

# basic functions
async def llm(state:State):
    if not state.has('session'):
        state.session = ClientSession(state.url)
    state.resp = await state.session.post("/v1/chat/completions",json=state.payload)
    state.resp = await state.resp.text()

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
    print(f"""
[input]     {state.question}
[original]  {state.answer}
[rewrite]   {state.resp}""")






def fun1(state):
    state.url = "http://127.0.0.1:9880"
    state.model = "Qwen1.5-14B-Chat"
    state.payload = {
        "model": state.model,
        "messages": [
            {
                "role": "user",
                "content": "以外星飞船降落在地球上为题写一个短篇小说."
            }
        ],
        "temperature": 0.8
    }

async def fun2(state):
    await llm(state)

async def fun3(state):
    # print(f"state in func3: {state.resp}", flush=True)
    await state.session.close()