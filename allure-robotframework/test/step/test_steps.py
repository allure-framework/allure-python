import unittest
import os

from allure_robotframework.constants import RobotBasicKeywords
from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.result import with_status, has_step, has_attachment, has_parameter
from hamcrest import assert_that, all_of


def has_step_with_keyword_log(step_name, *matchers):
    return has_step(
        step_name,
        has_attachment(attach_type='text/html', name='Keyword Log'),
        *matchers
    )


class CaseStatus(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_one_step(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'One Step',
                has_step_with_keyword_log(RobotBasicKeywords.NO_OPERATION)
            )
        )

    def test_several_steps(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Several Steps',
                all_of(
                    has_step_with_keyword_log(
                        RobotBasicKeywords.LOG,
                        has_parameter('arg1', 'First Step')
                    ),
                    has_step_with_keyword_log(
                        RobotBasicKeywords.LOG,
                        has_parameter('arg1', 'Second Step')
                    ),
                    has_step_with_keyword_log(
                        RobotBasicKeywords.LOG,
                        has_parameter('arg1', 'Third Step')
                    ),
                )
            )
        )

    def test_different_status_steps(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Different Status Steps',
                all_of(
                    has_step_with_keyword_log(
                        RobotBasicKeywords.NO_OPERATION,
                        with_status('passed')
                    ),
                    has_step_with_keyword_log(
                        RobotBasicKeywords.FAIL,
                        with_status('failed')
                    )
                )
            )
        )

    def test_embedded_steps(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Embedded Steps',
                has_step_with_keyword_log(
                    'First Step',
                    has_step_with_keyword_log(
                        'Second Step',
                        has_step_with_keyword_log(
                            'Third Step',
                            has_step_with_keyword_log(RobotBasicKeywords.NO_OPERATION)
                        )
                    )
                )
            )
        )
