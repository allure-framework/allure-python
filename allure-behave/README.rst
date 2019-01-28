Allure Behave Formatter
=======================
.. image:: https://pypip.in/v/allure-behave/badge.png
        :alt: Release Status
        :target: https://pypi.python.org/pypi/allure-behave
.. image:: https://pypip.in/d/allure-behave/badge.png
        :alt: Downloads
        :target: https://pypi.python.org/pypi/allure-behave

- `Source <https://github.com/allure-framework/allure-python>`_

- `Documentation <https://docs.qameta.io/allure/2.0/>`_

- `Gitter <https://gitter.im/allure-framework/allure-core>`_


Installation and Usage
======================

.. code:: bash

    $ pip install allure-behave
    $ behave -f allure_behave.formatter:AllureFormatter -o %allure_result_folder% ./features
    $ allure serve %allure_result_folder%