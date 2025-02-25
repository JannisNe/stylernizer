# Stylernizer

Make plots for a large project with a unified style using a simple command line interface. No more fiddling with matplotlib styles in every plot script. No more unversionable jupyter notebooks.

## Installation

Right now you can only install from github:

```
pip install git@github.com:JannisNe/stylernizer.git
```

## Usage

`stylerizer` is a tool to make plots for a large project with a unified style using a simple command line interface. For the following examples, we assume that you have a project with a structure like this:

```
    project
    ├── __init__.py
    ├── topic1
    │   ├── __init__.py
    │   ├── plot1.py
    │   └── plot2.py
    └── plot4.py
```
### 1. Decorate the plotting functions with the `register` decorator.

`stylerizer` works with any plotting function that returns a `matplotlib` figure. The only requirement is that the function is registered with `stylerizer` using the `register` decorator.

For example, to register a plot in `plot1.py`:

```python
    from stylernizer import register
    import matplotlib.pyplot as plt

    @register()
    def my_plot():
        
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])
        return fig
```

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
stylernizer run project.topic1.plot1:my_plot
```
or a partial key:
```bash
stylernizer run project.topic1.plot
```
The latter will match all keys starting with `project.topic1.plot`.

You can find the plot in the output directory under `project_topic1_plot1_my_plot.pdf`.

## Configuration

`stylernizer` uses environment variables to configure the output directory and the style of the plots.

* `STYLERNIZER_OUTPUT`: The output directory for the plots. Defaults to `stylernizer` in the current working directory.
* `STYLERNIZER_BASE_STYLE`: The base style that is used for all plots. 
* `STYLERNIZER_CACHE`: The cache directory for the plots. Defaults to `.stylernizer` in the current working directory.

