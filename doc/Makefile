# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j auto -W --keep-going
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


# Customized clean due to examples gallery
clean:
	@echo "Cleaning everything."
	rm -rf $(BUILDDIR)/*
	rm -rf images/auto-generated
	rm -rf source/examples/gallery_examples
	find . -type d -name "_autosummary" -exec rm -rf {} +

# clean only examples
clean-examples:
	@echo "Cleaning only the examples."
	rm -rf source/examples/gallery_examples

# Create PDF
pdf:
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd $(BUILDDIR)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f $(BUILDDIR)/latex/ansys-sherlock-core.pdf && echo pdf exists) || exit 1

# Building gallery without running examples
html-noexamples:
	@echo "Building gallery without running examples."
	@sphinx-build -D plot_gallery=0 -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
