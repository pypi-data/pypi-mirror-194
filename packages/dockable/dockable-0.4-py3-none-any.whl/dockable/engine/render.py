import networkx as nx

from ..types import Step
from .graph import get_children, get_step


def render_steps(G: nx.DiGraph) -> list[str]:
    def assert_leave(x: Step) -> str:
        match x:
            case str() as s:
                return s
            case _:
                # leaves by definition must be str and cannot be dict,
                # as otherwise recursion would not have stopped
                # the type-conversion here is just to also tell this to mypy
                raise ValueError("unreachable")

    return [assert_leave(get_step(G, x)) for x in nx.dfs_postorder_nodes(G) if len(get_children(G, x)) == 0]


def render_image(data: dict) -> str:
    data2 = render_steps(data["steps"])
    return "\n".join(data2)


def render(data: dict) -> str:
    return "\n".join([render_image(x) for x in data["images"]])
