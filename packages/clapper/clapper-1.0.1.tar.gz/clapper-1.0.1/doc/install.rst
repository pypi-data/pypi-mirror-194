.. SPDX-FileCopyrightText: Copyright © 2022 Idiap Research Institute <contact@idiap.ch>
..
.. SPDX-License-Identifier: BSD-3-Clause

.. _clapper.install:

==============
 Installation
==============

We support two installation modes, through pip_, or mamba_ (conda), for two
types of releases, stable, or beta (a.k.a. development, latest).  Choose a
combination from the tabbed pane below.


.. tab:: pip/stable

   .. code-block:: sh

      pip install clapper


.. tab:: pip/beta

   .. code-block:: sh

      pip install git+https://gitlab.idiap.ch/software/clapper


.. tab:: conda/stable

   .. code-block:: sh

      mamba install -c conda-forge clapper


.. tab:: conda/beta

   .. code-block:: sh

      mamba install -c https://www.idiap.ch/software/biosignal/conda/label/beta -c conda-forge clapper


.. include:: links.rst
