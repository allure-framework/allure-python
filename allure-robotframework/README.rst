Allure Robot Framework Listener
===============================

-  `Source <https://github.com/allure-framework/allure-python>`_

-  `Documentation <https://docs.qameta.io/allure/2.0>`_

-  `Gitter <https://gitter.im/allure-framework/allure-core>`_

Installation and Usage
======================

.. code:: bash

    $ pip install allure-robotframework
    $ robot --listener allure_robotframework ./my_robot_test

Optional argument sets output directory. Example:

.. code:: bash

    $ robot --listener allure_robotframework;/set/your/path/here ./my_robot_test

Default output directory is `output/allure`.

Listener support `robotframework-pabot library <https://pypi.python.org/pypi/robotframework-pabot>`_:

.. code:: bash

    $ pabot --listener allure_robotframework ./my_robot_test