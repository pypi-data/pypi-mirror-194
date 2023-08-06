import hashlib
import json
from collections.abc import Callable
from typing import TypeAlias

import networkx as nx
import yaml

from dockable.types import Hash, Step

LinkFnc: TypeAlias = Callable[[nx.DiGraph, Step, Step], None]


def hash_step(s: Step) -> Hash:
    data = json.dumps(s, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def add_step(G: nx.DiGraph, step: Step) -> None:
    G.add_node(hash_step(step), data=step)


def has_step(G: nx.DiGraph, step: Step) -> bool:
    return G.has_node(hash_step(step))


def get_step(G: nx.DiGraph, node: Hash) -> Step:
    return G.nodes.data()[node]["data"]


def link_child(G: nx.DiGraph, parent: Step, child: Step) -> None:
    G.add_edge(hash_step(parent), hash_step(child), type="child")


def link_need(G: nx.DiGraph, parent: Step, need: Step) -> None:
    G.add_edge(hash_step(parent), hash_step(need), type="need")


def get_children(G: nx.DiGraph, x: Hash) -> list[Hash]:
    return [y for y, t in get_dependencies(G, x) if t == "child"]


def get_needs(G: nx.DiGraph, x: Hash) -> list[Hash]:
    return [y for y, t in get_dependencies(G, x) if t == "need"]


def get_dependencies(G: nx.DiGraph, x: Hash) -> list[tuple[Hash, str]]:
    return [(y, nx.get_edge_attributes(G, "type")[(x, y)]) for y in G.successors(x)]


def dangling_nodes(G: nx.DiGraph) -> list[Hash]:
    return [x for x, y in G.out_degree() if y == 0]


def to_dict(G: nx.DiGraph) -> list[dict | str]:
    def _to_dict(node: Hash) -> dict | str:
        data = get_step(G, node)
        children = get_children(G, node)
        needs = get_needs(G, node)
        match data, children, needs:
            case x, [], []:
                return x
            case dict() as d, [*xs], [*ys]:
                return {**d, "_children": [_to_dict(x) for x in xs], "_needs": [_to_dict(y) for y in ys]}
            case str() as s, [*xs], [*ys]:
                return {"name": s, "_children": [_to_dict(x) for x in xs], "_needs": [_to_dict(y) for y in ys]}
            case _:
                raise ValueError("unreachable")

    return [_to_dict(x) for x, y in G.in_degree() if y == 0]


def print_graph(G: nx.DiGraph) -> None:
    print(yaml.safe_dump(to_dict(G), sort_keys=False))
