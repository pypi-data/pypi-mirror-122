# This file is part of BurnMan - a thermoelastic and thermodynamic toolkit for
# the Earth and Planetary Sciences
# Copyright (C) 2012 - 2021 by the BurnMan team, released under the GNU
# GPL v2 or later.


"""
Introducing BurnMan |version|
=============================

Overview
--------

BurnMan is an open source mineral physics and seismological toolkit written in Python
which can enable a user to calculate (or fit) the physical and chemical properties
of endmember minerals, fluids/melts, solid solutions, and composite assemblages.

Properties which BurnMan can calculate include:

  - the thermodynamic free energies, allowing phase equilibrium calculations,
    endmember activities, chemical potentials and oxygen (and other) fugacities.

  - entropy, enabling the user to calculate isentropes for a given assemblage.

  - volume, to allow the user to create density profiles.

  - seismic velocities, including Voigt-Reuss-Hill and Hashin-Strikman bounds
    and averages.

The toolkit itself comes with a large set of classes and functions which are
designed to allow the user to easily combine mineral physics with
geophysics, and geodynamics. The features of BurnMan include:

  - the full codebase, which includes implementations of many static and thermal equations of state
    (including Vinet, Birch Murnaghan, Mie-Debye-Grueneisen, Modified Tait),
    and solution models (ideal, symmetric, asymmetric, subregular).
  - popular endmember and solution datasets already coded into burnman-usable format
    (including :cite:`HP2011`, :cite:`Stixrude2005` and :cite:`Stixrude2011`)
  - Optimal least squares fitting routines for multivariate data with (potentially correlated) errors
    in pressure and temperature. As an example, such functions can be used to
    simultaneously fit volumes, seismic velocities and enthalpies.
  - a "Planet" class, which self-consistently calculates gravity profiles, mass, moment of
    inertia of planets given the chemical and temperature structure of a planet
  - published geotherms
  - a tutorial on the basic use of BurnMan
  - a large collection of annotated examples
  - a set of high-level functions which create files readable by seismological and geodynamic software,
    including: Mineos :cite:`Masters2011`, AxiSEM :cite:`NissenMeyer2014` and ASPECT
  - an extensive suite of unit tests to ensure code functions as intended
  - a series of benchmarks comparing BurnMan output with published data
  - a directory containing user-contributed code from published papers

BurnMan makes extensive use of `SciPy <http://www.scipy.org/>`_,
`NumPy <http://www.numpy.org/>`_ and `SymPy <http://www.sympy.org/>`_
which are widely used Python libraries for scientific computation.
`Matplotlib <http://matplotlib.org/>`_ is used
to display results and produce publication quality figures.
The computations are consistently formulated in terms of SI units.

The code documentation including class and function descriptions can be found online at
http://burnman.readthedocs.io.

This software has been designed to allow the end-user a great deal of freedom
to do whatever calculations they may wish and to add their own modules.
The underlying Python classes have been designed to make new endmember,
solid solution and composite models easy to read and create.
We have endeavoured to provide examples and benchmarks which cover the
most popular uses of the software, some of which are included in the figure below.
This list is certainly not exhaustive, and we will definitely have missed interesting
applications. We will be very happy to accept contributions in
form of corrections, examples, or new features.

Structure
---------
.. image:: figures/structure.png


.. _ref-installation:

Installation
------------

Requirements
^^^^^^^^^^^^

  - Python 3.7+
  - Python modules: NumPy, SciPy, SymPy, Matplotlib


Source code
^^^^^^^^^^^
The source code can be found at https://github.com/geodynamics/burnman.

Install under Ubuntu
^^^^^^^^^^^^^^^^^^^^

1. Install dependencies using apt by opening a terminal window and entering
   ``sudo apt-get install python python-scipy python-numpy python-sympy python-matplotlib git``
2. Clone the BurnMan repository ``git clone https://github.com/geodynamics/burnman.git``
3. Go to the Burnman examples directory and type:
   ``python example_beginner.py``
   Figures should show up, indicating that it is working.


Install on a Mac
^^^^^^^^^^^^^^^^

1. get Xcode
2. If you don't have Python yet, download it (for free) from
   python.org/download . Make sure to use Python 3.7+.
   To check your version of python, type the following in a
   terminal: ``python --version``
3. Install the latest Numpy version from http://sourceforge.net/projects/numpy/files/NumPy/
4. Install the latest Scipy from http://sourceforge.net/projects/scipy/files/
5. Install the latest Sympy from http://sourceforge.net/projects/sympy/files/
6. Install the latest Matplotlib from http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.1.1/
7. Clone the BurnMan repository ``git clone https://github.com/geodynamics/burnman.git``
8. Go to the Burnman examples directory and type ``python example_beginner.py``
   Figures should show up, indicating that it is working.

Install under Windows
^^^^^^^^^^^^^^^^^^^^^

To get Python running under Windows:

1. Download Python from http://www.python.org/ and install
2. Go to http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy, download and install
3. Go to http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy, download and install
4. Go to http://www.lfd.uci.edu/~gohlke/pythonlibs/#sympy, download and install
5. Go to http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib, download and install
6. Download BurnMan from github (https://github.com/geodynamics/burnman)
7. Open Python Shell (IDLE Python GUI)
8. File -- Open -- find one of the example files
9. Run the module (or press F5)


Citing BurnMan
--------------

If you use BurnMan in your work, we ask that you cite the following publications:

  - Myhill, R., Cottaar, S., Heister, T., Rose, I., and Unterborn, C. (2021):
    BurnMan v1.0.0 [Software]. Computational Infrastructure for Geodynamics. Zenodo.
    `(https://doi.org/10.5281/zenodo.5552443) <https://doi.org/10.5281/zenodo.5552443>`_

  - Cottaar S., Heister, T., Rose, I., and Unterborn, C., 2014, BurnMan: A
    lower mantle mineral physics toolkit, Geochemistry, Geophysics, and
    Geosystems, 15(4), 1164-1179 `(https://doi.org/10.1002/2013GC005122)
    <https://doi.org/10.1002/2013GC005122>`_

Contributing to BurnMan
-----------------------

If you would like to contribute bug fixes, new functions or new modules
to the existing codebase, please contact us at info@burnman.org or make a
pull request at `https://github.com/geodynamics/burnman <https://github.com/geodynamics/burnman>`_.

BurnMan also includes a contrib directory that contains python and ipython
scripts used to reproduce published results. We welcome the submission of
new contributions to this directory. As with the contribution of code,
please contact us at info@burnman.org or make a pull request at
`https://github.com/geodynamics/burnman <https://github.com/geodynamics/burnman>`_.

Acknowledgement and Support
---------------------------

  - This project was initiated at, and follow-up research support was received
    through, Cooperative Institute of Deep Earth Research, CIDER (NSF FESD
    grant 1135452) -- see `www.deep-earth.org <http://www.deep-earth.org>`_

  - We thank all the members of the CIDER Mg/Si team for their input:
    Valentina Magni, Yu Huang, JiaChao Liu, Marc Hirschmann, and Barbara
    Romanowicz. We also thank Lars Stixrude for providing benchmarking calculations
    and Zack Geballe, Motohiko Murakami, Bill McDonough, Quentin Williams,
    Wendy Panero, and Wolfgang Bangerth for helpful discussions.

  - We thank CIG (`www.geodynamics.org <http://www.geodynamics.org>`_) for support
    and accepting our donation of BurnMan as an official project.

"""
from __future__ import absolute_import
from .version import version as __version__

