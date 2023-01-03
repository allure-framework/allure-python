import csv
import io

from hamcrest.core.base_matcher import BaseMatcher


class CsvEquivalent(BaseMatcher):
    def __init__(self, rows, **csv_kwargs):
        self.__rows = rows
        self.__csv_kwargs = csv_kwargs

    def _matches(self, item):
        with io.StringIO(item, newline="") as stream:
            reader = csv.reader(stream, **self.__csv_kwargs)
            return list(reader) == self.__rows

    def describe_to(self, description):
        description.append_text(
            f"csv document equivalent to {self.__rows!r}"
        )


def csv_equivalent(rows, **csv_kwargs):
    return CsvEquivalent(rows, **csv_kwargs)
