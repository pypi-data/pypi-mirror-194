from types import CodeType, FrameType
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union

__all__: List[str]

# noinspection SpellCheckingInspection
def _getframe(__depth: int) -> Optional[FrameType]: ...

# noinspection SpellCheckingInspection
getframe: Callable[[int],  Optional[FrameType]]

# noinspection SpellCheckingInspection
def isfunctionincallchain(obj: Union[Callable[[Any], Any], CodeType], __depth: int = ...) -> bool: ...

# noinspection SpellCheckingInspection
def nameof(obj: Any) -> Optional[str]: ...

_ArgVal = Optional[Union[int, str, Sequence[str], Tuple[Any, bool]]]

# noinspection SpellCheckingInspection
def _get_argval(offset: int,
                op: int,
                arg: int,
                varnames: Tuple[_ArgVal] = ...,
                names: Tuple[_ArgVal] = ...,
                constants: Tuple[_ArgVal] = ...,
                cells: Tuple[_ArgVal] = ...) -> _ArgVal: ...
def _get_last_name(code: bytes, names: Tuple[str]) -> Optional[str]: ...

class PropertyMeta(type):
    def __init__(cls, name, bases, attrs) -> None: ...

def _is_empty_accessor(accessor: Union[Callable[[Any], Any], ellipsis, None]) -> bool: ...