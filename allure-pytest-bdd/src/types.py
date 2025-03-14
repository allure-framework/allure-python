from collections import namedtuple


AllurePytestBddTestData = namedtuple(
    "AllurePytestBddTestData",
    ["feature", "scenario", "pytest_params"],
)
