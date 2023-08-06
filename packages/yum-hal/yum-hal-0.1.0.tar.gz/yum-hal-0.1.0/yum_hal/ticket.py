import msgpack
import base64
import json

from typing import Union, Sequence, Mapping
from uuid import uuid4
from datetime import datetime

wtype = Union[int, float, bool, None, Sequence, Mapping, datetime]

_DTFORMAT = '%Y%m%d%H%M%S%f'

def decode_datetime(obj):
    if "_dt_" in obj:
        obj = datetime.strptime(obj["as_str"], _DTFORMAT)
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime):
        return {"_dt_": True, "as_str": obj.strftime(_DTFORMAT)}
    return obj


class Ticket(object):
    def __init__(self, code: str, status: int = 0) -> None:
        super(Ticket, self).__init__()
        self.id = str(uuid4())
        self.birth_time = datetime.now()
        self.code = code
        self.status = status
        self.body = {}

    def __repr__(self) -> str:
        j = self.__dict__.copy()
        j['birth_time'] = self.birth_time.strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps(j)

    def put(self, name: str, value: wtype) -> None:
        self.body[name] = value

    def take(self, name: str, default_value: wtype = None) -> wtype:
        return self.body.get(name, default_value)

    def encode(self) -> str:
        bs = msgpack.packb(
            {
                "id": self.id,
                "code": self.code,
                "birth_time": self.birth_time,
                "body": self.body,
                "status": self.status,
            },
            default=encode_datetime,
        )

        if isinstance(bs, bytes):
            return base64.urlsafe_b64encode(bs).decode()

        raise RuntimeError('encode error')

    def decode(self, msg: str) -> None:
        bs = base64.urlsafe_b64decode(msg)
        t = msgpack.unpackb(bs, object_hook=decode_datetime)
        self.id = t.get("id")
        self.code = t.get("code")
        self.birth_time = t.get("birth_time")
        self.body = t.get("body")
        self.status = t.get("status")
