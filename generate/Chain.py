from timeit import timeit
from typing import Callable
import asyncio
from typing import Any
from inspect import iscoroutinefunction as isasync
from State import State
from LLM import LLM, Req, Resp
from collections import namedtuple
from functools import partial


class Chain:
    def __init__(self, *callable_list: list[Callable]):
        self.callable_list = callable_list
        self.state = State()
    
    async def invoke(self, init_state:State=None):
        """
        go through the functions and excute each of them.
        if the function is async, the chain will await it.
        """
        if init_state is not None:
            self.state = init_state

        for operate in self.callable_list:
            if isinstance(operate, LLM):
                # this must be llm.__call__
                self.state.resp = await operate(self.state.req)
            elif isinstance(operate, Chain):
                operate.invoke(self.init_state)
            elif isinstance(operate, Callable):
                operate(self.state)
            else:
                pass


class LLMChain(Chain):
    def __init__(self, prepare:Callable=None, llm:LLM=None, after:Callable=None):
        super().__init__(prepare, llm, after)