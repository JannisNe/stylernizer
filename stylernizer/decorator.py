from typing import Any

from stylernizer.plotter import Plotter


def register(
    style_name: str | list[str] = None,
    arg_loop: Any | list[Any] | None = None,
    orientation: str | None = None,
):
    return Plotter.register(style_name, arg_loop, orientation)
