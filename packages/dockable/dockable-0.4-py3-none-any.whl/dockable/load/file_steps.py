import os
from collections.abc import Callable
from typing import Any, ParamSpec

import yaml
from jinja2 import ChainableUndefined, Template  # type: ignore
from jinja2.exceptions import UndefinedError

from dockable.types import Handler, LocalContext, Path, Step

P = ParamSpec("P")


def load_template(data: str, **opts: Any) -> Callable[..., tuple[str | None, list[Step]]]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> tuple[str | None, list[Step]]:
        try:
            rendered = Template(data, **opts).render({**kwargs, "args": [*args], "kwargs": kwargs})
        except UndefinedError as e:
            raise ValueError(f"while rendering:\n{data}") from e
        parsed = yaml.safe_load(rendered)
        return parsed.get("name"), parsed["steps"]

    return inner


def load_template_step(data: str) -> tuple[str | None, Handler]:
    name, _ = load_template(data, undefined=ChainableUndefined)()

    def _load(*args: P.args, **kwargs: P.kwargs) -> list[Step]:
        _, steps = load_template(data)(*args, **kwargs)
        return steps

    return name, _load


def load_text_step(data: str) -> tuple[str | None, Handler]:
    parsed = yaml.safe_load(data)
    return parsed.get("name"), lambda: parsed["steps"]


def load_file_steps(file: Path) -> LocalContext:
    with open(file) as fh:
        res = fh.read()
        data = res.split("\n---\n")
    basename = os.path.basename(file).split(".", 1)[0]

    def fallback_name(name: str | None) -> str:
        match name, basename, len(data):
            case (str() as x, _, _):
                return x
            case (None, x, 1):
                return x
            case _:
                raise ValueError("name must be defined if multiple commands are defined in a single file")

    load_fnc = load_template_step if file.endswith(".jinja") else load_text_step
    data2 = [load_fnc(x) for x in data]
    return {fallback_name(k): v for k, v in data2}