# Classes and associated functions for representing rocks and minerals:
from .classes.material import Material, material_property
from .classes.perplex import PerplexMaterial
from .classes.mineral import Mineral
from .classes.combinedmineral import CombinedMineral
from .classes.solutionmodel import SolutionModel
from .classes.solidsolution import SolidSolution
from .classes.composite import Composite
from .classes.anisotropy import AnisotropicMaterial
from .classes.anisotropicmineral import AnisotropicMineral
from .classes.anisotropicmineral import cell_parameters_to_vectors
from .classes.anisotropicmineral import cell_vectors_to_parameters
from .classes.mineral_helpers import HelperLowHighPressureRockTransition
from .classes.mineral_helpers import HelperSpinTransition
from .classes.mineral_helpers import HelperRockSwitcher

# Other classes
from .classes.composition import Composition
from .classes.layer import Layer
from .classes.planet import Planet
from .classes.polytope import MaterialPolytope
from .classes import seismic
from .classes import averaging_schemes

# Mineral library
from . import minerals

# Equations of state
from . import eos

# Tools
from . import tools
from .tools import geotherm
from .tools.equilibration import equilibrate
from .tools.partitioning import calculate_nakajima_fp_pv_partition_coefficient

# Optimization functions
from .optimize import composition_fitting
from .optimize import linear_fitting
from .optimize import nonlinear_fitting
from .optimize import nonlinear_solvers
from .optimize import eos_fitting
