"""A lightweight theme for JupyterHub."""
import os
from pathlib import Path
from sphinx.util import logging

__version__ = "0.0.3"

THEME_PATH = (Path(__file__).parent / "theme" / "jupyterhub-sphinx-theme").resolve()

logger = logging.getLogger(__name__)


def _config_provided_by_user(app, key):
    """Check if the user has manually provided the config.
    REMOVE when pydata v0.14 is released and import from there.
    """
    return any(key in ii for ii in [app.config.overrides, app.config._raw_config])


def set_config_defaults(app):
    config = app.config
    try:
        theme = app.builder.theme_options
    except AttributeError:
        theme = None
    if not theme:
        theme = {}

    # Default jupyter favicon
    if not _config_provided_by_user(app, "html_favicon"):
        config.html_favicon = (
            "https://github.com/jupyterhub/jupyterhub-sphinx-theme/raw/master/src/jupyterhub_sphinx_theme/theme/jupyterhub-sphinx-theme/static/favicon.png"
        )

    # Navigation bar
    if "navbar_align" not in theme:
        theme["navbar_align"] = "left"

    icon_links = [] if "icon_links" not in theme else theme["icon_links"]
    icon_links.extend(
        [
            {
                "name": "Discourse",
                "url": "https://discourse.jupyter.org/",
                "icon": "fa-brands fa-discourse",
                "type": "fontawesome",
            },
            {
                "name": "Team Compass",
                "url": "https://jupyterhub-team-compass.readthedocs.io/en/latest/",
                "icon": "fa-solid fa-compass",
                "type": "fontawesome",
            },
        ]
    )
    theme["icon_links"] = icon_links

    # Default logo
    logo = {} if "logo" not in theme else theme["logo"]
    if not logo:
        logo = {}
    if "image_dark" not in logo:
        path_dark = THEME_PATH / "static" / "hub-rectangle-dark.svg"
        logo["image_dark"] = str(path_dark.resolve())
    if "image_light" not in logo:
        path_light = THEME_PATH / "static" / "hub-rectangle.svg"
        logo["image_light"] = str(path_light.resolve())
    theme["logo"] = logo

    # Sphinxext Opengraph add URL based on ReadTheDocs variables
    # auto-generate this so that we don't have to manually add it in each documentation.
    # it should be addable via the environment variables.
    env = os.environ
    if "GITHUB_ACTION" in env:
        site_url = f"https://{env['GITHUB_REPOSITORY_OWNER']}.github.io/{env['GITHUB_REPOSITORY']}"
    elif "READTHEDOCS" in env:
        site_url = f"https://{env['READTHEDOCS_PROJECT']}.readthedocs.io/{env['READTHEDOCS_LANGUAGE']}/{env['READTHEDOCS_VERSION_NAME']}"
    else:
        # Don't do anything automatic if we aren't in RTD or GHP
        site_url = None
    if site_url and not hasattr(config, "ogp_site_url"):
        logger.info("Setting `ogp_site_url` via CI/CD environment variables...")
        config.ogp_site_url = site_url

    # Clean up actions
    # Update the HTML theme config
    app.builder.theme_options = theme


def _activate_extensions_after_config_inited(app, extensions):
    """Activate extensions and trigger the config-inited event.

    This ensures that new extensions have their event hooks triggered, but that old
    ones don't trigger twice.
    """
    # Save the old event listeners and then replace with an empty list
    old_listeners = app.events.listeners["config-inited"]
    app.events.listeners["config-inited"] = []
    # Activate extensions which will re-add new extensions to listeners["config-inited"]
    for extension in extensions:
        app.setup_extension(extension)
    # Trigger config-inited so that their hooks fire
    app.emit("config-inited", app.config)
    # Now add back the old extension list
    app.events.listeners["config-inited"][:0] = old_listeners


def setup(app):
    app.add_html_theme("jupyterhub_sphinx_theme", THEME_PATH)
    app.config.html_static_path.append(str(THEME_PATH / "static"))
    extensions = ["sphinx_copybutton", "sphinxext.opengraph"]
    _activate_extensions_after_config_inited(app, extensions)
    app.connect("builder-inited", set_config_defaults)
