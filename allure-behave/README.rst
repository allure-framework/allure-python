Allure Behave Formatter
=======================

- `Source <https://github.com/allure-framework/allure-python>`_

- `Documentation <https://docs.qameta.io/allure/2.0/>`_

- `Gitter <https://gitter.im/allure-framework/allure-core>`_


Installation and Usage
======================

.. code:: bash

    $ pip install allure-behave
    $ behave -f allure_behave.formatter:AllureFormatter -o %allure_result_folder% ./features
    $ allure serve %allure_result_folder%