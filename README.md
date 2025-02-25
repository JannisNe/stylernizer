# Stylernizer

Make plots for a large project like a thesis with a unified style using a simple command line interface. No more fiddling with matplotlib styles in every plot script. No more unversionable jupyter notebooks.

## Concepts

### File Structure
The idea of `stylernizer` is that your project structure follows a topic tree as shown below. To get rid of redundant plot filenames and module and function names, `stylernizer` saves the produced plots under a filename compiled from the topic tree and the function name. This way, you can easily find the plot you are looking for and keep your project organized. 

### Styles
`stylernizer` uses `matplotlib` styles to define the appearance of the plots. You can define a base style for all plots and additional styles for specific cases such as full page plots, margin plots, etc. This way, you can easily change the appearance of all plots in your project by changing the base style.

## Installation

Right now you can only install from github:

```
pip install git@github.com:JannisNe/stylernizer.git
```

## Usage

`stylernizer` is a tool to make plots for a large project with a unified style using a simple command line interface. For the following examples, we assume that you have a project with a structure like this:

```
    project
    ├── __init__.py
    ├── topic1
    │   ├── __init__.py
    │   ├── topic1_1.py
    │   └── topic1_2.py
    ├── plotx.py
    └── styles
        ├── base.mplstyle
        └── fullpage.mplstyle
```

If you have not run `stylernizer` for your plots yet, you need to register your plots first following steps 1 and 2 before producing the plots in step 3. After that, you can skip step 1 and 2 and directly produce the plots.

### 1. Decorate the plotting functions with the `register` decorator.

`stylernizer` works with any plotting function that returns a `matplotlib` figure. The only requirement is that the function is registered with `stylernizer` using the `register` decorator.

For example, to register a plot in `plot1.py`:

```python
    from stylernizer import register
    import matplotlib.pyplot as plt

    @register("fullpage", arg_loop=["log", "linear"])
    def my_plot(scale: str):
        
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])
        ax.set_xscale(scale)
        ax.set_yscale(scale)
        return fig
```

`register()` takes three optional arguments:
* `style_name`: `str` or `list[str]`; The style(s) to use for this plot in addition to the base style (see below). These must be importable by `matplotlib.style.use()` (see [this documentation](https://matplotlib.org/stable/users/explain/customizing.html#defining-your-own-style) for more info on style sheets). In this example, the plot will use the `topic1` style.
* `arg_loop`: `Any` or `list[Any]`; The argument(s) to loop over when calling the function. This is useful when you want to create multiple plots with the same function but different arguments. In this example, the function will be called with `scale="log"` and `scale="linear"`. The ouput files will be named `project_topic1_topic1_1_my_plot_log.pdf` and `project_topic1_topic1_1_my_plot_linear.pdf`.
* `orientation`: `str`; The orientation of the plot. Can be `landscape`, `portrait` or `square`. Defaults to `landscape`.

### 2. Run `stylernizer register` to register your package.

```bash
stylernizer register project
```

### 3. Run `stylernizer run` to make the plots.

To produce all registered plots in the project:
```bash
stylernizer run
```

You can also produce a specific plot by providing the key of the plot:
```bash
stylernizer run project.topic1.topic1_1:my_plot
```
or a partial key:
```bash
stylernizer run project.topic1.topic1_1
```
The latter will match all keys starting with `project.topic1.topic1_1`.

You can find the plot in the output directory under `project_topic1_topic1_1_my_plot.pdf`.

## Configuration

`stylernizer` uses environment variables to configure the output directory and the style of the plots.

* `STYLERNIZER_OUTPUT`: The output directory for the plots. Defaults to `stylernizer` in the current working directory.
* `STYLERNIZER_BASE_STYLE`: The base style that is used for all plots. 
* `STYLERNIZER_CACHE`: The cache directory for the plots. Defaults to `.stylernizer` in the current working directory.

