from allure_commons.logger import AllureFileLogger
from allure_commons.model2 import ENVIRONMENT_FILE
from allure_commons_test.report import parse_properties


def read_environment(report_dir):
    path = report_dir / ENVIRONMENT_FILE
    return dict(parse_properties(path.read_text(encoding="utf-8")))


def test_environment_is_written(tmp_path):
    logger = AllureFileLogger(tmp_path)

    logger.report_environment({"browser": "chrome", "env": "staging"})

    assert read_environment(tmp_path) == {"browser": "chrome", "env": "staging"}


def test_environment_is_merged(tmp_path):
    logger = AllureFileLogger(tmp_path)

    logger.report_environment({"browser": "chrome", "env": "staging"})
    logger.report_environment({"browser": "firefox", "version": "1.2.3"})

    assert read_environment(tmp_path) == {
        "browser": "firefox",
        "env": "staging",
        "version": "1.2.3"
    }


def test_special_characters_are_escaped(tmp_path):
    environment = {
        "os.name": "Windows 11",
        "key with spaces": "value with spaces",
        "key=with=separators": "a\nb",
        "key:with:colons": "c:\\temp",
        "back\\slash": "d\\e"
    }
    logger = AllureFileLogger(tmp_path)

    logger.report_environment(environment)

    assert read_environment(tmp_path) == environment


def test_non_ascii_values_are_written(tmp_path):
    logger = AllureFileLogger(tmp_path)

    logger.report_environment({"browser": "Я.Браузер"})

    assert read_environment(tmp_path) == {"browser": "Я.Браузер"}


def test_empty_environment_creates_no_file(tmp_path):
    logger = AllureFileLogger(tmp_path)

    logger.report_environment({})

    assert not (tmp_path / ENVIRONMENT_FILE).exists()
