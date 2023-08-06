from typing import Any, Dict, Union

DictStr = Dict[str, str]
DictStrInt = Dict[str, int]
DictInt = Dict[int, int]
DictAny = Dict[str, Any]


class Empty:
    """
    A placeholder class object.
    """


HashableType = Union[int, bool, str, float, list, dict]
