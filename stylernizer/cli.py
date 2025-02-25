import logging
from typing import Optional

import numpy as np
import typer
from rich import console, tree
from typing_extensions import Annotated

from stylernizer.plotter import Plotter

logger = logging.getLogger(__name__)


app = typer.Typer()


def walk_modules(
    names: list[str], the_tree: tree.Tree, length: int, parent: str = "", level: int = 0
):
    modules = np.unique([n.split(":")[0].split(".")[0] for n in names])
    logger.debug(f"walking modules: {modules}, parent: {parent}, level: {level}")
    for m in modules:
        logger.debug(f"adding module {m}")
        sub_tree = the_tree.add(f"[bold blue] {m}")
        members = [n for n in names if n.startswith(m)]
        functions = [n for n in members if n.startswith(f"{m}:")]
        for f in functions:
            _f = f.split(":")[1]
            logger.debug(f"adding function {_f}")
            filled = "".ljust(length - len(_f) - 4 * (level - 1), ".")
            ps = parent.strip(".") + "." if parent else ""
            fs = f.strip(".")
            logger.debug(f"parent: {ps}, function: {fs}")
            sub_tree.add(f"[yellow] {_f}[/yellow]{filled}[bold magenta]{ps}{fs}")
        non_functions = [
            n.removeprefix(m).removeprefix(".") for n in members if n not in functions
        ]
        if len(non_functions) > 0:
            walk_modules(
                non_functions,
                sub_tree,
                length,
                parent=m if not parent else f"{parent}.{m}",
                level=level + 1,
            )


def get_tree(name: list[str] | None = None) -> tree.Tree:
    plotter = Plotter()
    if name is not None:
        names = [
            k for k in plotter.registry.keys() if any([iname in k for iname in name])
        ]
    else:
        names = plotter.registry.keys()
    logger.debug(f"listing plots: {names}")
    length = max(
        [4 * (n.split(":")[0].count(".") + 1) + 2 + len(n.split(":")[1]) for n in names]
    )
    logger.debug(f"length: {length}")
    _tree = tree.Tree(
        "[bold white]Plots Tree" + "".join([" "] * (length + 3)) + "Plot Keys"
    )
    walk_modules(names, _tree, length)
    return _tree


@app.command()
def register(
    name: Annotated[
        list[str], typer.Argument(help="Names(s) of the packages/modules to register")
    ],
    log_level: Annotated[str, typer.Option("--log-level", "-l")] = "INFO",
):
    logging.getLogger("stylernizer").setLevel(log_level.upper())
    for n in name:
        logger.info(f"registering {n}")
        __import__(n)
    plotter = Plotter()
    logger.info(f"registered {len(plotter.registry)} plots")
    _tree = get_tree()
    console.Console().print(_tree, new_line_start=True)
    plotter.dump_cache()
    typer.Exit()


@app.command(name="list")
def list_available_plots(
    log_level: Annotated[str, typer.Option("--log-level", "-l")] = "INFO",
    name: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="Names(s) of the plots to make",
        ),
    ] = None,
):
    logging.getLogger("stylernizer").setLevel(log_level.upper())
    _tree = get_tree(name)
    console.Console().print(_tree, new_line_start=True)
    typer.Exit()


@app.command()
def run(
    log_level: Annotated[str, typer.Option("--log-level", "-l")] = "INFO",
    name: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="Names(s) of the plots to make",
        ),
    ] = None,
    save: bool = True,
    show: bool = False,
):
    logging.getLogger("stylernizer").setLevel(log_level.upper())
    plotter = Plotter()
    plotter.plot(name=name, save=save, show=show)
    typer.Exit()


def main():
    app()


if __name__ == "__main__":
    app()
