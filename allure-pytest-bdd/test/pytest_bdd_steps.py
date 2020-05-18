from pytest_bdd import given, when
from pytest_bdd import parsers


@given(parsers.parse("feature file {name} with content:\n\"\"\"\n{feature}\n\"\"\""))
def feature_definition(feature, testdir, name="example"):
    testdir.makefile("{name}.feature".format(name=name), **dict([(name, feature)]))
    pass


@given("dummy steps in conftest.py")
def dummy_steps(request, testdir):
    dummy_steps_path = request.config.rootdir.join("test", "dummy_steps.py")
    with open(dummy_steps_path, encoding="utf-8") as f:
        content = f.read()
        testdir.makeconftest(content)


@given(parsers.parse('test file with "{scenario}" scenario in {feature}'))
def test_file_with_scenario(testdir, scenario, feature):
    testdir.makepyfile(current_test="""
    from pytest_bdd import scenario

    @scenario("{feature}.feature", "{scenario}")
    def test_it():
        pass

    """.format(scenario=scenario, feature=feature))


@when("run pytest-bdd with allure")
def run(allured_testdir):
    allured_testdir.run_with_allure()
