from timeit import timeit
from typing import Callable
import asyncio
from inspect import iscoroutinefunction as isasync
from State import State


class Chain:
    def __init__(self, *func_list: Callable):
        self.func_list = func_list
        self.state = State()
    
    async def invoke(self):
        for func in self.func_list:
            if isasync(func):
                await func(self.state)
            else:
                func(self.state)
    
    

if __name__ == "__main__":
    # def funca():
    #     pass
    # async def funcb():
    #     pass
    # async def funcc():
    #     await funcb()
    # print(isasync(funca), isasync(funcb), isasync(funcc))
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