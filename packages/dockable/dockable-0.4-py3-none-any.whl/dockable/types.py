from collections.abc import Callable
from typing import TypeAlias

Path: TypeAlias = str
Hash: TypeAlias = str
Step: TypeAlias = dict | str
StepArgs: TypeAlias = dict | list | str
Handler: TypeAlias = Callable[..., list[Step]]
LocalContext: TypeAlias = dict[str, Handler]
Context: TypeAlias = dict[str, LocalContext]
