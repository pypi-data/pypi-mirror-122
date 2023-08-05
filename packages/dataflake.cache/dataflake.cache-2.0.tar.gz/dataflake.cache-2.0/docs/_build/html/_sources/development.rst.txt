=============
 Development
=============


Getting the source code
=======================
The source code is maintained on GitHub. To check out the trunk:

.. code-block:: sh

  $ git clone https://github.com/dataflake/dataflake.cache.git

You can also browse the code online at
https://github.com/dataflake/dataflake.cache


Bug tracker
===========
For bug reports, suggestions or questions please use the
GitHub issue tracker at
https://github.com/dataflake/dataflake.cache/issues.


Using the buildout configuration
================================
:mod:`dataflake.cache` ships with its own :file:`buildout.cfg` buildout
configuration file. The buildout procedure will set up all requirements
for running the unit tests and building the documentation.

Using the buildout configuration requires a one-time bootstrap procedure, which
differs depending on the Python version.

.. code-block:: console

    $ cd /path/to/dataflake.cache
    $ python2.7 -m virtualenv .     # PYTHON 2
    $ python3 -m venv .             # PYTHON 3
    $ bin/pip install -U pip        # Make sure pip is compatible
    $ bin/pip install -Ur requirements.txt


Running the tests
=================
Once you have a buildout finished, the tests can be run as follows:

.. code-block:: console

    $ bin/test
    Running zope.testrunner.layer.UnitTests tests:
      Set up zope.testrunner.layer.UnitTests in 0.000 seconds.
      Ran 23 tests with 0 failures, 0 errors and 0 skipped in 1.628 seconds.
    Tearing down left over layers:
      Tear down zope.testrunner.layer.UnitTests in 0.000 seconds.


The package also ships with a ``tox`` configuration that will run the tests
across all supported Python versons, and the linting and code coverage check:

.. code-block:: console

    $ bin/tox
    ...
    py27: commands succeeded
    py34: commands succeeded
    py35: commands succeeded
    py36: commands succeeded
    py37: commands succeeded
    py38: commands succeeded
    pypy: commands succeeded
    pypy3: commands succeeded
    jython: commands succeeded
    coverage: commands succeeded
    flake8: commands succeeded


Building the documentation
==========================
The :mod:`dataflake.cache` buildout installs the Sphinx scripts required 
to build the documentation, including testing its code snippets:

.. code-block:: console

   $ cd docs
   $ make doctest html
   Running Sphinx...
   ...
   running tests...

   Document: usage
   ---------------
   1 items passed all tests:
     14 tests in default
   14 tests in 1 items.
   14 passed and 0 failed.
   Test passed.
   
   Doctest summary
   ===============
      14 tests
       0 failures in tests
       0 failures in setup code
   build succeeded.
   ...
   Running Sphinx...
   ...
   build succeeded.

   The HTML pages are in _build/html.


Making a release
================
Make sure you have the added requirements ``wheel`` and ``twine`` available:

.. code-block:: console

    $ cd /path/to/dataflake.cache
    $ bin/pip install -U wheel twine
    $ rm -rf dist
    $ bin/buildout -N
    $ bin/buildout setup setup.py sdist bdist_wheel
    $ bin/twine upload -s dist/*

The ``bin/buildout`` step will make sure the correct package information 
is used.
