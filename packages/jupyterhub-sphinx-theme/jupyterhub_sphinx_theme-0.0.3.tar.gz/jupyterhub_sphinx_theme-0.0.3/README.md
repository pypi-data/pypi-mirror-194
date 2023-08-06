# The JupyterHub Documentation Theme

A lightweight theme built on the PyData Sphinx Theme, for use by the JupyterHub community.
It makes minimal changes to the `pydata-sphinx-theme` in order to standardize styles and a top-bar that can be shared across all JupyterHub documentation.

## Defaults this theme sets

This theme sets a few default values to standardize the look and feel across JupyterHub documentation.

```{note}
If there are other standard features/customizations that would be helpful across the JupyterHub team documentation, we can probably add it here so please open an issue to discuss.
```

Here is a brief summary:

### Style

- Sets the primary color to a slightly-darkened "Jupyter orange"
- Removes primary color from headers and makes them bold to be noticeable
- Aligns the header links to the left

### Logo and branding

- Adds a light/dark mode JupyterHub logo
- Adds a favicon
- Adds icon links for our Discourse, Team Compass, and Jupyter.org

### Extensions

- [`sphinx-copybutton`](https://sphinx-copybutton.readthedocs.io/) for copy buttons in our code cells.
- [`sphinxext-opengraph`](https://sphinxext-opengraph.readthedocs.io/en/latest/) for OpenGraph protocol metadata. `site_url` will automatically be detected via `ReadTheDocs` or `GitHub Actions` environment variables in CI/CD.

## How to use this theme

Follow these steps:

1. Add this theme to the `pip` install requirements of the repo.
   For now, point it to the `main` branch like so:

   ```
   # in requirements.txt
   git+https://github.com/jupyterhub/jupyterhub-sphinx-theme
   ```

   or to install locally

   ```console
   $ pip install git+https://github.com/jupyterhub/jupyterhub-sphinx-theme
   ```
2. Configure the Sphinx docs to use the theme by editing `conf.py`

   ```{code-block} python
   :caption: conf.py

   html_theme = "jupyterhub_sphinx_theme"
   ```
3. Add it to your theme's extensions:

   ```{code-block} python
   :caption: conf.py

   extensions = [
      "jupyterhub_sphinx_theme"
   ]
   ```

## Make customizations on top of these defaults

You can make customizations on top of the defaults in this theme.
See [the PyData theme documentation](https://pydata-sphinx-theme.readthedocs.io/) for guidance on what is possible.

In general, this theme only sets defaults, and you can override whatever you like.

## Developer documentation

### Theme build system

This theme uses the [`sphinx-theme-builder` tool](https://github.com/pradyunsg/sphinx-theme-builder), which is a helper tool for automatically compiling Sphinx theme assets.
This will download a local copy of NodeJS and build the theme's assets with the environment specified in `package.json`.

### Theme structure

This theme follows the [`sphinx-theme-builder` filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/reference/filesystem-layout/).

### Build the theme locally

You can build the documentation for this theme to preview it.
The easiest way to build the documentation in this repository is to use [the `nox` automation tool](https://nox.thea.codes/), a tool for quickly building environments and running commands within them.
This ensures that your environment has all the dependencies needed to build the documentation.

To do so, follow these steps:

1. Install `nox`

   ```console
   $ pip install nox
   ```
2. Build the documentation:

   ```console
   $ nox -s docs
   ```

This should create a local environment in a `.nox` folder, build the documentation (as specified in the `noxfile.py` configuration), and the output will be in `docs/_build/html`.

To build live documentation that updates when you update local files, run the following command:

```console
$ nox -s docs-live
```

## Make a release

To make a release:

- update the version number in `src/jupyterhub_sphinx_theme/__init__.py`
- push the changes
- [make a release on GitHub](https://github.com/jupyterhub/jupyterhub-sphinx-theme/releases).

When you finish this process, a GitHub Action will trigger to package and upload the release to PyPI.
