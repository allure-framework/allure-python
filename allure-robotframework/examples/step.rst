==================
Steps and substeps
==================

All keywords of a Robot Framework test case are automatically converted to
allure steps.

To add nested steps apply the :code:`@allure.step` decorator to a step function
or use the :code:`allure.step` function in your test library:

**my_lib.py**:

..  code:: python
    :name: steps-lib

    import allure

    @allure.step("Substep {parameter}")
    def substep_with_decorator(parameter):
        pass

    def substep():
        with allure.step("Library substep"):
            substep_with_decorator("A")
            pass

**The test data**:

..  code:: robotframework
    :name: steps-robot

    *** Settings ***
    Library     ./my_lib.py

    *** Test Cases ***
    Allure substeps
        Substep