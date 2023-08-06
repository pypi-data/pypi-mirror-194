def raw(*args: str) -> list[str]:
    return list(args)


def run(*args: list[str] | str) -> list[str]:
    def optional_join(infix: str, x: list[str] | str) -> str:
        return x if type(x) is str else infix.join(x)

    commands = optional_join(" \\\n  && ", [optional_join(" \\\n    ", x) for x in args])
    return [f"RUN {commands}"]


def parallel(*args: dict) -> list[dict]:
    return [{**x, "needs": []} for x in args]
