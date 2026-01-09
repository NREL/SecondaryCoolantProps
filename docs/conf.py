# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime
from pathlib import Path
from sys import path

from scp import VERSION

root_dir = Path(__file__).parent.parent.resolve()
path.insert(0, str(root_dir))

project = "SecondaryCoolantProps"
copyright = f"{datetime.datetime.now(tz=datetime.timezone.utc).date().year}, Mitchell, M.; Lee, E."  # noqa: A001
author = "Matt Mitchell, Edwin Lee"
release = VERSION

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
