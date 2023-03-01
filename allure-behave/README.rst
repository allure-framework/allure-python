Allure Behave Formatter
=======================
.. image:: https://img.shields.io/pypi/v/allure-behave
        :alt: Release Status
        :target: https://pypi.python.org/pypi/allure-behave
.. image:: https://img.shields.io/pypi/dm/allure-behave
        :alt: Downloads
        :target: https://pypi.python.org/pypi/allure-behave

- `Source <https://github.com/allure-framework/allure-python>`_

- `Documentation <https://docs.qameta.io/allure-report>`_

- `Gitter <https://gitter.im/allure-framework/allure-core>`_


Installation and Usage
======================

.. code:: bash

    $ pip install allure-behave
    $ behave -f allure_behave.formatter:AllureFormatter -o %allure_result_folder% ./features
    $ allure serve %allure_result_folder%


Support behave parallel
-----------------------

Current implementation of behave-parallel makes some allure features inaccessible. So in this case you need patch your
environment.py files instead using formatter. If you don't use environment.py, just crate empty one with calling allure
like in example below.

.. code:: python

    from allure_behave.hooks import allure_report

    ### your code

    allure_report("path/to/result/dir")

Usage examples
--------------

See usage examples `here <examples>`_.
