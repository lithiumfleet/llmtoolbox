from dataclasses import dataclass, field, asdict
from typing import Union
import aiohttp
from aiohttp import ClientSession
import asyncio
import json




class Res:
    def __init__(self) -> None:
        pass



@dataclass
class Req:
    pass




class llm:

    def __init__(self) -> None:
        self.url: str
        self.key: str = "sk-"

    def invoke(inputs: str|list[str]):
        pass # 

    @staticmethod
    async def fetch(session:ClientSession , url:str, data:Req) -> Res:
        async with session.post(url, json=asdict(data)) as resp:
            return await Res(resp)

    