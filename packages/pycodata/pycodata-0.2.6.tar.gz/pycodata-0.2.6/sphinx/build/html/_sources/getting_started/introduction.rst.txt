Description
============

Python wrapper around the
`(Modern) Fortran codata library <https://milanskocic.github.io/codata/index.html>`_.
Follow the `installation instructions <https://milanskocic.github.io/codata/md_introduction_install.html>`_.
for compiling and installing the library.
The wrapper must also be compiled on the host platform after installing the codata library. 
The compilation of the wrapper is trivial and it should work with every C compiler as long as the codata library
was compiled and installed with all paths set properly.

The list of the available constants is available 
`here <https://milanskocic.github.io/codata/md_introduction_raw_codata.html>`_.

The version of the python wrapper follows the versions (major and minor) of the codata library.
The patches will be indenpendent.

How to install
=================

.. literalinclude:: ../../../INSTALL.txt
    :language: python

Dependencies
==============

.. literalinclude:: ../../../requirements.txt

License
==========

.. literalinclude:: ../../../LICENSE.txt