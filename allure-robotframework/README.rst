Allure Robot Framework Listener
===============================
.. image:: https://img.shields.io/pypi/v/allure-robotframework
        :alt: Release Status
        :target: https://pypi.python.org/pypi/allure-robotframework
.. image:: https://img.shields.io/pypi/dm/allure-robotframework
        :alt: Downloads
        :target: https://pypi.python.org/pypi/allure-robotframework

-  `Source <https://github.com/allure-framework/allure-python>`_

-  `Documentation <https://docs.qameta.io/allure-report/>`_

-  `Gitter <https://gitter.im/allure-framework/allure-core>`_

Installation and Usage
======================

.. code:: bash

    $ pip install allure-robotframework
    $ robot --listener allure_robotframework ./my_robot_test

Optional argument sets output directory. Example:

.. code:: bash

    $ robot --listener allure_robotframework:/set/your/path/here ./my_robot_test

Default output directory is `output/allure`.

Listener support `robotframework-pabot library <https://pypi.python.org/pypi/robotframework-pabot>`_:

.. code:: bash

    $ pabot --listener allure_robotframework ./my_robot_test

Advanced listener settings:

    - ALLURE_MAX_STEP_MESSAGE_COUNT=5. If robotframework step contains less messages than specified in this setting, each message shows as substep. This reduces the number of attachments in large projects. The default value is zero - all messages are displayed as attachments.

Usage examples
--------------

See usage examples `here <examples>`_.


Contributing to allure-robotframework
=====================================

This project exists thanks to all the people who contribute. Especially by `Megafon <https://corp.megafon.com>`_ and
`@skhomuti <https://github.com/skhomuti>`_ who started and maintaining allure-robotframework.
