from asyncio import sleep
from aiohttp import ClientSession
from State import State

# basic functions
async def llm(state:State):
    if not state.has('session'):
        state.session = ClientSession(state.url)
    state.resp = await state.session.post("/v1/chat/completions",json=state.payload)
    state.resp = await state.resp.text()

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