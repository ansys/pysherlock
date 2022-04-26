import os
import sys

from ansys.sherlock.core import __version__

sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "pysherlock"
copyright = "(c) 2022 ANSYS, Inc. All rights reserved"
author = "ANSYS Inc."
release = version = __version__

# optionally use the default pyansys logo
html_logo = "https://docs.pyansys.com/_static/pyansys-logo-black-cropped.png"

html_theme = "pyansys_sphinx_theme"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/pyansys/pyansys-sphinx-theme",
    "show_prev_next": False,
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]

autosummary_generate = True

# Numpydoc config
numpydoc_show_class_members = False  # we take care of autosummary on our own

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# static path
html_static_path = ["_static"]

# We have our own custom templates
templates_path = ["_templates"]
