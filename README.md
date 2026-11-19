# Allure Python Integrations

[![Build](https://github.com/allure-framework/allure-python/actions/workflows/build.yaml/badge.svg)](https://github.com/allure-framework/allure-python/actions/workflows/build.yaml)

> The repository contains adapters for Python-based test frameworks.

[<img src="https://allurereport.org/public/img/allure-report.svg" height="85px" alt="Allure Report logo" align="right" />](https://allurereport.org "Allure Report")

- Learn more about Allure Report at [https://allurereport.org](https://allurereport.org)
- 📚 [Documentation](https://allurereport.org/docs/) – discover official documentation for Allure Report
- ❓ [Questions and Support](https://github.com/orgs/allure-framework/discussions/categories/questions-support) – get help from the team and community
- 📢 [Official announcements](https://github.com/orgs/allure-framework/discussions/categories/announcements) –  stay updated with our latest news and updates
- 💬 [General Discussion](https://github.com/orgs/allure-framework/discussions/categories/general-discussion) – engage in casual conversations, share insights and ideas with the community
- 🖥️ [Live Demo](https://demo.allurereport.org/) — explore a live example of Allure Report in action

---

## Pytest
[![Release
Status](https://img.shields.io/pypi/v/allure-pytest)](https://pypi.python.org/pypi/allure-pytest)
[![Downloads](https://img.shields.io/pypi/dm/allure-pytest)](https://pypi.python.org/pypi/allure-pytest)

Allure [pytest](http://pytest.org) integration. It's developed as pytest
plugin and distributed via
[pypi](https://pypi.python.org/pypi/allure-pytest).

[Usage examples](/allure-pytest/examples).

## Behave
[![Release
Status](https://img.shields.io/pypi/v/allure-behave)](https://pypi.python.org/pypi/allure-behave)
[![Downloads](https://img.shields.io/pypi/dm/allure-behave)](https://pypi.python.org/pypi/allure-behave)

Allure [behave](https://behave.readthedocs.io/en/latest/) integration.
Just external formatter that produce test results in allure2 format.
This package is available on
[pypi](https://pypi.python.org/pypi/allure-behave).

[Usage examples](/allure-behave/examples).

## Robot Framework
[![Release
Status](https://img.shields.io/pypi/v/allure-robotframework)](https://pypi.python.org/pypi/allure-robotframework)
[![Downloads](https://img.shields.io/pypi/dm/allure-robotframework)](https://pypi.python.org/pypi/allure-robotframework)

Allure [RobotFramework](http://robotframework.org/) integration. This
integration is a
[Listener](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface\))
and does not require changing autotests.

[Read more ...](/allure-robotframework/README.rst).

[Usage examples](/allure-robotframework/examples).

## Pytest-BDD

[![Release
Status](https://img.shields.io/pypi/v/allure-pytest-bdd)](https://pypi.python.org/pypi/allure-pytest-bdd)
[![Downloads](https://img.shields.io/pypi/dm/allure-pytest-bdd)](https://pypi.python.org/pypi/allure-pytest-bdd)

Allure [pytest-bdd](http://pytest.org) integration. It's developed as
pytest plugin and distributed via
[pypi](https://pypi.python.org/pypi/allure-pytest-bdd).

## Nose2
[![Release
Status](https://img.shields.io/pypi/v/allure-nose2)](https://pypi.python.org/pypi/allure-nose2)
[![Downloads](https://img.shields.io/pypi/dm/allure-nose2)](https://pypi.python.org/pypi/allure-nose2)

## Skipping muted tests

All adapters support `excludedTests` in the JSON test plan supplied through
`ALLURE_TESTPLAN_PATH`:

```json
{
  "version": "1.0",
  "excludedTests": [
    { "id": 101 },
    { "selector": "test_checkout#test_expired_card" }
  ]
}
```

A matching test is skipped before its body runs and, when reporting is enabled,
retained with `status: "skipped"` and `statusDetails.muted: true`. Existing
runner filters and test-plan selection still apply: muting never adds tests to
the run. Omitting `tests`, or using `"tests": []`, leaves selection unrestricted
under the adapter’s existing rules. pytest-bdd and nose2 do not add test-plan
selection; they apply muting to the tests selected by their runners.

IDs match static Allure ID annotations/tags, with numeric and string IDs treated
alike. IDs assigned dynamically inside a test body cannot be used for skipping.
Selectors match the adapter’s existing `fullName` exactly (not as a regex):

| Adapter | Selector |
| --- | --- |
| pytest | `module#test`, or `module.Class#test` |
| Behave | `Feature name: Scenario name` |
| Robot Framework | `Suite.Test name` |
| pytest-bdd | `<feature.rel_filename>:Scenario name` |
| nose2 | `module.test`, or `module.Class.test` |

An entry matches by ID **or** selector; an unmatched ID does not prevent a
selector match. Parameterized tests and scenario outlines keep their existing
identities, so one selector may skip multiple cases. Use the reported `fullName`
for the exact selector, including framework-specific paths and rendered names.

Skipping uses each runner’s lifecycle. Discovery, suite setup and other hooks
may still run. Robot Framework uses its native `robot:skip` tag (Robot Framework
4+), and works with the listener alone or the existing test-plan prerun modifier.
Behave’s existing skipped-result visibility options still apply.

## Allure python commons

Common engine for all modules. It is useful for make integration with
your homemade frameworks.

## Allure python commons test

Just pack of hamcrest matchers for validation result in allure2 json
format.
