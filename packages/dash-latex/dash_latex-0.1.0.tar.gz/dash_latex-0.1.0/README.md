# DashLatex: Typeset LaTeX in Dash apps

dash-latex is a Dash component library. Specifically, `DashLatex` is a light Dash wrapper for [ReactLatex](https://github.com/zzish/react-latex) which is itself a wrapper for [Katex](https://katex.org/docs/options.html).

![demo-video](./demo.gif)

`DashLatex` allows the LaTeX markup language to be used in Dash apps.

Get started with:

1. Install Dash and its dependencies: https://dash.plotly.com/installation
2. Run `python usage.py`
3. Visit http://localhost:8050 in your web browser

## Getting started

DashLatex works like any other Dash component:

```python
import dash_latex as dl
import dash

app = dash.Dash(__name__)

app.layout = dl.DashLatex(
    r"""
    When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
    $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
    """,
)

if __name__ == "__main__":
    app.run_server(debug=True)
```

Note that if using inline strings to write LaTeX, using raw strings is recommended, as LaTeX markup contains character sequences which Python will interpret as escape sequences.

DashLatex exposes all of the declarative options available from Katex, which are documented [here](https://katex.org/docs/options.html). You can run `help(dl.DashLatex)` to see a list of parameters exposed in the Python API.

### Install dependencies

If you have selected install_dependencies during the prompt, you can skip this part.

1. Install npm packages
    ```
    $ npm install
    ```
2. Create a virtual env and activate.

    ```
    $ virtualenv venv
    $ . venv/bin/activate
    ```

    _Note: venv\Scripts\activate for windows_

3. Install python packages required to build components.
    ```
    $ pip install -r requirements.txt
    ```
4. Install the python packages for testing (optional)
    ```
    $ pip install -r tests/requirements.txt
    ```

## Working with this package

1. Build:
    ```
    $ npm run build
    ```
2. Create a Python distribution:

    ```
    $ python setup.py sdist bdist_wheel
    ```

    This will create source and wheel distribution in the generated the `dist/` folder.
    See [PyPA](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project)
    for more information.
