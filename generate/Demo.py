from Chain import Chain, LLMChain
from State import State
from LLM import LLM
from Task import demo
import asyncio

# current: 
# a specific task, e.g rewrite ruozhiba ds with argumented tone.
# more general pipline is still in developing...


asyncio.run(demo())