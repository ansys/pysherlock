import os
import sys

from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary import get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr
import re

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

autodoc_default_flags = ['members']
autosummary_generate = True
autosummary_imported_members = True
autosummary_ignore_module_all = False

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

# The following is an unsuccessful attempt to dynamically generate the API tree menu for all the public class methods.
# https://stackoverflow.com/questions/20569011/python-sphinx-autosummary-automated-listing-of-member-functions/30783465#30783465
# Maybe we can get this to work in the future.
class AutoAutoSummary(Autosummary):

    option_spec = {
        'methods': directives.unchanged,
        'attributes': directives.unchanged,
        'toctree': directives.unchanged
    }

    required_arguments = 1

    @staticmethod
    def get_members(obj, typ, include_public=None):
        if not include_public:
            include_public = []
        items = []
        for name in dir(obj):
            try:
                documenter = get_documenter(safe_getattr(obj, name), obj)
            except AttributeError:
                continue
            if documenter.objtype == typ:
                items.append(name)
        public = [x for x in items if x in include_public or not x.startswith('_')]
        return public, items

    def run(self):
        clazz = str(self.arguments[0])
        try:
            (module_name, class_name) = clazz.rsplit('.', 1)
            m = __import__(module_name, globals(), locals(), [class_name])
            c = getattr(m, class_name)
            if 'methods' in self.options:
                _, methods = self.get_members(c, 'method', ['__init__'])

                self.content = ["~%s.%s" % (clazz, method) for method in methods if not method.startswith('_')]
            if 'attributes' in self.options:
                _, attribs = self.get_members(c, 'attribute')
                self.content = ["~%s.%s" % (clazz, attrib) for attrib in attribs if not attrib.startswith('_')]
        finally:
            return super(AutoAutoSummary, self).run()

def setup(app):
    app.add_directive('autoautosummary', AutoAutoSummary)