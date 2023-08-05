# DashLatex: Typeset LaTeX in Dash apps

dash-latex is a Dash component library. Specifically, `DashLatex` is a light Dash wrapper for [ReactLatex](https://github.com/zzish/react-latex) which is itself a wrapper for [Katex](https://katex.org/docs/options.html).

![demo-video](./demo.gif)

`DashLatex` allows the LaTeX markup language to be used in Dash apps.

Get started with:

1. Install Dash and its dependencies: https://dash.plotly.com/installation
2. Run `python usage.py`
3. Visit http://localhost:8050 in your web browser

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
