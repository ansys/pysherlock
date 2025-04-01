"""Sphinx documentation configuration file."""

from datetime import datetime
import os

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

from ansys.sherlock.core import __version__

LaTeXBuilder.supported_image_types = ["image/png", "image/pdf", "image/svg+xml"]

# Project information
project = "ansys-sherlock-core"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", default="nocname.com")
switcher_version = get_version_match(__version__)

# Select desired logo, theme, and declare the html title
html_logo = pyansys_logo_black
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PySherlock"
html_favicon = ansys_favicon

# specify the location of your github repo
html_context = {
    "github_user": "ansys",
    "github_repo": "pysherlock",
    "github_version": "main",
    "doc_path": "doc/source",
}
html_theme_options = {
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
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_design",
]

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

# We have our own custom templates
templates_path = ["_templates"]

autodoc_mock_imports = [
    "grpc",
    "SherlockCommonService_pb2",
    "SherlockCommonService_pb2_grpc",
    "SherlockProjectService_pb2",
    "SherlockProjectService_pb2_grpc",
    "SherlockModelService_pb2",
    "SherlockModelService_pb2_grpc",
    "SherlockLifeCycleService_pb2",
    "SherlockLifeCycleService_pb2_grpc",
    "SherlockLayerService_pb2",
    "SherlockLayerService_pb2_grpc",
    "SherlockStackupService_pb2",
    "SherlockStackupService_pb2_grpc",
    "SherlockPartsService_pb2",
    "SherlockPartsService_pb2_grpc",
    "SherlockAnalysisService_pb2",
    "SherlockAnalysisService_pb2_grpc",
]

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

# Suprpress warnings
suppress_warnings = ["design.grid", "design.fa-build"]
