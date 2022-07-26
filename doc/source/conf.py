import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

from ansys.sherlock.core import __version__

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
