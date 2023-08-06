from .. import Arrayable
from typing import Union


class User(Arrayable):
    id: Union[str, None] = None
    name: Union[str, None] = None
    email: Union[str, None] = None

    # User constructor.
    # param: id
    # type: str|None
    # param: name
    # type: str|None
    # param: email
    # type: str|None
    def __init__(self, id: Union[str, None] = None, name: Union[str, None] = None,
                 email: Union[str, None] = None) -> None:
        self.id = id
        self.name = name
        self.email = email
