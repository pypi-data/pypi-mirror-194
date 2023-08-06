import os

import yaml

from dockable.types import Path


def load_requirements(file: Path) -> dict:
    file = os.path.expanduser(file)
    with open(file) as fh:
        data = yaml.safe_load(fh)
    return data


def ansible(**kwargs) -> list[dict]:
    roles = kwargs["roles"] if "roles" in kwargs else []
    collections = kwargs["collections"] if "collections" in kwargs else []
    from_requirements = kwargs["from_requirements"] if "from_requirements" in kwargs else []
    reqs_pkg = [load_requirements(x) for x in from_requirements]
    return [
        {
            ".ansible-galaxy-internal": {
                **kwargs,
                "roles": roles + [y for x in reqs_pkg for y in x["roles"]],
                "collections": collections + [y for x in reqs_pkg for y in x["collections"]],
            }
        }
    ]
