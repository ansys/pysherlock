.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.9.1 <https://github.com/ansys/pysherlock/releases/tag/v0.9.1>`_ - January 21, 2026
=====================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - feat: secure grpc channels
          - `#704 <https://github.com/ansys/pysherlock/pull/704>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - MAINT: set secret for GitHub action named "Release to GitHub"
          - `#574 <https://github.com/ansys/pysherlock/pull/574>`_


`0.9.0 <https://github.com/ansys/pysherlock/releases/tag/v0.9.0>`_ - May 22, 2025
=================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - feat: launching a specific version of Sherlock
          - `#431 <https://github.com/ansys/pysherlock/pull/431>`_

        * - feat: add Analysis.update_component_failure_mechanism_analysis_props()
          - `#478 <https://github.com/ansys/pysherlock/pull/478>`_

        * - feat: New API update_semiconductor_wearout_props()
          - `#488 <https://github.com/ansys/pysherlock/pull/488>`_

        * - feat: new API update_PTH_fatigue_props()
          - `#492 <https://github.com/ansys/pysherlock/pull/492>`_

        * - feat: add Parts.get_parts_list_properties()
          - `#502 <https://github.com/ansys/pysherlock/pull/502>`_

        * - feat: new API update_pad_properties()
          - `#505 <https://github.com/ansys/pysherlock/pull/505>`_

        * - feat: Refactor launcher to allow connecting to Sherlock that is running
          - `#508 <https://github.com/ansys/pysherlock/pull/508>`_

        * - feat: new API deletePartsFromPartsList()
          - `#526 <https://github.com/ansys/pysherlock/pull/526>`_

        * - feat: Update thermal maps APIs
          - `#530 <https://github.com/ansys/pysherlock/pull/530>`_

        * - feat: Get solder info RPC
          - `#534 <https://github.com/ansys/pysherlock/pull/534>`_

        * - feat: new API import_GDSII_file
          - `#537 <https://github.com/ansys/pysherlock/pull/537>`_

        * - feat: new API to add board outline
          - `#560 <https://github.com/ansys/pysherlock/pull/560>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - fix: proper AUTHORS file
          - `#438 <https://github.com/ansys/pysherlock/pull/438>`_

        * - fix: API updatePTHFatigueProps()
          - `#506 <https://github.com/ansys/pysherlock/pull/506>`_

        * - fix: PartLocation variable was renamed by mistake
          - `#515 <https://github.com/ansys/pysherlock/pull/515>`_

        * - fix: update_pad_properties - returnCode management
          - `#522 <https://github.com/ansys/pysherlock/pull/522>`_

        * - fix: don't try to launch Sherlock that isn't installed with corresponding version of Ansys
          - `#548 <https://github.com/ansys/pysherlock/pull/548>`_

        * - fix: Error handling: improved for Parts, Lifecycle, and Stackup
          - `#567 <https://github.com/ansys/pysherlock/pull/567>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - MAINT: add action changelog and changelog.rst for release notes
          - `#426 <https://github.com/ansys/pysherlock/pull/426>`_

        * - Update unit test for HV strain map analysis.
          - `#428 <https://github.com/ansys/pysherlock/pull/428>`_

        * - MAINT: Bump ansys-sphinx-theme from 1.1.6 to 1.1.7
          - `#429 <https://github.com/ansys/pysherlock/pull/429>`_

        * - MAINT: Bump grpcio from 1.67.0 to 1.67.1
          - `#433 <https://github.com/ansys/pysherlock/pull/433>`_

        * - MAINT: Bump pytest-cov from 5.0.0 to 6.0.0
          - `#434 <https://github.com/ansys/pysherlock/pull/434>`_

        * - MAINT: Bump ansys-sphinx-theme from 1.1.7 to 1.2.0
          - `#436 <https://github.com/ansys/pysherlock/pull/436>`_

        * - feat: Adding version check to all API methods
          - `#440 <https://github.com/ansys/pysherlock/pull/440>`_

        * - feat: Keith/potting region update
          - `#441 <https://github.com/ansys/pysherlock/pull/441>`_

        * - fix: Analysis.update_harmonic_vibe_props(): add support for setting model source and strain map natural frequency
          - `#442 <https://github.com/ansys/pysherlock/pull/442>`_

        * - docs: update the pull request template
          - `#446 <https://github.com/ansys/pysherlock/pull/446>`_

        * - feat:Keith/copy delete potting region
          - `#448 <https://github.com/ansys/pysherlock/pull/448>`_

        * - MAINT: Bump ansys-sphinx-theme from 1.2.0 to 1.2.1
          - `#449 <https://github.com/ansys/pysherlock/pull/449>`_

        * - doc: project logo
          - `#450 <https://github.com/ansys/pysherlock/pull/450>`_

        * - MAINT: Bump codecov/codecov-action from 4 to 5
          - `#451 <https://github.com/ansys/pysherlock/pull/451>`_

        * - feat: add type hints
          - `#454 <https://github.com/ansys/pysherlock/pull/454>`_

        * - feat: increment version of ansys-api-sherlock to 0.1.35
          - `#461 <https://github.com/ansys/pysherlock/pull/461>`_

        * - fea: adding new PySherlock APIs Layer.list_layers and Layer.export_layer_image
          - `#462 <https://github.com/ansys/pysherlock/pull/462>`_

        * - chore: update CHANGELOG for v0.8.0
          - `#469 <https://github.com/ansys/pysherlock/pull/469>`_

        * - chore: update CHANGELOG for v0.8.1
          - `#471 <https://github.com/ansys/pysherlock/pull/471>`_

        * - MAINT: Bump version ansys-api-sherlock to v0.1.36
          - `#473 <https://github.com/ansys/pysherlock/pull/473>`_

        * - docs: Updated documentation in update potting region.
          - `#477 <https://github.com/ansys/pysherlock/pull/477>`_

        * - MAINT: bump ansys-sphinx-theme from 1.2.3 to 1.2.4
          - `#479 <https://github.com/ansys/pysherlock/pull/479>`_

        * - DOC: New documentation examples
          - `#480 <https://github.com/ansys/pysherlock/pull/480>`_

        * - MAINT: Add support for Python 3.13
          - `#481 <https://github.com/ansys/pysherlock/pull/481>`_

        * - MAINT: bump grpcio from 1.67.1 to 1.69.0
          - `#482 <https://github.com/ansys/pysherlock/pull/482>`_

        * - MAINT: bump ansys-sphinx-theme from 1.2.4 to 1.2.6
          - `#483 <https://github.com/ansys/pysherlock/pull/483>`_

        * - MAINT: Revert grpcio version for tests. Modify dependabot.yml so it doesn't update grpcio dependencies
          - `#485 <https://github.com/ansys/pysherlock/pull/485>`_

        * - chore: update CHANGELOG for v0.8.2
          - `#489 <https://github.com/ansys/pysherlock/pull/489>`_

        * - MAINT: bump ansys-api-sherlock from 0.1.37 to 0.1.38
          - `#490 <https://github.com/ansys/pysherlock/pull/490>`_

        * - feat: Update license file to latest
          - `#494 <https://github.com/ansys/pysherlock/pull/494>`_

        * - MAINT: bump ansys-sphinx-theme from 1.2.6 to 1.2.7
          - `#496 <https://github.com/ansys/pysherlock/pull/496>`_

        * - MAINT: bump ansys-api-sherlock from 0.1.38 to 0.1.39
          - `#497 <https://github.com/ansys/pysherlock/pull/497>`_

        * - MAINT: bump sphinx-gallery from 0.18.0 to 0.19.0
          - `#499 <https://github.com/ansys/pysherlock/pull/499>`_

        * - MAINT: bump ansys-sphinx-theme from 1.2.7 to 1.3.1
          - `#500 <https://github.com/ansys/pysherlock/pull/500>`_

        * - MAINT: bump ansys-api-sherlock from 0.1.39 to 0.1.40
          - `#503 <https://github.com/ansys/pysherlock/pull/503>`_

        * - MAINT: bump sphinx from 8.1.3 to 8.2.0
          - `#504 <https://github.com/ansys/pysherlock/pull/504>`_

        * - MAINT: bump ansys-sphinx-theme from 1.3.1 to 1.3.2
          - `#509 <https://github.com/ansys/pysherlock/pull/509>`_

        * - MAINT: bump sphinx from 8.2.0 to 8.2.3
          - `#516 <https://github.com/ansys/pysherlock/pull/516>`_

        * - MAINT: bump pytest from 8.3.4 to 8.3.5
          - `#518 <https://github.com/ansys/pysherlock/pull/518>`_

        * - MAINT: bump ansys-api-sherlock from 0.1.41 to 0.1.42
          - `#520 <https://github.com/ansys/pysherlock/pull/520>`_

        * - fix: unit test for Layer.list_layers()
          - `#529 <https://github.com/ansys/pysherlock/pull/529>`_

        * - MAINT: bump ansys-api-sherlock from 0.1.43 to 0.1.44
          - `#531 <https://github.com/ansys/pysherlock/pull/531>`_

        * - MAINT: bump ansys-sphinx-theme from 1.3.2 to 1.4.2
          - `#532 <https://github.com/ansys/pysherlock/pull/532>`_

        * - feat: Keith/solder info
          - `#533 <https://github.com/ansys/pysherlock/pull/533>`_

        * - maint: set sphinx-design as documentation requirement
          - `#535 <https://github.com/ansys/pysherlock/pull/535>`_

        * - MAINT: bump pytest-cov from 6.0.0 to 6.1.0
          - `#540 <https://github.com/ansys/pysherlock/pull/540>`_

        * - test: modify test for getting part list properties to validate partNumber instead of validating number of properties
          - `#541 <https://github.com/ansys/pysherlock/pull/541>`_

        * - MAINT: bump pytest-cov from 6.1.0 to 6.1.1
          - `#542 <https://github.com/ansys/pysherlock/pull/542>`_

        * - docs: Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#543 <https://github.com/ansys/pysherlock/pull/543>`_, `#554 <https://github.com/ansys/pysherlock/pull/554>`_

        * - MAINT: Bump ansys/actions from 8 to 9
          - `#544 <https://github.com/ansys/pysherlock/pull/544>`_

        * - fix: stackup test- modified expected CTEz for result of Stackup.get_stackup_props()
          - `#545 <https://github.com/ansys/pysherlock/pull/545>`_

        * - docs: Layer.update_modeling_region()- fixed HTML formatting of example (rem…
          - `#547 <https://github.com/ansys/pysherlock/pull/547>`_

        * - test: fix launcher tests
          - `#549 <https://github.com/ansys/pysherlock/pull/549>`_

        * - MAINT: Bump ansys-api-sherlock from 0.1.45 to 0.1.46
          - `#552 <https://github.com/ansys/pysherlock/pull/552>`_

        * - MAINT: Bump matplotlib from 3.9.2 to 3.10.1
          - `#555 <https://github.com/ansys/pysherlock/pull/555>`_

        * - MAINT: Bump sphinx-notfound-page from 1.0.4 to 1.1.0
          - `#556 <https://github.com/ansys/pysherlock/pull/556>`_

        * - MAINT: Bump ansys-sphinx-theme from 1.3.1 to 1.4.2
          - `#557 <https://github.com/ansys/pysherlock/pull/557>`_

        * - MAINT: Bump sphinx-autodoc-typehints from 2.5.0 to 3.0.1
          - `#558 <https://github.com/ansys/pysherlock/pull/558>`_

        * - docs: Examples: reorganize folders, fix Sphinx warnings
          - `#561 <https://github.com/ansys/pysherlock/pull/561>`_

        * - docs: corrected the syntax of the API example for Model.exportTraceModel()
          - `#565 <https://github.com/ansys/pysherlock/pull/565>`_

        * - chore: Update pre-config-hooks from 4.6.0 to 5.0.0
          - `#566 <https://github.com/ansys/pysherlock/pull/566>`_

        * - MAINT: Bump ansys-sphinx-theme from 1.4.2 to 1.4.3
          - `#568 <https://github.com/ansys/pysherlock/pull/568>`_

        * - MAINT: Bump ansys-sphinx-theme from 1.4.3 to 1.4.4
          - `#569 <https://github.com/ansys/pysherlock/pull/569>`_

        * - MAINT: Bump matplotlib from 3.10.1 to 3.10.3
          - `#570 <https://github.com/ansys/pysherlock/pull/570>`_

        * - docs: document version compatibility in the installation instructions
          - `#571 <https://github.com/ansys/pysherlock/pull/571>`_


`0.8.2 <https://github.com/ansys/pysherlock/releases/tag/v0.8.2>`_ - 2025-01-20
===============================================================================

Documentation
^^^^^^^^^^^^^

- fix: changed Launcher.launch_sherlock() to properly append sherlock_command_args `#487 <https://github.com/ansys/pysherlock/pull/487>`_

`0.8.1 <https://github.com/ansys/pysherlock/releases/tag/v0.8.1>`_ - 2024-12-10
===============================================================================

Fixed
^^^^^

- fix: conf.py issue `#467 <https://github.com/ansys/pysherlock/pull/467>`_
- fix: import statements `#470 <https://github.com/ansys/pysherlock/pull/470>`_


Documentation
^^^^^^^^^^^^^

- MAINT: Bump pytest from 8.3.3 to 8.3.4 `#459 <https://github.com/ansys/pysherlock/pull/459>`_
- MAINT: Bump ansys-sphinx-theme from 1.2.1 to 1.2.3 `#463 <https://github.com/ansys/pysherlock/pull/463>`_

`0.8.0 <https://github.com/ansys/pysherlock/releases/tag/v0.8.0>`_ - 2024-12-10
===============================================================================

Fixed
^^^^^

- fix: conf.py issue `#467 <https://github.com/ansys/pysherlock/pull/467>`_

`0.8.0 <https://github.com/ansys/pysherlock/releases/tag/v0.8.0>`_ - 2024-12-09
===============================================================================

Added
^^^^^

- feat: launching a specific version of Sherlock `#431 <https://github.com/ansys/pysherlock/pull/431>`_


Fixed
^^^^^

- fix: proper AUTHORS file `#438 <https://github.com/ansys/pysherlock/pull/438>`_


Documentation
^^^^^^^^^^^^^

- MAINT: add action changelog and changelog.rst for release notes `#426 <https://github.com/ansys/pysherlock/pull/426>`_
- Update unit test for HV strain map analysis. `#428 <https://github.com/ansys/pysherlock/pull/428>`_
- MAINT: Bump ansys-sphinx-theme from 1.1.6 to 1.1.7 `#429 <https://github.com/ansys/pysherlock/pull/429>`_
- MAINT: Bump grpcio from 1.67.0 to 1.67.1 `#433 <https://github.com/ansys/pysherlock/pull/433>`_
- MAINT: Bump pytest-cov from 5.0.0 to 6.0.0 `#434 <https://github.com/ansys/pysherlock/pull/434>`_
- MAINT: Bump ansys-sphinx-theme from 1.1.7 to 1.2.0 `#436 <https://github.com/ansys/pysherlock/pull/436>`_
- feat: Adding version check to all API methods `#440 <https://github.com/ansys/pysherlock/pull/440>`_
- feat: Keith/potting region update `#441 <https://github.com/ansys/pysherlock/pull/441>`_
- fix: Analysis.update_harmonic_vibe_props(): add support for setting model source and strain map natural frequency `#442 <https://github.com/ansys/pysherlock/pull/442>`_
- docs: update the pull request template `#446 <https://github.com/ansys/pysherlock/pull/446>`_
- feat:Keith/copy delete potting region `#448 <https://github.com/ansys/pysherlock/pull/448>`_
- MAINT: Bump ansys-sphinx-theme from 1.2.0 to 1.2.1 `#449 <https://github.com/ansys/pysherlock/pull/449>`_
- doc: project logo `#450 <https://github.com/ansys/pysherlock/pull/450>`_
- MAINT: Bump codecov/codecov-action from 4 to 5 `#451 <https://github.com/ansys/pysherlock/pull/451>`_
- feat: add type hints `#454 <https://github.com/ansys/pysherlock/pull/454>`_
- feat: increment version of ansys-api-sherlock to 0.1.35 `#461 <https://github.com/ansys/pysherlock/pull/461>`_

.. vale on