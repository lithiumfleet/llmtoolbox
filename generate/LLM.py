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
        self.session = None

    @classmethod
    def connect(cls, url:str, apikey:str="sk-", max_concurrency:int=50):
        return cls(url, apikey, max_concurrency)

    async def __aenter__(self):
        if self.session is None:
            self.session = ClientSession(base_url=self.url, headers={"Authorization": f"{self.apikey}"})
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        self.session.close()
        self.session = None

    async def _send(self, req:Req) -> Resp:
        async with self.session.post("/v1/chat/completions", json=req.req) as resp:
            return Resp(req.req_id, await resp.json())

    # async def add_req(self, req:dict) -> int:
    #     req_id = heappop(self.index_manager) # FIXME: empty index not considered
    #     await self.req_pool.put(asyncio.create_task(self._send(Req(req_id, req))))
    #     return req_id

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
        # req_id = await self.add_req(req)
        # return await self.recv_resp(req_id)
        # 容我先把串行跑通
        return await self._send(Req(0, req))


        
    