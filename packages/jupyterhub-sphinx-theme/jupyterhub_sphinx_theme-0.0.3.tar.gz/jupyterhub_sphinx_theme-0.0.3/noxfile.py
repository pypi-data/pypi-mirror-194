import nox

nox.options.reuse_existing_virtualenvs = True

build_command = ["-b", "html", "docs", "docs/_build/html"]


@nox.session
def docs(session):
    """Build the documentation locally. Use `-- live` to run a live server."""
    session.install("-e", ".[dev]")
    session.install("-r", "docs/requirements.txt")

    if "live" in session.posargs:
        session.run("stb", "serve", "docs")
    else:
        session.run("stb", "compile")
        session.run("sphinx-build", *build_command)
