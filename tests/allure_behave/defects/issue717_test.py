import allure
import pytest

from allure_behave.utils import step_table
from allure_commons_test.content import csv_equivalent
from hamcrest import assert_that


class RowStub:
    def __init__(self, cells):
        self.cells = cells

    def __iter__(self):
        return iter(self.cells)


class TableStub:
    def __init__(self, headings, rows):
        self.headings = headings
        self.rows = [RowStub(cells) for cells in rows]


class StepStub:
    def __init__(self, content):
        headings, *rows = content
        table = TableStub(headings, rows)
        self.table = table


class CsvTestData:
    def __init__(self, content):
        self.step = StepStub(content)
        self.content = content


@pytest.fixture(params=[
    pytest.param(
        [
            ["a"],
            [","]
        ],
        id="comma"
    ),
    pytest.param(
        [
            ["a"],
            ["\""]
        ],
        id="quote"
    ),
    pytest.param(
        [
            ["a", "b"],
            ["1,2", "3,4"]
        ],
        id="2c-commas"
    ),
    pytest.param(
        [
            ["a", "b"],
            ["\"1\",2", "3\",4"]
        ],
        id="mix"
    )
])
def csv_testdata(request):
    yield CsvTestData(request.param)


@allure.issue("717")
def test_step_table_data_escaping(csv_testdata):
    assert_that(
        step_table(csv_testdata.step),
        csv_equivalent(csv_testdata.content)
    )
