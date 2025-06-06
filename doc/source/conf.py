"""Sphinx documentation configuration file."""

from datetime import datetime
import os
from pathlib import Path

from ansys_sphinx_theme import (
    ansys_favicon,
    ansys_logo_white,
    ansys_logo_white_cropped,
    get_version_match,
    latex,
    pyansys_logo_black,
    watermark,
)
from sphinx.builders.latex import LaTeXBuilder
from sphinx.util import logging
from sphinx_gallery.sorting import FileNameSortKey

from ansys.sherlock import core as pysherlock
from ansys.sherlock.core import __version__

LaTeXBuilder.supported_image_types = ["image/png", "image/pdf", "image/svg+xml"]

# Project information
project = "ansys-sherlock-core"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", default="sherlock.docs.pyansys.com")
switcher_version = get_version_match(__version__)

# Select desired logo, theme, and declare the html title
html_logo = pyansys_logo_black
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PySherlock"
html_favicon = ansys_favicon

# Convert notebooks into Python scripts and include them in the output files
logger = logging.getLogger(__name__)

pysherlock.BUILDING_GALLERY = True

DEFAULT_EXAMPLE_EXTENSION = "py"
DOC_PATH = "doc/source"
GALLERY_EXAMPLES_PATH = "examples/gallery_examples"
EXAMPLES_ROOT = "examples"
EXAMPLES_PATH_FOR_DOCS = f"../../{EXAMPLES_ROOT}/"

SOURCE_PATH = Path(__file__).parent.resolve().absolute()
pyansys_light_mode_logo = str(os.path.join(SOURCE_PATH, "_static", "pyansys-logo-light_mode.png"))

# specify the location of your github repo
html_context = {
    "github_user": "ansys",
    "github_repo": "pysherlock",
    "github_version": "main",
    "doc_path": str(DOC_PATH),
}
html_theme_options = {
    "logo": "pyansys",
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
    "check_switcher": False,
    "github_url": "https://github.com/ansys/pysherlock",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "header_links_before_dropdown": 5,  # number of links before the dropdown menu
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": "https://github.com/ansys/pysherlock/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
}

# Sphinx extensions
extensions = [
    "jupyter_sphinx",
    "notfound.extension",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinxemoji.sphinxemoji",
    "ansys_sphinx_theme.extension.linkcode",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
}

# notfound.extension
notfound_template = "404.rst"
notfound_urls_prefix = "/../"

autodoc_default_flags = ["members"]
autosummary_generate = True

# Numpydoc config
numpydoc_show_class_members = False  # we take care of autosummary on our own

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# static path
html_static_path = ["_static"]
templates_path = ["_templates"]
# The suffix(es) of source filenames.
source_suffix = ".rst"

# We have our own custom templates
templates_path = ["_templates"]

# additional logos for the latex coverpage
latex_additional_files = [watermark, ansys_logo_white, ansys_logo_white_cropped]

# change the preamble of latex with customized title page
# variables are the title of pdf, watermark
latex_elements = {"preamble": latex.generate_preamble(html_title)}

linkcheck_ignore = ["https://www.ansys.com/*"]

# If we are on a release, we have to ignore the "release" URLs, since it is not
# available until the release is published.
if switcher_version != "dev":
    linkcheck_ignore.append(f"https://github.com/ansys/pysherlock/releases/tag/v{version}")


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "links.rst",
    # because we include this in examples/index.rst
    f"{GALLERY_EXAMPLES_PATH}/index.rst",
]

# -- Sphinx Gallery Options ---------------------------------------------------
sphinx_gallery_conf = {
    # convert rst to md for ipynb
    "pypandoc": True,
    # path to your examples scripts
    "examples_dirs": ["../../examples/"],
    # path where to save gallery generated examples
    "gallery_dirs": ["examples/gallery_examples"],
    # Pattern to search for example files
    "filename_pattern": r"\." + DEFAULT_EXAMPLE_EXTENSION,
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery example by file name instead of number of lines (default)
    "within_subsection_order": FileNameSortKey,
    # directory where function granular galleries are stored
    "backreferences_dir": None,
    # Modules for which function level galleries are created.  In
    "doc_module": "ansys-sherlock-core",
    "ignore_pattern": "flycheck*",
    "thumbnail_size": (350, 350),
    "remove_config_comments": True,
    "default_thumb_file": pyansys_light_mode_logo,
    "show_signature": False,
    "ignore_pattern": r"examples_globals.py",
}

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""
# Read link all targets from file
with open("links.rst") as f:
    rst_epilog += f.read()
rst_epilog = rst_epilog.replace("%%VERSION%%", f"v{release}")

# Copy button customization ---------------------------------------------------
# exclude traditional Python prompts from the copied code
copybutton_prompt_text = r">>> ?|\.\.\. "
copybutton_prompt_is_regexp = True

# numpydoc configuration
numpydoc_use_plots = True
numpydoc_show_class_members = False
numpydoc_xref_param_type = True
numpydoc_validate = False
numpydoc_validation_checks = {
    # "GL06",  # Found unknown section
    # "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

suppress_warnings = ["label.*", "design.fa-build", "config.cache", "numpydoc.*"]

# Display todos by setting to True
todo_include_todos = True
