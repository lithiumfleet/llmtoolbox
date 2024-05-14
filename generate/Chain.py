from timeit import timeit
from typing import Callable
import asyncio
from inspect import iscoroutinefunction as isasync
from State import State
from LLM import LLM
from collections import namedtuple


class Chain:
    def __init__(self, *func_list: list[Callable]):
        self.func_list = func_list
        self.state = State()
    
    async def invoke(self):
        """
        go through the functions and excute each of them.
        if the function is async, the chain will await it.
        """
        for func in self.func_list:
            if isinstance(func, LLM):
                # this must be llm.__call__
                self.state.resp = await func(self.state.req)
            else:
                func(self.state)
    
    

if __name__ == "__main__":
    from Task import *
    import sys
    def main(max_num=1):
        chains = [Chain(fun1, fun2, fun3) for _ in range(max_num)]
        # asyncio.run([chain.invoke()]*10)

        tasks = [chain.invoke() for chain in chains]
        async def aiomain():
            await asyncio.gather(*tasks)
        asyncio.run(aiomain())
    
    main(int(sys.argv[1]))