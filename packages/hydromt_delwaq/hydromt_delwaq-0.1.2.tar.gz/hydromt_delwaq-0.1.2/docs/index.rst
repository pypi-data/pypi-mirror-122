======================
HydroMT plugin: DELWAQ
======================

`HydroMT <https://github.com/Deltares/hydromt>`_ is a python package, developed by Deltares, to build 
and analyse environmental models. It provides a generic model api with attributes to access the model schematization, 
(dynamic) forcing data, results and states.

This plugin provides an implementation for the `DELWAQ <https://oss.deltares.nl/web/delft3d/delwaq1>`_ water quality engine. 
It details the different steps and explains how to use HydroMT to easily get started and work on your own DELWAQ model. WIth this plugin 
you can interact with both classic **D-Water Quality** models as well as **D-Emission** models.

For detailed information on HydroMT itself, you can visit the `core documentation <https://deltares.github.io/hydromt_plugin/latest/>`_.

Documentation
=============

**Getting Started**

* :doc:`intro`
* :doc:`installation`
* :doc:`examples/index`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started

   intro
   installation
   examples/index

**User Guide**

* :doc:`user_guide/components`
* :doc:`user_guide/build_configuration`
* :doc:`user_guide/attributes`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: User Guide

   user_guide/components
   user_guide/build_configuration
   user_guide/attributes

**Advanced topics**

* :doc:`advanced/workflows`
* :doc:`advanced/coupling_wflow`
* :doc:`advanced/generic_delwaq`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Advanced topics

   advanced/workflows
   advanced/coupling_wflow
   advanced/generic_delwaq

**References & Help**

* :doc:`api/api_index`
* :doc:`contributing`
* :doc:`changelog`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: References & Help

   api/api_index
   contributing
   changelog


License
-------

Copyright (c) 2021, Deltares

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You can find the full terms of the GNU General Public License at <https://www.gnu.org/licenses/>.
