from aiohttp import ClientSession
from asyncio import Queue
from queue import PriorityQueue
import asyncio
from dataclasses import dataclass, field
from heapq import heapify, heappush, heappop
import datetime
from State import State

@dataclass
class Req:
    id: int
    req: dict

@dataclass
class Resp:
    id: int
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
        print("opening session.")
        self.session = ClientSession(base_url=self.url, headers={"Authorization": f"{self.apikey}"})
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        print("session will be closed.")
        await self.session.close()

    async def _send(self, req:Req) -> Resp:
        print(f"sending req{req.id}")
        async with self.session.post("/v1/chat/completions", json=req.req) as resp:
            resp = Resp(req.id, await resp.json())
        return resp

    async def __call__(self, req_data:dict) -> dict:
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
        req_id = self.timestamp()
        return await self._send(Req(req_id, req_data))

    @staticmethod
    def timestamp() -> int:
        current_datetime = datetime.datetime.now()
        current_timestamp_us = int(current_datetime.timestamp() * 1000000)
        return current_timestamp_us