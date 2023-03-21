# Todo test mp
from test.example_runner import run_docstring_example

def test_func_fullname():
    """
    >>> def test_func_fullname_example1():
    ...     pass
    >>> def test_func_fullname_example2():
    ...     pass
    >>> def test_func_fullname_example3():
    ...     pass
    """
    allure_report = run_docstring_example()