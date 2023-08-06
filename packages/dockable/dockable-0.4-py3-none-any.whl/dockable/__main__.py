import argparse

import yaml

from ._version import __version__
from .engine.render import render
from .engine.unfold import unfold
from .load.module import load_modules
from .types import Path


def _main(input_file: Path, output_file: Path) -> None:
    with open(input_file) as fh:
        data = yaml.safe_load(fh)
    ctx = load_modules(data["dependencies"])
    data2 = unfold(ctx, data)
    out = render(data2)
    with open(output_file, "w+") as fh:
        fh.write(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("input", type=str, help="path to docker.yml input file")
    parser.add_argument("output", type=str, help="output Dockerfile")
    args = parser.parse_args()
    _main(args.input, args.output)


main()
