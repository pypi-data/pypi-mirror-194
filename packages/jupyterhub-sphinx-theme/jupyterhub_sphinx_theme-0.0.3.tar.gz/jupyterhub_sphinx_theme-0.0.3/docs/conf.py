project = "JupyterHub Sphinx Theme"
copyright = "2022"
author = "JupyterHub"
main_doc = "index"
version = "0.0.1a"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "jupyterhub_sphinx_theme"
html_title = "JupyterHub Sphinx Theme"
html_copy_source = True
html_sourcelink_suffix = ""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "icon_links": [            {
                "name": "GitHub",
                "url": "https://github.com/jupyterhub/jupyterhub-sphinx-theme",
                "icon": "fa-brands fa-github",
            },]
}
html_context = {
    "github_user": "jupyterhub",
    "github_repo": "jupyterhub-sphinx-theme",
    "github_version": "main",
}
