import typing as t

Headers = t.Dict[str, str]
Id = t.NewType("id_", str)
Messages = t.List[t.Dict[str, str]]
Chunk = t.NewType("chunk", t.Dict[str, str])
Any = t.Any

__all__ = ["Headers", "Id", "Chunk", "Messages", "Any"]

# Path: assets/typing.py