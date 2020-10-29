import unittest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from test.example_runner import run_docstring_example


class TestStatus(unittest.TestCase):
    def test_passed_status(self):
        """
        >>> import unittest

        >>> class TestStatusExample(unittest.TestCase):
        ...     def test_passed_example(self):
        ...         assert True
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_passed_example",
                                  with_status("passed"))
                    )

    def test_failed_status(self):
        """
        >>> import unittest

        >>> class TestStatusExample(unittest.TestCase):
        ...     def test_failed_example(self):
        ...         assert False, "my message"
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_failed_example",
                                  with_status("failed"),
                                  has_status_details(with_message_contains("my message"))
                                  )
                    )

    def test_broken_status(self):
        """
        >>> import unittest

        >>> class TestStatusExample(unittest.TestCase):
        ...     def test_broken_example(self):
        ...         raise Exception("my error")
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_broken_example",
                                  with_status("broken"),
                                  has_status_details(with_message_contains("my error"))
                                  )
                    )

    def test_skipped_status(self):
        """
        >>> import unittest

        >>> class TestStatusExample(unittest.TestCase):
        ...     def test_skipped_example(self):
        ...         self.skipTest('my skip reason')
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_skipped_example",
                                  with_status("skipped"),
                                  has_status_details(with_message_contains("my skip reason"))
                                  )
                    )