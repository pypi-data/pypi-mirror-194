import os

import pip_api

from dockable.types import Path


def load_requirements(file: Path) -> list[str]:
    file = os.path.expanduser(file)
    res = pip_api.parse_requirements(file)
    return [str(x) for x in res.values()]


def pip(**kwargs) -> list[dict]:
    pkg = kwargs["pkg"] if "pkg" in kwargs else []
    from_requirements = kwargs["from_requirements"] if "from_requirements" in kwargs else []
    reqs_pkgs = [load_requirements(x) for x in from_requirements]
    reqs_pkg = [y for x in reqs_pkgs for y in x]
    return [
        {
            ".pip-internal": {
                **kwargs,
                "pkg": pkg + reqs_pkg,
            }
        }
    ]
