# Todo test mp
from tests.allure_nose2.nose2_runner import AllureNose2Runner


def test_func_fullname(nose2_runner: AllureNose2Runner):
    """
    >>> def test_func_fullname_example1():
    ...     pass
    >>> def test_func_fullname_example2():
    ...     pass
    >>> def test_func_fullname_example3():
    ...     pass
    """
    nose2_runner.run_docstring()
