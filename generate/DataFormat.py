from dataclasses import dataclass, asdict


@dataclass
class Message:
    role:str
    content:str


@dataclass
class ReqData:
    model:str
    temperature:float
    messages:list[Message]

    def tojson(self):
        return asdict(self)


@dataclass
class Req:
    id: int
    data: dict





@dataclass
class Usage:
    prompt_tokens:int
    completion_tokens:int
    total_tokens:int


@dataclass
class Choice:
    index:int
    message:Message
    finish_reason:str


@dataclass
class RespData:
    id:str
    object:str
    created:int
    model:str
    choices:list[Choice]
    usage:Usage


class Resp:
    def __init__(self, resp_id:int, resp_data:dict) -> None:
        self.id:int = resp_id
        self.data:RespData = resp_data if isinstance(resp_data, RespData) else RespData(**resp_data)

