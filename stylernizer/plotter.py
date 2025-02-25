import logging
import os
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from rich.logging import RichHandler

formatter = logging.Formatter("%(message)s", "%H:%M:%S")
handler = RichHandler()
handler.setFormatter(formatter)
logging.getLogger("stylernizer").addHandler(handler)
logging.getLogger("stylernizer").propagate = False
logger = logging.getLogger(__name__)


class Plotter:

    registry = {}
    output_directory: Path = (
        Path(os.environ.get("STYLERNIZER_OUTPUT", "~/stylernizer"))
        .expanduser()
        .resolve()
    )
    base_style: str | None = os.environ.get("STYLERNIZER_BASE_STYLE")

    def __init__(self):
        logger.debug(f"using directory {self.output_directory}")
        self.output_directory.mkdir(exist_ok=True)

    @classmethod
    def register(
        cls,
        style_name: str | list[str] = None,
        arg_loop: Any | list[Any] | None = None,
        orientation: str | None = None,
    ):
        if isinstance(style_name, str):
            style_name = [style_name]
        styles = []
        if cls.base_style:
            styles.extend(cls.base_style)
        if style_name:
            styles.extend(style_name)

        def plot_function_with_style(f):

            def wrapper(*args, **kwargs):
                logger.debug(f"using styles {styles}")
                style.use(styles)
                if orientation:
                    cls.set_orientation(orientation)
                return f(*args, **kwargs)

            fname = f.__module__ + ":" + f.__name__
            if not arg_loop:
                cls.registry[fname] = wrapper
            else:
                for a in np.atleast_1d(arg_loop):
                    ka = (
                        a
                        if (len(a) == 1 or isinstance(a, str))
                        else "_".join([str(aa) for aa in a])
                    )
                    cls.registry[f"{fname}_{ka}"] = (
                        lambda x=a, *args, **kwargs: wrapper(x, *args, **kwargs)
                    )

            return f

        return plot_function_with_style

    @classmethod
    def set_orientation(cls, orientation: str):
        assert orientation in ["landscape", "portrait", "square"]
        figsize = plt.rcParams["figure.figsize"]
        current_orientation = "landscape" if figsize[0] > figsize[1] else "portrait"
        if current_orientation != orientation:
            logger.debug(f"changing orientation to {orientation}")
            ratio = figsize[1] / figsize[0] if orientation != "square" else 1
            exponent = (
                1 if orientation == "landscape" else -1
            )  # 1 landscape, -1 portrait, meaningless for square
            plt.rcParams["figure.figsize"] = (figsize[0], figsize[0] * ratio**exponent)

    def get_filename(self, name: str):
        return self.output_directory / (
            name.replace(":", "_").replace(".", "_") + ".pdf"
        )

    def plot(
        self,
        name: str | list[str] | None = None,
        save: bool = False,
        show: bool = False,
    ):
        all_names = self.registry.keys()
        if isinstance(name, str):
            name = [name]
        if name is None:
            name = self.registry.keys()
        _name = [n2 for n2 in all_names if any([n2.startswith(n1) for n1 in name])]
        if len(_name) < 1:
            raise KeyError(
                "No plot found in registry! Available are "
                + ", ".join(self.registry.keys())
            )
        logger.info(f"making {len(_name)} plots")
        logger.debug(", ".join(_name))
        for n in _name:
            logger.info(f"plotting {n}")
            fig = self.registry[n]()
            if save:
                filename = self.get_filename(n)
                logger.info(f"saving to {filename}")
                fig.savefig(filename, bbox_inches="tight")
            if show:
                plt.show()
            plt.close()
        logger.info("done")
