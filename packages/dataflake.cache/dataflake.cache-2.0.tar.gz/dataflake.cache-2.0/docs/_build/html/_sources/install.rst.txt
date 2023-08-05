Installation
============

You will need `Python <http://python.org>`_ version 2.7 or better to
run :mod:`dataflake.cache`.

It is advisable to install :mod:`dataflake.cache` into a
:term:`virtualenv` in order to obtain isolation from any "system"
packages you've got installed in your Python version (and likewise, 
to prevent :mod:`dataflake.cache` from globally installing 
versions of packages that are not compatible with your system Python).

After you've got the requisite dependencies installed, you may install
:mod:`dataflake.cache` into your Python environment using pip::

  $ pip install dataflake.cache

If you use :mod:`zc.buildout` you can add :mod:`dataflake.cache`
to the necessary ``eggs`` section to have it pulled in automatically.
