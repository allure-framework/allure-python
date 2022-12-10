from hamcrest.core.base_matcher import BaseMatcher
from hamcrest import all_of


class MapsTo(BaseMatcher):
    def __init__(self, mapping, *value_matchers):
        self.__mapping = mapping
        self.__value_matcher = all_of(*value_matchers)

    def _matches(self, item):
        if item not in self.__mapping:
            return False
        return self.__value_matcher.matches(
            self.__mapping[item]
        )

    def describe_to(self, description):
        keys = list(self.__mapping)
        description.append_text(
            f"one of keys {keys!r} mapping to "
        )
        self.__value_matcher.describe_to(description)


def maps_to(mapping, *value_matchers):
    return MapsTo(mapping, *value_matchers)
