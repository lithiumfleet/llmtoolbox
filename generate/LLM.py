from aiohttp import ClientSession
from asyncio import Queue
from queue import PriorityQueue
import asyncio
from dataclasses import dataclass, field
from heapq import heapify, heappush, heappop

@dataclass
class Req:
    req_id: int
    req: dict

@dataclass
class Resp:
    resp_id: int
    resp: str


class LLM:
    """
    LLM is a forwarding proxy controls the max concurrency.
    
    use `llm(req)` will add the request to queue and send.
    """

    def __init__(self, url:str, apikey:str, max_concurrency:int):
        self.url = url
        self.apikey = apikey
        self.req_pool = Queue(max_concurrency)
        self.exit_flag = False # this flag can notify the _run function, flag will set to True at the end of handling the last request
        self.resp_buffer = [] * max_concurrency
        self.index_manager = [i for i in range(max_concurrency)] # indexes that are not used yet
        heapify(self.index_manager)

    @classmethod
    def connect(cls, url:str, apikey:str="sk-", max_concurrency:int=50):
        return cls(url, apikey, max_concurrency)

    def __enter__(self):
        self.session = ClientSession(self.url)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        asyncio.run(self.session.close())

    async def _run(self):
        """
        clear the req_pool in background.
        """
        if not self.exit_flag:
            # 死循环直到某个任务触发了退出条件
            # 返回的结果会存到resp_buffer中, resp_buffer是数组, 附带一个用堆实现的序号管理器
            return await asyncio.wait(self.req_pool, return_when=asyncio.FIRST_COMPLETED)
        raise RuntimeError("no tasks")
    
    async def recv_resp(self, req_id:int) -> Resp:
        resp = Resp(-1, "")
        while resp.resp_id != req_id:
            resp = await self._run()
        return resp


    async def _send(self, req:Req) -> Resp:
        resp = await self.session.post("/v1/chat/completions", json=req)
        return Resp(req.req_id, await resp.text())

    async def add_req(self, req:dict) -> int:
        req_id = heappop(self.index_manager) # FIXME: empty index not considered
        await self.req_pool.put(asyncio.create_task(self._send(Req(req_id, req))))
        return req_id

    async def __call__(self, req:dict) -> dict:
        """
        call with openai-api compatible payload.

        for example:

        req = {
            "model": <model name>,
            "messages": [
                {
                    "role": "user",
                    "content": <your prompt>
                }
            ],
            "temperature": 0.8
        }
        """
        req_id = await self.add_req(req)
        return await self.recv_resp(req_id)
        
    